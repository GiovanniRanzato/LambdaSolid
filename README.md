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

## 🧱 Project Structure – Hexagonal Architecture

LambdaSolid follows a [Hexagonal Architecture (Ports & Adapters)](https://alistair.cockburn.us/hexagonal-architecture/) design, which promotes **separation of concerns**, **testability**, and **independence from infrastructure**.

```
src/
├── domain/                       # Core business logic (pure)
│   ├── models/                   # Domain entities (e.g. Order, User)
│   ├── services/                 # Business use cases
│   └── interfaces/               # Abstract ports (e.g. RepositoryI)
│
├── infrastructure/              # Frameworks & technical details
│   ├── config/                  # Configuration components (e.g. Config, SecretManager)
│   ├── factories/               # Technical components factories (e.g. EventFactory, HandlerFactory)
│   ├── interfaces/              # Technical interfaces (e.g. EventI, HandlerI)
│   ├── App.py                   # Application orchestrator (wires everything)
│   ├── containers.py            # Dependency injection setup for core structure (via `dependency_injector`)
│   ├── depends.py               # Dependencies definitions for the application
│   └── EventsRegistry.py        # Internal event routing registry 
│   
├── api/                         # Input adapters (events/APIs)
│   └── api_gateway/             # Logic for API Gateway events (e.g. FastAPI routing)
│
├── repositories/                # Output adapters (DB, SNS, etc.)
│   └── db/                      # Example: DB repositories implementing interfaces
│
├── main.py                      # AWS Lambda entrypoint
└── tests/                       # Unit/integration tests (mirroring the src structure)
```

### Key Concepts

- `domain/` is **framework-agnostic** and contains the heart of the business logic.
- `infrastructure/` deals with **how** the logic is executed (frameworks, DI, factories).
- `api/` and `repositories/` are **adapters** that handle external I/O.
- `main.py` is the **entrypoint** for your AWS Lambda deployment.
- Interfaces like `EventI`, `HandlerI`, and the `EventsRegistry` are placed in `infrastructure/` because they **serve technical routing**, not domain rules.
