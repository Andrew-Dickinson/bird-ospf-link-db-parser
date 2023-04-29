import json
import os

import pytest
from bird_parser.parse_bird_output import parse_ospf_state_all


def test_with_live_data():
    absolute_path = os.path.dirname(__file__)
    input_fname = os.path.join(
        absolute_path, "artifacts/ospf_state_output_apr_29_2023.txt"
    )
    expected_output_fname = os.path.join(
        absolute_path, "artifacts/expected_output.json"
    )
    with open(input_fname, "r") as input_txt:
        parsed_object = parse_ospf_state_all(input_txt.read())

    with open(expected_output_fname, "r") as output_json:
        expected_output = json.load(output_json)

    parsed_routers = parsed_object["areas"]["0.0.0.0"]["routers"]
    expected_routers = expected_output["areas"]["0.0.0.0"]["routers"]

    for key in parsed_routers:
        assert parsed_routers[key] == expected_routers[key]

    parsed_networks = parsed_object["areas"]["0.0.0.0"]["networks"]
    expected_networks = expected_output["areas"]["0.0.0.0"]["networks"]

    for key in parsed_networks:
        assert parsed_networks[key] == expected_networks[key]
