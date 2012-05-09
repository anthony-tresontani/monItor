from monitor import Check

class CheckOK(Check):
    def check(self):
        return Check.OK

class CheckJohnsen(Check):
    def check(self):
        return Check.NOK
 
