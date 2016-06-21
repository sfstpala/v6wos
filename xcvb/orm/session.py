import base64
import uuid
import datetime
import sqlalchemy
import xcvb.orm


class Session(xcvb.orm.Model, xcvb.orm.Base):

    __tablename__ = "sessions"

    session_id = sqlalchemy.Column(
        sqlalchemy.String, primary_key=True)

    session_id.type.length = 22

    @staticmethod
    def random_id(seed=None):
        seed = seed or uuid.uuid4().bytes
        return base64.urlsafe_b64encode(seed).decode().rstrip(
            "=")[:xcvb.orm.session.Session.session_id.type.length]

    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now)

    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)
