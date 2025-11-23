import argparse
import json

configs = json.load(open("configs/args_config.json", "r"))
parser = argparse.ArgumentParser(description=configs["description"])

for arg in configs["arguments"]:
    parser.add_argument(
        arg,
        type=eval(configs["arguments"][arg]["type"]),
        default=configs["arguments"][arg]["default"],
        help=configs["arguments"][arg]["help"]
    )
