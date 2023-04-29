
# Bird OSFP Link Database Parser

Parses the output of the BIRD Routing Daemon's `birdc show ospf state` command into a machine-readable JSON string.

```sh
> birdc show ospf state all | parse-bird-link-db - | jq | less
{
  "areas": {
    "0.0.0.0": {
      "routers": {
        "10.68.29.50": {
          "links": {
            "router": [
              {
                "id": "10.69.7.31",
                "metric": 10
              }
            ],
            "stubnet": [
              {
                "id": "10.69.29.50/32",
                "metric": 0
              },
              {
                "id": "10.68.29.50/32",
                "metric": 0
              }
            ],
            "external": [
              {
                "id": "10.70.174.0/24",
                "metric": 20
              }
            ]
          }
        },
        "10.68.73.125": {
          "links": {
            "router": [
              {
                "id": "10.69.73.25",
                "metric": 10
              },
              {
                "id": "10.69.52.83",
                "metric": 30
              },
              {
                "id": "10.69.73.25",
                "metric": 30
              }
            ],
            "stubnet": [
              {
                "id": "10.69.73.125/32",
                "metric": 0
              },
              {
                "id": "10.68.73.125/32",
                "metric": 0
              }
            ]
          }
        },
        ...
      }
    }
  }
}
```

## Output Format

The output format is detailed using [JSON Schema](https://json-schema.org/) in `src/bird_parser/output_schema.json`

## Usage

Pre-requisites: `python3` available via the shell

First, install the CLI via pip:
```shell
pip install bird-ospf-link-db-parser
```

then invoke the tool with the CLI command:
```shell
birdc show ospf state all | parse-bird-link-db -
```

But you probably want to use `jq` and `less` to make this output a bit more managable:
```shell
sudo apt update && sudo apt install jq less
birdc show ospf state all | parse-bird-link-db - | jq | less
```

## Dev Setup

Pre-requisites: `python3` available via the shell

Setup by cloning, creating a virtual env, and installing the application
```sh
git clone https://github.com/Andrew-Dickinson/bird-ospf-link-db-parser
cd bird-ospf-link-db-parser
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

then invoke the tool with the CLI command:
```sh
birdc show ospf link state all > parse-bird-link-db -
```

## Running the unit tests

Follow the instructions under "Dev Setup" above, to clone a local copy of this application and activate
the virtual environment. Then installing the test dependencies with:
```sh
pip install -e ".[test,dev]"
```

Finally, invoke the test suite using pytest:
```
pytest test/
```

## Building to PyPi

Follow the instructions above to clone a local copy of this application, activate
the virtual environment, and run the tests.

Then, build & upload the application with
```
rm -rf dist/*
python -m build .
twine upload dist/*
```

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments
 * [Best-README-Template](https://github.com/othneildrew/Best-README-Template/)
