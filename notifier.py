import smtplib
from email.mime.text import MIMEText

class NoActionNotifier(object):

    def __init__(self, check):
        self.check = check

    def notify(self):pass

class ConsoleNotifier(NoActionNotifier):
    def notify(self):
        print "FAILED"

class EmailNotifier(NoActionNotifier):
    to = "tresontani@gmail.com"
    _from = "monitor@cdk.dk"
    server = 'smtp.gmail.com'
    port = 587
    user = "csv.tresontani@gmail.com"
    password = "csv13csv"

    def notify(self):
        content = "Check %s failed at %s" % (self.check.check_name, self.check.last_exc_time)
        content += "\n" + getattr(self.check, "error_message", "")
        msg = MIMEText(content)
        msg['Subject'] = "Error while performing check %s" % self.check.check_name
        msg['From'] = self._from
        msg['To'] = self.to
        s = smtplib.SMTP(self.server, getattr(self, "port", 25))
        if hasattr(self, "user") and hasattr(self, "password"):
            s.starttls()
            s.login(self.user, self.password)
        s.sendmail(self._from , [self.to], msg.as_string())

        
