from monitor.scheduler import Check
from monitor.notifier import ConsoleNotifier

class CheckOK(Check):
    frequency = 0
    notifiers = [ConsoleNotifier]

    def check(self):
        return Check.OK

class CheckJohnsen(Check):
    frequency = 5

    def check(self):
        return Check.NOK
 
