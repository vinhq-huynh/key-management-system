from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

"""Small utility function whose only job is to manage the connection to the database."""

db_url = "postgresql+psycopg2://postgres:1506@localhost:5432/postgres"

# Create the database engine that we will use for all of our work.  This does not actually connect
# just yet, it is more like a connection prototype that we actually fire up when we create a session.
engine = create_engine(db_url, pool_size=5, pool_recycle=3600, echo=False)

# Create a session factory using the engine that we just defined.
session_factory = sessionmaker(bind=engine)

# I am told that this next line contributes to making the code thread safe since the
# scoped_session returns the same Session every time it's called for any given thread.
# I personally don't expect to try to run concurrent threads from Python using
# SQLAlchemy anytime soon, but if I do, I'll be ready!
Session = scoped_session(session_factory)
