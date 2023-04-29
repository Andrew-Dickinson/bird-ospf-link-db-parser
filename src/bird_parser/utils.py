from typing import List, Any


class OutputDict(dict):
    def create_key_from_path(self, path: List[str]):
        nested_dict = self
        for item in path:
            if item not in nested_dict:
                nested_dict[item] = {}
            nested_dict = nested_dict[item]

    def set_value_by_path(self, path: List[str], value: Any):
        nested_dict = self
        for item in path[:-1]:
            nested_dict = nested_dict[item]

        nested_dict[path[-1]] = value

    def get_value_by_path(self, path: List[str]):
        nested_dict = self
        for item in path:
            nested_dict = nested_dict[item]

        return nested_dict


def parse_router_link(line_parts: List[str]):
    assert line_parts[2] in ["metric", "metric2"]
    link = {"id": line_parts[1], line_parts[2]: int(line_parts[3])}

    if len(line_parts) == 6:
        assert line_parts[4] == "via"
        link["via"] = line_parts[5]

    return link


def get_default_value_for_resource(resource_name: str):
    if resource_name == "area":
        return {
            "networks": {},
            "routers": {},
        }
    elif resource_name == "router":
        return {
            "links": {
                "network": [],
                "external": [],
                "router": [],
                "stubnet": [],
            }
        }
    elif resource_name == "network":
        return {
            "dr": "",
            "routers": [],
        }
    else:
        raise NotImplementedError(
            f"No default value found for resource: {resource_name}"
        )
