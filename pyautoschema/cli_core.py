import argparse
import os

from pyautoschema.core import schemaCreatorJson, schemaCreatorXml

def main():
    parser = argparse.ArgumentParser(description="Convert a dictionary or JSON file into Pydantic model.")
    parser.add_argument('--input', '-i', required=True, help='Path to a .json or .xml file')
    parser.add_argument('--output', '-o', default='schemas.py', help='Path to output .py file')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file '{args.input}' does not exist.")
        return

    try:
        if args.input.endswith(".json"):
            schemaCreatorJson(args.input, output=args.output)
        elif args.input.endswith(".xml"):
            schemaCreatorXml(args.input, output=args.output)
        else:
            print("Unsupported file format. Use .json or .xml")
            return
    except Exception as e:
        print(f"Error processing input file: {e}")
        return

if __name__ == "__main__":
    main()