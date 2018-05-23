from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine

from sqlalchemy import Column, Integer, String

Base = declarative_base()



engine = create_engine("sqlite3:///config.db")