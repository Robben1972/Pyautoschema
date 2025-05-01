from setuptools import setup, find_packages

setup(
    name='pyautoschema',
    version='0.1.0',
    author='Shakhobiddin Bozorov',
    description='Generate Pydantic schemas from dictionaries automatically',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
