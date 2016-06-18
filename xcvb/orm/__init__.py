import sqlalchemy.ext.automap


Base = sqlalchemy.ext.automap.automap_base()


class Model:

    engine = None


def prepare(uri):
    if Model.engine is None:
        Model.engine = sqlalchemy.create_engine(uri)
        Base.prepare(Model.engine, reflect=True)
        Base.metadata.create_all(Model.engine)
    return Model.engine
