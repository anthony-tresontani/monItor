import collections
import datetime
import glob
import importlib

from sqlalchemy import Column, Integer, String, DateTime, create_engine

from monitor.config import Session, Base, SCRIPTS_FOLDER
from monitor.notifier import NoActionNotifier, ConsoleNotifier

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
            session = Session()
            if session.query(Run).filter_by(name=self.check_name).count():
                db_run = session.query(Run).filter_by(name=self.check_name).one()
                self.last_exc_time = db_run.last_exc_time
                self.last_status = db_run.status
            else:
	        self.last_exc_time = None
	        self.last_status = None
            self._notifiers = [notifier_class(self) for notifier_class in getattr(self, "notifiers", [NoActionNotifier])]
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
           run.last_exc_time = self.last_exc_time 
           run.status = self.last_status
           run.nb_run = run.nb_run + 1
        else:
           inst = Run(name=self.check_name, last_exc_time=self.last_exc_time, status=self.last_status, nb_run=1)
           session.add(inst)
        session.commit()

    def notify(self):
        for notifier in self._notifiers:
            notifier.notify()

    def run(self):
        self.previous_status = self.last_status
        self.last_exc_time = datetime.datetime.now()
        self.last_status = self.check()
        self.save_in_db()

        if self.previous_status == self.OK and self.last_status != self.OK:
            self.notify()
        return self.last_status

    @property
    def check_name(self):
        return getattr(self, "name", self.__class__.__name__)

def get_next_run(scripts_folder=SCRIPTS_FOLDER, date_run=datetime.datetime.now()):
    to_run = set()
    for check_class in get_check_scripts(scripts_folder):
        check_instance = check_class()
        if check_instance.last_exc_time: 
            if check_instance._frequency is not None:
                if check_instance.last_exc_time + datetime.timedelta(minutes=check_instance._frequency) > date_run:
                    continue
            else:
                continue 
        to_run.add(check_class)
    return to_run

# automatic script import
def import_scripts(scripts_folder):
    if isinstance(scripts_folder, str):
        scripts_folder = [scripts_folder]
    for path in scripts_folder:
        for filepath in glob.glob(path):
            file_import = ".".join(filepath.split(".")[:-1]).replace("/", ".")
            importlib.import_module(file_import)


def get_check_scripts(script_folder):
    import_scripts(script_folder)
    return check_scripts


class Run(Base):
     __tablename__ = 'runs'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     nb_run = Column(Integer)
     last_exc_time = Column(DateTime)
     status = Column(String)

     def __init__(self, name, last_exc_time, status, nb_run):
         self.name = name
         self.last_exc_time = last_exc_time
         self.status = status
         self.nb_run = nb_run
 

     def __repr__(self):
        return "<Run('%s','%s', '%s')>" % (self.name, self.status, self.last_exc_time)
