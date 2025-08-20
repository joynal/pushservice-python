# Push Notification Service

Simple push notification app. This have three components pushservice(API), parser, and sender. Parser process push notifications and sends them to the appropriate channels. Sender is responsible for delivering the notifications. This has followed hexagonal architecture principles.

## Setup

1. Run postgres database and kafka with docker:
```
docker compose up -d
```

2. Copy settings.template.yaml to settings.yaml and update the values as needed.

3. Create a virtual environment and install dependencies:
```bash
uv venv --python 3.13.6
source venv/bin/activate
uv pip install -r requirements.txt
```

4. Run DB migrations
```bash
alembic upgrade head
```

5. create some dummy data

```bash
python -m database.seed.site
python -m database.seed.subscriber -s=[get the site id from previous step] -l=100
python -m database.seed.push -s=[get the site id from previous step]
```

6. Create kafka topic, with kafka we are going to pass events from one service to another

```bash
docker exec -it kafka sh -c "/opt/bitnami/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic raw-push"

docker exec -it kafka sh -c "/opt/bitnami/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic send-push"
```

## Run application

Following process will trigger a push notification for dispatch, the notification will be pass over kafka topic and from there parser will catch it and process it.
Then it will send it to sender or the dispatching to FCM/Mozilla Autopus.

```bash
python -m parser

# In other terminal run 1 ore more sender application
python -m sender
```

8. Dispatch a push notification service, get the notification id from previous step or db

```bash
python -m scripts.schedule_notification -n=<notification_id>
```

## Test

```
# test database migration
pytest --test-alembic

# other test
pytest tests/unit/test_push_parser.py
```

### Directory Structure

The top level structure includes:

- docs - where all documentation should go including diagrams, adrs, etc.
- modules - where git submodules are put if they are used
- pushservice(API), parser, sender - the application source code is in a directory named for itself
- tests - the tests live outside the application source code, this directory is
  further broken down into a directory of the types of tests: unit, integration, etc.

### Architecture Glossary

This is a glossary of components in the pushservice(API), parser, sender directory.

##### Adapters

`/adapters` are the peripheral application
components that do IO calls. The core principle of Clean Architecture is ensuring IO
is on the periphery of the application as opposed to traditional layered architecture
where is is in the middle. Adapters can be broken into two types Primary
and Secondary. Interaction between adapters and the application core is done
through Ports.

A primary adapter is a driving adapter which means it initiates application
functionality (via a port that wraps a use case). Typically the initiation is
driven by something like a http request or a message coming off an inbound queue.

A secondary Adapter is a driven adapter which means it is called out to from within
the application core (via a port). An example would be pushing a message to a queue or doing
CRUD on a database.

##### Domain

`/core/domain` (aka business logic) is the pure functional aspect of the application.
Calling a module in the Domain should never result in IO; this is a hard rule. The
domain is a collection of algorithms and data structures that provide useful
functionality that is consumed by the use cases.

##### Ports

`/core/ports` are an abstract implementation (i.e. contract) of a set of
functions/methods that do IO. Ports are defined in the application core but their
concrete implementations are defined as adapters.

##### Use Cases

`/core/use_cases` (aka application services) are the almost-pure functional aspects
of the application. Almost-pure in that it does not have any coupling to IO
dependencies but instead interacts with them via the Port/Adapter abstraction. The
inversion of control pattern is key to achieving this decoupling.
Use cases are the glue between the ports and domain logic. They are driven
by primary adapters and in turn drive secondary adapters. The entire functionality
of the application can be expressed as an aggregate of the use cases.

### Responsibilities of `__main__.py`

`__main__` is the application entry point. It's only responsibilities are to load and log the app settings and call `app.py`.

### Responsibilities of `app.py`

`app.py` is the main application class. It's responsibilities are to:

- Setup monitoring, including:
  - logging
  - metrics
- Initialize adapters
- Act as the composite root and create an object graph
- Define dependency life cycles
- Run preflight checks
- Start/serve/initiate/etc. the primary adapters
- Top level exception handling and graceful process exiting

## Run db migrations

> alembic upgrade head

### Downgrading

- To remove all migrations done do:

  > alembic downgrade base

- To go back to a specific migration revision do:
  > alembic downgrade <revision_id>

`NOTE`: You can do `alembic history` to a view a list of migrations in the project

## Pre-commit hook

Install pre-commit:

```bash
pip install pre-commit
```

Initialized hooks:

```bash
pre-commit install
```

Update pre-commit config to latest:

```bash
pre-commit autoupdate
```

Run pre-commit without commit:

```bash
pre-commit run
```

Run pre-commit on all files:

```bash
pre-commit run --all-files
```
