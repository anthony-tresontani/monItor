MonItor is a command line tools with the purpose of simplyfing business check script execution for your application.

If you want to check than at least one email has been sent to a customer, an order has been placed, 
a new record has been added in the DB, etc... , monitor will run your check script on a regular basis.
If that fail, he will notify you via any channel.

Specify your jobs through a python class.

class CheckOK(Check):
    frequency = 5
    notifiers = [ConsoleNotifier]

    def check(self):
        return Check.OK

Every 5 minutes, this check script will run and ensure that... it's OK.

