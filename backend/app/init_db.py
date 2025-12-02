from .db import Base, engine
from . import models  # ensure models are imported so Base knows about them


def init_db():
    # This will create tables if they do not already exist
    Base.metadata.create_all(bind=engine)
