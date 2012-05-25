import datetime
import glob
import importlib

check_scripts = set([])

class CheckMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        cls = type.__new__(meta, classname, bases, classDict)
        if not classname == "Check":
            check_scripts.add(cls)
        return cls


class Check(object):
    __metaclass__ = CheckMetaClass
    OK, NOK = "OK", "NOK"

    _shared_dict = None
    def __init__(self):
        if not self.__class__._shared_dict:
	    self.last_exc_time = None
	    self.last_status = None
	    self._frequency = getattr(self, "frequency", None)
            self.__class__._shared_dict = self.__dict__
        else:
            self.__dict__ = self.__class__._shared_dict

    def set_frequency(self, nb_minutes):
        self._frequency = nb_minutes

    @property
    def last_exc(self):
        return {"name":self.check_name,
                "time": self.last_exc_time,
                "status": self.last_status,
                }

    @property
    def description(self):
        return getattr(self, "desc", "no description")
        
    def save_in_db(self):
        session = Session()
        if session.query(Run).filter_by(name=self.check_name).count():
           run = session.query(Run).filter_by(name=self.check_name).one()
           run.last_exec_time = self.last_exc_time 
           run.status = self.last_status
           run.nb_run = run.nb_run + 1
        else:
           inst = Run(name=self.check_name, last_exec_time=self.last_exc_time, status=self.last_status, nb_run=1)
           session.add(inst)
        session.commit()

    def run(self):
        self.last_exc_time = datetime.datetime.now()
        self.last_status = self.check()
        self.save_in_db()
        return self.last_status

    @property
    def check_name(self):
        return getattr(self, "name", self.__class__.__name__)


def get_check_scripts():
    return check_scripts

def get_next_run(date_run=datetime.datetime.now()):
    to_run = set()
    for check_class in get_check_scripts():
        check_instance = check_class()
        if check_instance.last_exc_time: 
            if check_instance._frequency:
                if check_instance.last_exc_time + datetime.timedelta(minutes=check_instance._frequency) > date_run:
                    continue
            else:
                continue 
        to_run.add(check_class)
    return to_run

# automatic script import
for filepath in glob.glob("scripts/check_*py"):
   file_import = ".".join(filepath.split(".")[:-1]).replace("/", ".")
   importlib.import_module(file_import)

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///test_db', echo=True)
Session = sessionmaker(bind=engine)

class Run(Base):
     __tablename__ = 'runs'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     nb_run = Column(Integer)
     last_exec_time = Column(DateTime)
     status = Column(String)

     def __init__(self, name, last_exec_time, status, nb_run):
         self.name = name
         self.last_exec_time = last_exec_time
         self.status = status
         self.nb_run = nb_run
 

     def __repr__(self):
        return "<Run('%s','%s', '%s')>" % (self.name, self.status, self.last_exec_time)
