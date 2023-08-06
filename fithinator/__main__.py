from yaml import parse
from fithinator.fithinator import main_loop

import argparse


def parse_args():
    p = argparse.ArgumentParser(description="FITHINATOR: Status monitor for FITH servers")
    p.add_argument('-c', '--config',
                        type=str,
                        default='/boot/fithinator.yml',
                        help='Location of the config file, default /boot/fithinator.yml'
    )
    parsed_args = p.parse_args()
    return parsed_args

if __name__ == "__main__":
    main_loop(parse_args())
