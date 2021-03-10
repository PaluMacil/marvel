import cmd
import argparse

# setup for command parsing
parser = argparse.ArgumentParser()
parser.add_argument("hero")
parser.add_argument("-a", "--associates", help="gathers information on the hero's associates",
                    action="store_true")
parser.add_argument("-v", "--verbose", help="prints detailed information about resource retrieval",
                    action="store_true")
args = parser.parse_args()

if __name__ == '__main__':
    if args.associates:
        result = cmd.find_associated_heroes(args.hero, args.verbose)
    else:
        result = cmd.find_hero(args.hero, args.verbose)

    print('complete')
