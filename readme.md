### Create a topic:

```bash
docker exec -it kafka sh -c "/opt/bitnami/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9093 --replication-factor 1 --partitions 3 --topic raw-push"
```





# python-app-template
The python-app-template is a templated application structure that can be used
for all new and existing (with a refactor) applications. The structure is based
on Clean Architecture (aka Ports & Adapters, Onion Architecture, Hexagonal
Architecture).

### Directory Structure
The top level structure includes:
* docs - where all documentation should go including diagrams, adrs, etc.
* modules - where git submodules are put if they are used
* python-app-template - the application source code is in a directory named for itself
* tests - the tests live outside the application source code, this directory is
further broken down into a directory of the types of tests: unit, integration, etc.

### Architecture Glossary
This is a glossary of components in the python-app-template directory.

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
`__main__` is the application entry point. It's only repsonsibilites are to load and log the app settings and call `app.py`.


### Responsibilities of `app.py`
`app.py` is the main application class. It's repsonsibilites are to:
* Setup monitoring, including:
    - logging
    - metrics
* Initialize adapters
* Act as the composite root and create an object graph
* Define dependency life cycles
* Run preflight checks
* Start/serve/initiate/etc. the primary adapters
* Top level exception handling and graceful process exiting



## Runningal
> alembic upgrade head

### Downgrading
- To remove all migrations done do:
> alembic downgrade base

- To go back to a specific migration revision do:
> alembic downgrade <revision_id>

`NOTE`: You can do `alembic history` to a view a list of migrations in the project
