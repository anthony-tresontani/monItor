from monitor import get_check_scripts, Check
from clint.textui import colored, puts

def main(list, action=None): 
    if list:
        print_action_list()
    else:
        do_check(action)


def do_check(action):
    action = filter(lambda check: check().check_name == action, get_check_scripts()) 
    if not action:
        puts(colored.red("This action doesn't exist"))
    else:
        result = action[0]().run()
        color = colored.green if result == Check.OK else colored.red
        puts(color(result))


main.__annotations__ = {
    "list" : ("list the available checksq", "flag", "l"),
    }


def print_action_list():
    for check_class in get_check_scripts():
        check = check_class()
        print "{check_name} - {description}".format(check_name=check.check_name, description=check.description)

 
if __name__ == '__main__':
    import plac; plac.call(main)

