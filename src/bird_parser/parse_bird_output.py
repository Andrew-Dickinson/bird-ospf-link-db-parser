import re

def get_indentation_level(line: str):
    return len(line) - len(line.lstrip("\t"))


def parse_ospf_state_all(ospf_state_str: str):
    lines = [line.rstrip() for line in ospf_state_str.split("\n") if len(line) > 0]

    assert re.match(r"BIRD.+ready\.", lines[0])

    areas = {}

    current_area_id = None
    current_area = {}

    current_item_id = None
    current_item = {}
    current_item_type = None

    for line in lines[1:]:
        line_parts = line.split()
        indentation_level = get_indentation_level(line)

        if indentation_level == 0:
            assert len(line_parts) == 2
            assert line_parts[0] == "area"

            if current_area_id is not None:
                areas[current_area_id] = current_area

            current_area = {"routers": {}, "networks": {}}
            current_area_id = line_parts[1]
        elif indentation_level == 1:
            assert len(line_parts) == 2
            assert line_parts[0] in ["router", "network"]

            if current_item_id is not None:
                current_area[f"{current_item_type}s"][current_item_id] = current_item

            current_item_type = line_parts[0]
            current_item = {"links": {}} if current_item_type == "router" else {}
            current_item_id = line_parts[1]
        elif indentation_level == 2:
            if line_parts[0] == "distance":
                # Ignore distance from our local perspective as it's not meaningful to
                # understanding the global state of the system
                continue

            if current_item_type == "router":
                if line_parts[0] == "external":
                    assert len(line_parts) == 4 or len(line_parts) == 6
                else:
                    assert len(line_parts) == 4

                resource_name = line_parts[0]
                assert resource_name in ["router", "stubnet", "external", "network"]

                if resource_name not in current_item["links"]:
                    current_item["links"][resource_name] = []

                assert line_parts[2] in ["metric", "metric2"]
                resource = {"id": line_parts[1], line_parts[2]: int(line_parts[3])}

                if len(line_parts) == 6:
                    assert line_parts[4] == "via"
                    resource[line_parts[4]] = line_parts[5]

                current_item["links"][resource_name].append(resource)
            elif current_item_type == "network":
                assert len(line_parts) == 2

                assert line_parts[0] in ["dr", "router"]
                if line_parts[0] == "dr":
                    current_item["dr"] = line_parts[1]
                elif line_parts[0] == "router":
                    if "routers" not in current_item:
                        current_item["routers"] = []
                    current_item["routers"].append(line_parts[1])

    current_area[f"{current_item_type}s"][current_item_id] = current_item
    areas[current_area_id] = current_area
    return {"areas": areas}