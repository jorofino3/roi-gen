import docopt

"""
A simple example of using docopt to create a command-line application.

Usage:
  my_program.py command <argument>
  my_program.py (-h | --help)

Options:
  -h --help     Show this screen.

Examples:
  my_program.py greet World

"""
def main():
    arguments = docopt(__doc__)

    command = arguments['command']
    argument = arguments['<argument>']

    if command == 'greet':
        print(f'Hello, {argument}!')

if __name__ == '__main__':
    main()
