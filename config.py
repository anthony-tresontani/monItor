from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from notifier import ConsoleNotifier

Base = declarative_base()
engine = create_engine('sqlite:///test_db', echo=False)
Session = sessionmaker(bind=engine)


SCRIPTS_FOLDER = ("scripts/check_*py",)
