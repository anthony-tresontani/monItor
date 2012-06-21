from pyparsing import Word, alphas, nums, restOfLine, Suppress, Group, OneOrMore
from datetime import datetime
from subprocess import Popen, PIPE;

from monitor import Check
from notifier import ConsoleNotifier, EmailNotifier

class CheckJohnsen(Check):
    # Custom parameters
    gap_valid_in_days = 1
    mail_file = "mail.log"

    # Generic parameters
    frequency = 0    # Run everytime
    notifiers = [ConsoleNotifier, EmailNotifier]     # Display the result in the console and send an email
    error_message = "No mail has been send to Johnsen for more than %d day(s)" % gap_valid_in_days    # additional information on failure

    def check(self):
         p1 = Popen(["grep", "carlsberg@johnsen.dk",self.mail_file], stdout=PIPE)
         p2 = Popen(["tail", "-1"], stdin=p1.stdout, stdout=PIPE)
         p1.stdout.close()
         output = p2.communicate()[0]
         date_ = self.get_date_from_log(output)
         now = datetime.now()
         if (now - date_).total_seconds() < self.gap_valid_in_days * 60*60*24:
             return self.OK
         else:
             return self.NOK

    def get_date_from_log(self, log_line):
         time_token = Word(nums, exact=2) + ":"
         time_ = Group(OneOrMore(time_token) + Word(nums, exact=2)).setResultsName("time")
         date_ = Word(alphas, exact=3).setResultsName("month") + Word(nums, max=2).setResultsName("day") + time_
         parser = date_ + Suppress(restOfLine)
         value = parser.searchString(log_line)[0]
         now = datetime.now()
         year_now = now.year
         date_ = value['month'] + " " +  value['day'] + " "  + str(year_now) + " " +  "".join(value['time'])
         date_ = datetime.strptime(date_, "%b %d %Y %H:%M:%S")
         return date_

        
         
         

 
