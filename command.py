from monitor import get_check_scripts, Check, get_next_run
from clint.textui import colored, puts

def main(list, all, action=None): 
    if list:
        print_action_list()
    elif all:
        do_all()
    elif action:
        do_check(action)
    else:
        puts(colored.red("You should provide an action"))


def run_action(action, extra=""):
    result = action.run()
    color = colored.green if result == Check.OK else colored.red
    if result:
        puts(color(extra + result))

def do_all():
    next_runs = get_next_run()
    for index, action in enumerate(next_runs):
        action = action()
        run_action(action, extra="%d. %s - " % (index +1, action.check_name))
    if not next_runs:
        puts(colored.green("No check ready to be performed"))

def do_check(action):
    action = filter(lambda check: check().check_name == action, get_check_scripts()) 
    if not action:
        puts(colored.red("This action doesn't exist"))
    else:
        run_action(action[0]())


main.__annotations__ = {
    "list" : ("list the available checksq", "flag", "l"),
    "all" : ("Run all check according to their frequency", "flag", "a"),
    }


def print_action_list():
    for check_class in get_check_scripts():
        check = check_class()
        print "{check_name} - {description}".format(check_name=check.check_name, description=check.description)

 
if __name__ == '__main__':
    import plac; plac.call(main)

