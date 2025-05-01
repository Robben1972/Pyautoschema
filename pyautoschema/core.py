def infer_schema(code: dict, output: str = 'schemas.py') -> None:
    def pascal_case(s): return ''.join(word.capitalize() for word in s.split('_'))

    def wrapper(code_value: dict, name: str = 'InferredModel'):
        schemas = {name: {}}
        use_list = use_union = use_any = False

        for key, value in code_value.items():
            if isinstance(value, dict):
                class_name = pascal_case(key)
                schemas[name][key] = class_name
                nested_schema, l, u, a = wrapper(value, class_name)
                schemas.update(nested_schema)
                use_list |= l
                use_union |= u
                use_any |= a

            elif isinstance(value, list):
                types = list(set(type(item) for item in value))
                if len(types) == 1:
                    item_type = types[0].__name__
                    schemas[name][key] = f"List[{item_type}]"
                    use_list = True
                elif len(types) == 2:
                    item_types = ', '.join(t.__name__ for t in types)
                    schemas[name][key] = f"List[Union[{item_types}]]"
                    use_list = use_union = True
                else:
                    schemas[name][key] = "List[Any]"
                    use_list = use_any = True
            else:
                schemas[name][key] = type(value).__name__

        return schemas, use_list, use_union, use_any

    schemas_dict, has_list, has_union, has_any = wrapper(code)

    typing_imports = ", ".join([imp for imp in ("List", "Union", "Any") if locals()[f"has_{imp.lower()}"]])
    with open(output, 'w') as f:
        if typing_imports:
            f.write(f"from typing import {typing_imports}\n")
        f.write("from pydantic import BaseModel\n\n")

        for model_name, model_fields in reversed(list(schemas_dict.items())):
            f.write(f"class {model_name}(BaseModel):\n")
            for field_name, field_type in model_fields.items():
                f.write(f"    {field_name}: {field_type}\n")
            f.write("\n")
