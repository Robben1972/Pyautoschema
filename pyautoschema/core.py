from dateutil.parser import parse as dt_parse
from uuid import UUID
import re

def detect_smart_type(value):
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, dict):
        return "dict"
    if isinstance(value, list):
        return "list"
    if isinstance(value, str):
        try:
            dt_parse(value)
            return "datetime"
        except:
            pass
        try:
            UUID(value)
            return "UUID"
        except:
            pass
        if re.match(r"[^@]+@[^@]+\.[^@]+", value):
            return "EmailStr"
        if re.match(r"https?://[^\s]+", value):
            return "HttpUrl"
        if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            return "date"
        if re.match(r"^\d{2}:\d{2}:\d{2}$", value):
            return "time"
    return "str"

def schemaCreator(code: dict, output: str = 'schemas.py') -> None:
    def pascal_case(s): return ''.join(word.capitalize() for word in s.split('_'))

    def wrapper(code_value: dict, name: str = 'InferredModel'):
        schemas = {name: {}}
        use_list = use_union = use_any = False
        detected_types = set()

        for key, value in code_value.items():
            if isinstance(value, dict):
                class_name = pascal_case(key)
                schemas[name][key] = class_name
                nested_schema, l, u, a, types = wrapper(value, class_name)
                schemas.update(nested_schema)
                use_list |= l
                use_union |= u
                use_any |= a
                detected_types.update(types)

            elif isinstance(value, list):
                types = list(set(detect_smart_type(item) for item in value))
                detected_types.update(types)
                if len(types) == 1:
                    item_type = types[0]
                    schemas[name][key] = f"List[{item_type}]"
                    use_list = True
                elif len(types) == 2:
                    item_types = ', '.join(types)
                    schemas[name][key] = f"List[Union[{item_types}]]"
                    use_list = use_union = True
                else:
                    schemas[name][key] = "List[Any]"
                    use_list = use_any = True
            else:
                field_type = detect_smart_type(value)
                schemas[name][key] = field_type
                detected_types.add(field_type)

        return schemas, use_list, use_union, use_any, detected_types

    schemas_dict, has_list, has_union, has_any, detected_types = wrapper(code)

    typing_imports = ", ".join([imp for imp in ("List", "Union", "Any") if locals()[f"has_{imp.lower()}"]])
    pydantic_imports = set()
    other_imports = set()

    for dtype in detected_types:
        if dtype in {"EmailStr", "HttpUrl"}:
            pydantic_imports.add(dtype)
        elif dtype in {"datetime", "date", "time"}:
            other_imports.add("datetime")
        elif dtype == "UUID":
            other_imports.add("uuid")
        elif dtype == "Decimal":
            other_imports.add("decimal")

    with open(output, 'w') as f:
        if typing_imports:
            f.write(f"from typing import {typing_imports}\n")
        if pydantic_imports:
            f.write(f"from pydantic import BaseModel, {', '.join(pydantic_imports)}\n")
        else:
            f.write("from pydantic import BaseModel\n")
        if "datetime" in other_imports:
            f.write("from datetime import datetime\n")
        if "uuid" in other_imports:
            f.write("from uuid import UUID\n")
        if "decimal" in other_imports:
            f.write("from decimal import Decimal\n")
        f.write("\n")

        for model_name, model_fields in reversed(list(schemas_dict.items())):
            f.write(f"class {model_name}(BaseModel):\n")
            if model_fields == {}:
                f.write("    pass\n")
            else:
                for field_name, field_type in model_fields.items():
                    f.write(f"    {field_name}: {field_type}\n")
            f.write("\n")

def schemaCreatorJson(path: str, output: str = 'schemas.py') -> None:
    import json
    with open(path, 'r') as f:
        data = json.load(f)
    schemaCreator(data, output)

def schemaCreatorXml(path: str, output: str = 'schemas.py') -> None:
    import xmltodict

    def convert_values(data):
        if isinstance(data, dict):
            return {key: convert_values(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [convert_values(item) for item in data]
        else:
            if isinstance(data, str):
                if data.isdigit():
                    return int(data)
                elif data.lower() in ('true', 'false'):
                    return data.lower() == 'true'
            return data

    with open(path, 'r') as f:
        data = xmltodict.parse(f.read())
        processed_data = convert_values(data)

    schemaCreator(processed_data, output)