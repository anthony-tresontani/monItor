class NoActionNotifier(object):

    def __init__(self, check):
        self.check = check

    def notify(self):pass

class ConsoleNotifier(NoActionNotifier):
    def notify(self):
        print "Here"
