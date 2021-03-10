import cmd
import argparse

# setup for command parsing
parser = argparse.ArgumentParser()
parser.add_argument("hero")
args = parser.parse_args()

if __name__ == '__main__':
    cmd.find_associated_heroes(args.hero)
    print('complete')
