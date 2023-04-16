
# Bird OSFP Link Database Parser



```sh
> ...

```


## Usage

Pre-requisites: `python3` available via the shell

Setup by cloning, creating a virtual env, and installing the application
```sh
git clone https://github.com/Andrew-Dickinson/bird-ospf-link-db-parser
cd bird-ospf-link-db-parser
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Next, create a `.env` file and fill out the variables
```sh
cp .env_example .env
nano .env
```

then invoke the tool with the CLI command:
```sh

```

## Running the unit tests

Follow the instructions under "Usage" above, to clone a local copy of this application and activate
the virtual environment. Then installing the test dependencies with:
```sh
pip install -e ".[test]"
```

Finally, invoke the test suite using pytest:
```
pytest test/
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
