# LambdaSolid
LambdaSolid
------------
## Installation

To get started, make sure you have Python 3.13 (or any compatible Python version you intend to use) installed on your system.

To set up and install the project, follow these steps using the Makefile:

### Create a virtual environment with Python 3.13:
```shell
    python3.13 -m venv venv
```
### Activate the newly created virtual environment:
```shell
    source venv/bin/activate
```
### Copy local environment variables:
```shell
    cp .env.local .env  
```
### Install the project requirements using Makefile:
```shell
    make install
```
This will prepare your environment and install the necessary dependencies.

## Testing
### Run tests
```shell
  make test
```
### Check coverage
```shell
  make coverage
```