# Function
F5 tool chain CLI (f5-toolchain)
 
# Usage
```
F5 tool chain CLI - a tool for working with F5 tool chain.
```
 
# Installation
```
cd f5_toolchain
python3 -m venv .venv
source .venv/bin/activate
python3 setup.py install
f5-toolchain --help
```

# Development
```
For development use the following install mode, so you can
make changes in the code and use it directly in the cli.

cd f5_toolchain
source .venv/bin/activate
pip3 install -r requirements.txt
pip3 install -e .
```