from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

# Note - The "connect string" shown in db_connection only goes so far as to specify the
# database name, which is 'postgres' in this case.  Be sure to create the proper schema
# in the PostgreSQL postgres database BEFORE trying to run this code, SQLAlchemy will not
# create the schema for you.

# Base is a class that we create that will be the supertype of each of our classes that
# we map to a database table.  In making our classes subtypes of Base, we inherit a number
# of useful utilities that make it much easier to access the database in Python.
Base = declarative_base(metadata=MetaData(schema="323 Phase 2"))

# Think of metadata as a crib sheet that SQLAlchemy uses to keep track of all the
# database objects that you create along the way in your application.  We could have called
# the metadata object anything, but you might as well keep it simple.
metadata = Base.metadata
