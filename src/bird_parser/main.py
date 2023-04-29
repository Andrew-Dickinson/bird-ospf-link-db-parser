import json
import os.path
import sys

from bird_parser.parse_bird_output import parse_ospf_state_all

from jsonschema import validate


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} OSPF_LINK_DB_TXT_FILE [--no-validate]")
        sys.exit(2)

    file_name = sys.argv[1]
    if file_name == "-":
        input_str = sys.stdin.read()
    else:
        with open(file_name) as input_file:
            input_str = input_file.read()

    link_db = parse_ospf_state_all(input_str)

    if len(sys.argv) < 3 or sys.argv[2] != "--no-validate":
        schema_fname = os.path.join(os.path.dirname(__file__), "output_schema.json")
        with open(schema_fname, "r") as output_schema:
            validate(link_db, json.load(output_schema))

    print(json.dumps(link_db))


if __name__ == "__main__":
    main()
