import re

from bird_parser.utils import (
    OutputDict,
    parse_router_link,
    get_default_value_for_resource,
)


def get_indentation_level(line: str):
    return len(line) - len(line.lstrip("\t"))


def parse_ospf_state_all(ospf_state_str: str):
    parser = StackParser(ospf_state_str)
    return parser.parse()


class StackParser:
    def __init__(self, ospf_state_str: str):
        self.output = OutputDict({})
        self.previous_indentation_level = 0
        self.path_stack = ["", ""]

        self.lines = [
            line.rstrip() for line in ospf_state_str.split("\n") if len(line) > 0
        ]
        self.lines.append("")

    def parse(self):
        assert re.match(r"BIRD.+ready\.", self.lines[0])

        for line in self.lines[1:]:
            self.parse_line(line)

        return self.output

    def parse_line(self, line: str):
        line_parts = line.split()
        indentation_level = get_indentation_level(line)

        if line_parts and (
            line_parts[0] == "distance" or line_parts[0] == "unreachable"
        ):
            # Ignore distance/reachability from our local perspective as it's not meaningful to
            # understanding the global state of the system
            return

        level_diff = indentation_level - self.previous_indentation_level
        if level_diff > 0:
            assert (
                level_diff == 1
            ), "Indenting by more than one tab at a time is not supported"
            self.handle_enter_resource(self.path_stack[-2][:-1])
        else:
            if level_diff < 0:
                self.handle_exit_resource(self.path_stack[2][:-1])

                # Account for the un-indent
                for i in range(abs(level_diff)):
                    self.path_stack.pop()
                    self.path_stack.pop()

            # Remove the previous "current level", since it will be replaced below
            self.path_stack.pop()
            self.path_stack.pop()

        if line_parts:
            self.path_stack.append(line_parts[0] + "s")
            self.path_stack.append(line_parts[1])

            current_container_name = (
                self.path_stack[-4][:-1] if len(self.path_stack) > 2 else None
            )
            if current_container_name == "router":
                link_type = line_parts[0]
                link_list_for_type = self.output.get_value_by_path(
                    self.path_stack[:-2] + ["links", link_type]
                )
                link_list_for_type.append(parse_router_link(line_parts))
            elif current_container_name == "network":
                network = self.output.get_value_by_path(self.path_stack[:-2])
                if line_parts[0] == "dr":
                    network["dr"] = line_parts[1]
                elif line_parts[0] == "router":
                    network["routers"].append(line_parts[1])
                else:
                    raise ValueError(f"Invalid line: {line}")

        self.previous_indentation_level = indentation_level

    def handle_enter_resource(self, resource_name: str):
        # Create an output key to track the new deeper indentation level
        self.output.create_key_from_path(self.path_stack)

        # If we are entering an area, router, or network, create the appropriate default containers
        if resource_name in ["area", "router", "network"]:
            self.output.set_value_by_path(
                self.path_stack,
                get_default_value_for_resource(resource_name),
            )

    def handle_exit_resource(self, resource_name: str):
        # If we are exiting a router, clean up the empty link lists so they don't appear in the output
        if resource_name == "router":
            link_lists = self.output.get_value_by_path(self.path_stack[:-2] + ["links"])
            lists_to_remove = [
                link_type for link_type, links in link_lists.items() if len(links) == 0
            ]
            for link_type in lists_to_remove:
                del link_lists[link_type]
