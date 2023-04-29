import re
from typing import List


def get_indentation_level(line: str):
    return len(line) - len(line.lstrip("\t"))


def create_key_from_path(dictionary: dict, path: List[str]):
    nested_dict = dictionary
    for item in path:
        if item not in nested_dict:
            nested_dict[item] = {}
        nested_dict = nested_dict[item]


def set_value_by_path(dictionary: dict, path: List[str], value=None):
    nested_dict = dictionary
    for item in path[:-1]:
        nested_dict = nested_dict[item]

    nested_dict[path[-1]] = value


def get_value_by_path(dictionary: dict, path: List[str]):
    nested_dict = dictionary
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


def parse_ospf_state_all(ospf_state_str: str):
    lines = [line.rstrip() for line in ospf_state_str.split("\n") if len(line) > 0]
    lines.append("")

    assert re.match(r"BIRD.+ready\.", lines[0])

    output = {}

    previous_indentation_level = -1
    path_stack = []

    for line in lines[1:]:
        line_parts = line.split()
        indentation_level = get_indentation_level(line)

        if line_parts and (
            line_parts[0] == "distance" or line_parts[0] == "unreachable"
        ):
            # Ignore distance/reachability from our local perspective as it's not meaningful to
            # understanding the global state of the system
            continue

        level_diff = indentation_level - previous_indentation_level
        if level_diff > 0:
            assert (
                level_diff == 1
            ), "Indenting by more than one tab at a time is not supported"
            create_key_from_path(output, path_stack)
            if indentation_level == 1:
                create_key_from_path(output, path_stack + ["networks"])
                create_key_from_path(output, path_stack + ["routers"])
            if indentation_level == 2:
                if path_stack[2] == "routers":
                    default_object = {
                        "links": {
                            "network": [],
                            "external": [],
                            "router": [],
                            "stubnet": [],
                        }
                    }
                elif path_stack[2] == "networks":
                    default_object = {
                        "dr": "",
                        "routers": [],
                    }
                else:
                    raise ValueError(f"Invalid object: '{path_stack[2]}' found!")

                set_value_by_path(
                    output,
                    path_stack,
                    default_object,
                )
        else:
            if level_diff < 0:
                if previous_indentation_level == 2:
                    if path_stack[2] == "routers":
                        link_lists = get_value_by_path(
                            output, path_stack[:-2] + ["links"]
                        )
                        lists_to_remove = [
                            link_type
                            for link_type, links in link_lists.items()
                            if len(links) == 0
                        ]
                        for link_type in lists_to_remove:
                            del link_lists[link_type]
            for i in range(max(-level_diff, 0) + 1):
                path_stack.pop()
                path_stack.pop()

        if line_parts:
            path_stack.append(line_parts[0] + "s")
            path_stack.append(line_parts[1])

            if indentation_level == 2:
                if path_stack[2] == "routers":
                    link_type = line_parts[0]
                    link_list_for_type = get_value_by_path(
                        output, path_stack[:-2] + ["links", link_type]
                    )
                    link_list_for_type.append(parse_router_link(line_parts))
                elif path_stack[2] == "networks":
                    network = get_value_by_path(output, path_stack[:-2])
                    if line_parts[0] == "dr":
                        network["dr"] = line_parts[1]
                    elif line_parts[0] == "router":
                        network["routers"].append(line_parts[1])
                    else:
                        raise ValueError(f"Invalid line: {line}")

        previous_indentation_level = indentation_level

    return output
