# ifc-meta-extractor

Extract metadata from an IFC file and save it to a JSON file.

## Dev

```sh
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Running ifc-meta-extractor

Extract metadata from an IFC file and save to a JSON file.

```sh
usage: ifc-meta-extractor [-h] -i INPUT -o OUTPUT

Process Extract IFC metadata to JSON

options:
  -h, --help                    Show this help message and exit
  -i INPUT, --input INPUT       Path to the input IFC file.
  -o OUTPUT, --output OUTPUT    Path to the output JSON file.
```

Example

```sh
ifc-meta-extractor -i ./data/my_file.ifc -o ./output/my_file_metadata.json
```
