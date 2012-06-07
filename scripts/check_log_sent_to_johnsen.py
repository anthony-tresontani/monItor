from monitor import Check

class CheckOK(Check):
    frequency = 0

    def check(self):
        return Check.OK

class CheckJohnsen(Check):
    frequency = 5

    def check(self):
        return Check.NOK
 
