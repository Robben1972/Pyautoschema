# PyAutoSchema

**PyAutoSchema** is a lightweight Python library that automatically generates [Pydantic](https://docs.pydantic.dev/) models from Python dictionaries, JSON, or XML files. It's especially useful for fast prototyping, validating API responses, or converting JSON-like structures into Pydantic schemas.

## 🔧 Features

- Supports nested dictionaries and complex data structures
- Infers list, union, and other advanced types
- Generates clean, human-readable Pydantic classes
- Supports JSON and XML input formats
- Simple one-line usage

## 📦 Installation

Install PyAutoSchema using pip:

```bash
pip install pyautoschema
```

## 🚀 Usage

### Python Dictionary Example

```python
from pyautoschema import schemaCreator

sample = {
    "id": 123,
    "name": "Alice",
    "tags": ["admin", "user"],
    "profile": {
        "age": 30,
        "active": True
    }
}

infer_schema(sample, output="schemas.py")
```

Generated output (`schemas.py`):

```python
from typing import List
from pydantic import BaseModel

class Profile(BaseModel):
    age: int
    active: bool

class InferredModel(BaseModel):
    id: int
    name: str
    tags: List[str]
    profile: Profile
```

### JSON File Example

```bash
pyautoschema --input sample.json --output schemas.py
```

### XML File Example

```bash
pyautoschema --input sample.xml --output schemas.py
```

## 🛠 CLI Usage

PyAutoSchema also provides a command-line interface for generating schemas directly from JSON or XML files.

```bash
pyautoschema --input <path_to_file> --output <output_file>
```

- `--input` (`-i`): Path to the input `.json` or `.xml` file (required)
- `--output` (`-o`): Path to the output `.py` file (default: `schemas.py`)

## 🧪 Supported Types

PyAutoSchema automatically detects and maps the following types:

- **Primitive Types**: `int`, `float`, `bool`, `str`
- **Advanced Types**: `datetime`, `date`, `time`, `UUID`, `EmailStr`, `HttpUrl`
- **Collections**: `List`, `Union`, `Any`


## 🌐 Links

- [Homepage](https://pypi.org/project/pyautoschema/)
- [Repository](https://github.com/Robben1972/pyautoschema)

## 📄 License

This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.