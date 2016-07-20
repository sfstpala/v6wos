import datetime
import sqlalchemy
import xcvb.orm


class Session(xcvb.orm.Model, xcvb.orm.Base):

    __tablename__ = "sessions"

    session_id = sqlalchemy.Column(
        sqlalchemy.String(length=26), primary_key=True)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        default=datetime.datetime.utcnow)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)
