import argparse
from configs import DESCRIPTION, ARGUMENTS

parser = argparse.ArgumentParser(description=DESCRIPTION)

for arg in ARGUMENTS:
    parser.add_argument(
        arg,
        type=eval(ARGUMENTS[arg]["type"]),
        default=ARGUMENTS[arg]["default"],
        help=ARGUMENTS[arg]["help"]
    )
