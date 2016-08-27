import unittest.mock
import io
import json
import couch
import xcvb.model


class BaseTest(xcvb.tests.TestCase):

    def setUp(self):
        super().setUp()
        xcvb.model.Base.couch = None

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
        xcvb.model.Base(self.application)
        xcvb.model.Base(self.application)
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
        xcvb.model.Base(self.application)
        xcvb.model.Base(self.application)
        BlockingCouch.assert_called_once_with(
            couch_url=self.application.config["couchdb"]["url"])
        blocking_couch.save_doc.assert_called_once_with({
            "_id": "test",
            "_rev": "new",
        })
