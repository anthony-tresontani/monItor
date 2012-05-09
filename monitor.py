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
	    self.nb_run = 0
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
                "nb_run": self.nb_run }

    @property
    def description(self):
        return getattr(self, "desc", "no description")
        
    def run(self):
        self.last_exc_time = datetime.datetime.now()
        self.last_status = self.check()
        self.nb_run += 1
        return self.last_status

    @property
    def check_name(self):
        return getattr(self, "name", self.__class__.__name__)


def get_check_scripts():
    return check_scripts

def get_next_run(date_run=datetime.datetime.now()):
    to_run = set()
    for check_class in get_check_scripts():
        print "Check", check_class
        check_instance = check_class()
        if check_instance.last_exc_time: 
            print "last exec found"
            if check_instance._frequency:
                print "Freq found"
                if check_instance.last_exc_time + datetime.timedelta(minutes=check_instance._frequency) > date_run:
                    print "No ready for next run"
                    continue
            else:
                print "no frequency"
                continue 
        print "Added"
        to_run.add(check_class)
    return to_run


for filepath in glob.glob("scripts/check_*py"):
   file_import = ".".join(filepath.split(".")[:-1]).replace("/", ".")
   importlib.import_module(file_import)

