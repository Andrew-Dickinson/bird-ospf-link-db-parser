from src.bird_parser.parse_bird_output import parse_ospf_state_all


def main():
    with open("example_data/ospf_state_output_apr_16_2023.txt") as input_file:
        link_db = parse_ospf_state_all(input_file.read())
    print(link_db)

if __name__ == "__main__":
    main()