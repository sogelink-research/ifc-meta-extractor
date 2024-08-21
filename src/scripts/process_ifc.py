import json
import argparse
from ifc_metadata_extractor import metadata
from typing import Any, Dict


def save_json(data: Dict[str, Any], output_file: str) -> None:
    """
    Save the data to a JSON file.

    Args:
        data (Dict[str, Any]): The data to save in JSON format.
        output_file (str): The path to the output JSON file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=2)
        print(f"Data successfully saved to {output_file}")
    except IOError as e:
        print(f"Failed to save data to {output_file}: {e}")


def get_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Process IFC file to JSON")
    parser.add_argument('--input', required=True,
                        help="Path to the input IFC file.")
    parser.add_argument('--output', required=True,
                        help="Path to the output JSON file.")
    return parser.parse_args()


def main() -> None:
    """
    Main function to process the IFC file and save metadata to JSON.
    """
    args = get_args()
    try:
        extractor = metadata.IFCMetadataExtractor(args.input)
        data = extractor.get_metadata()
        save_json(data, args.output)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
