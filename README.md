# Pyrefinder
*A realtime wilfdire detection and monitoring system*

## Getting started
To get started you will need the following
* Docker
* Python3 with pipenv installed

The steps to run the project are as follows:
1. In the terminal within the project directory run `pipenv shell && pipenv install --dev` to install all the dependencies
2. To then start the HiveMQ using `docker run -d -p 1883:1883 -p 1884:1884 -v {:project_root}/component-configs/config.xml:/opt/hivemq/conf/config.xml --name hivemq hivemq/hivemq-ce` where the project_root is the absolute path to the project
4. Initialize the database for the project by running `python -m pyrefinder.db_init` and a new SQLite Database should appear
3. Once the MQTT broker is running, launch pyrefinder with `python -m pyrefinder.main` and it should say "Connected" in the terminal and producing logs

And now you're ready to to accept incoming connections and act appropriately based of the topic.

## Testing
In order to run the tests for functionality do the following:
1. First initalize the database prior to running the test using `python -m pyrefinder.db_init`.
2. Then in the project folder run `pytest -v` to view each test ran

In order to run the publisher tests, make sure that the broker and pyrefinder is running per above instructions and then use `python -m publisher.py`