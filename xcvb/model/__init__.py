import os.path
import json
import glob
import pkg_resources
import yaml
import couch
import tornado.log
import tornado.autoreload


class Base:

    def __init__(self, application):
        if Base.__dict__.get("couch") is None:
            Base.couch = initialize(application.config["couchdb"]["url"])


def upload_docs(path, blocking_couch):
    with open(path) as f:
        docs = yaml.load(f) if path.endswith(".yaml") else json.load(f)
        docs = [docs] if isinstance(docs, dict) else docs
    for doc in docs:
        try:
            old = blocking_couch.get_doc(doc["_id"])
            doc["_rev"] = old["_rev"]
        except (couch.NotFound, KeyError):
            old = None
        tornado.log.app_log.info("Uploading {}".format(
            os.path.relpath(path))) if doc != old else None
        try:
            blocking_couch.save_doc(doc) if doc != old else None
        except couch.Conflict:
            pass


def initialize(couchdb_url):
    blocking_couch = couch.BlockingCouch(couch_url=couchdb_url)
    async_couch = couch.AsyncCouch(couch_url=couchdb_url)
    try:
        blocking_couch.create_db()
        tornado.log.app_log.warning(
            "Created new database at {!s}".format(couchdb_url))
    except couch.PreconditionFailed:
        tornado.log.app_log.info(
            "Connected to database at {!s}".format(couchdb_url))
    paths = glob.glob(os.path.join(
        pkg_resources.resource_filename(
            "xcvb", "design"), "*.yaml")) + glob.glob(os.path.join(
                pkg_resources.resource_filename(
                    "xcvb", "design"), "*.json"))
    for path in paths:
        tornado.autoreload.watch(path)
        upload_docs(path, blocking_couch)
    return async_couch
