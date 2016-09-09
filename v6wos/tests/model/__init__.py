import unittest.mock
import io
import json
import couch
import v6wos.model


class BaseTest(v6wos.tests.TestCase):

    def setUp(self):
        super().setUp()
        v6wos.model.Base.couch = None

    @unittest.mock.patch("couch.BlockingCouch")
    @unittest.mock.patch("glob.glob")
    @unittest.mock.patch("builtins.open")
    def test_initialize(self, open, glob, BlockingCouch):
        BlockingCouch.return_value = blocking_couch = unittest.mock.Mock()
        blocking_couch.get_doc.return_value = design = {
            "_id": "test",
        }
        open.return_value = io.StringIO(json.dumps(design))
        design_path = "design.json"
        glob.side_effect = [
            [],
            [design_path],
        ]
        v6wos.model.Base(self.application)
        v6wos.model.Base(self.application)
        BlockingCouch.assert_called_once_with(
            couch_url=self.application.config["couchdb"]["url"])
        blocking_couch.save_doc.assert_called_once_with(design)

    @unittest.mock.patch("couch.BlockingCouch")
    @unittest.mock.patch("glob.glob")
    @unittest.mock.patch("builtins.open")
    def test_initialize_second_pass(self, open, glob, BlockingCouch):
        BlockingCouch.return_value = blocking_couch = unittest.mock.Mock()
        blocking_couch.get_doc.return_value = {
            "_id": "test",
        }
        open.return_value = io.StringIO(json.dumps({
            "_id": "test",
            "_rev": "new",
        }))
        design_path = "design.json"
        glob.side_effect = [
            [],
            [design_path],
        ]
        blocking_couch.create_db.side_effect = couch.PreconditionFailed(
            unittest.mock.Mock())
        blocking_couch.save_doc.side_effect = couch.Conflict(
            unittest.mock.Mock())
        v6wos.model.Base(self.application)
        v6wos.model.Base(self.application)
        BlockingCouch.assert_called_once_with(
            couch_url=self.application.config["couchdb"]["url"])
        blocking_couch.save_doc.assert_called_once_with({
            "_id": "test",
            "_rev": "new",
        })
