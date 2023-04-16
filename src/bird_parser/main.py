import json
import sys

from bird_parser.parse_bird_output import parse_ospf_state_all


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} OSPF_LINK_DB_TXT_FILE")
        sys.exit(2)

    file_name = sys.argv[1]
    if file_name == "-":
        input_str = sys.stdin.read()
    else:
        with open(file_name) as input_file:
            input_str = input_file.read()

    link_db = parse_ospf_state_all(input_str)
    print(json.dumps(link_db))


if __name__ == "__main__":
    main()