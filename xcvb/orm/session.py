import sqlalchemy
import xcvb.orm


class Session(xcvb.orm.Model, xcvb.orm.Base):

    __tablename__ = "sessions"

    session_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
