import pytest
from bird_parser.parse_bird_output import parse_ospf_state_all

SIMPLE_INPUT = """BIRD 1.6.8 ready.

area 0.0.0.0

	router 10.10.10.10
		distance 61
		network 10.70.76.0/24 metric 10
		external 10.10.10.10/32 metric 1
		external 10.10.10.11/32 metric 1

	router 10.68.29.50
		distance 51
		router 10.69.7.31 metric 10
		stubnet 10.69.29.50/32 metric 0
		stubnet 10.68.29.50/32 metric 0
		external 10.70.174.0/24 metric 20

"""


def test_parse_simple():
    parsed_object = parse_ospf_state_all(SIMPLE_INPUT)

    assert parsed_object == {
        "areas": {
            "0.0.0.0": {
                "networks": {},
                "routers": {
                    "10.10.10.10": {
                        "links": {
                            "network": [{"id": "10.70.76.0/24", "metric": 10}],
                            "external": [
                                {"id": "10.10.10.10/32", "metric": 1},
                                {"id": "10.10.10.11/32", "metric": 1},
                            ],
                        }
                    },
                    "10.68.29.50": {
                        "links": {
                            "router": [{"id": "10.69.7.31", "metric": 10}],
                            "stubnet": [
                                {"id": "10.69.29.50/32", "metric": 0},
                                {"id": "10.68.29.50/32", "metric": 0},
                            ],
                            "external": [
                                {"id": "10.70.174.0/24", "metric": 20},
                            ],
                        }
                    },
                },
            }
        }
    }
