from .db import Base, engine
from . import models  # noqa: F401  # make sure models are imported


def init_db():
    # This should emit CREATE TABLE statements (because echo=True in engine)
    Base.metadata.create_all(bind=engine)
