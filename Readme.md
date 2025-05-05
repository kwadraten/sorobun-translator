# A Sorobun Translation Tool

Coded by Python. Use a database (Kuzu or Sqlite) to store words' definition from professional dictionary, which will be provided to model in the context.

## Usage

Require uv to manage python environment. Run "pip install uv" to install it.

```sh
uv sync

mv config_example.json config.json

python main.py -f [inputted text file] -o [outputted text file]
```
