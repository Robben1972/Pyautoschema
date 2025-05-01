
# PyAutoSchema

**PyAutoSchema** is a lightweight Python library that automatically generates [Pydantic](https://docs.pydantic.dev/) models from Python dictionaries. It's especially useful for fast prototyping, validating API responses, or converting JSON-like structures into Pydantic schemas.

## 🔧 Features

- Supports nested dictionaries
- Infers list and union types
- Generates clean, human-readable Pydantic classes
- Simple one-line usage

## 📦 Installation

```bash
pip install pyautoschema
```

## 🚀 Usage

```python
from pyautoschema import infer_schema

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

Output (`schemas.py`):

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