# PyreFinder

## Brokers and setup

Currently there are two brokers that can be used: Mosquitto and HiveMQ. Mosquitto is the lightweight option and uses little space and memory but does present issues with scaling as opposed to HiveMQ which does use far more resources but can easily scale in addtion to handling security and has industry/paid support. So take advantage of both scalability and minimal resources, Mosquitto would be used by Fighters while HiveMQ would be used for Finder. Depending on the broker for the project, here is how you can start each broker.

### Mosquitto

`docker run -d -p 1883:1883 -p 1884:1884 -v {:project_root}/component-configs/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto`

### HiveMQ

`docker run -d -p 1883:1883 -p 1884:1884 -v {:project_root}/component-configs/config.xml:/opt/hivemq/conf/config.xml --name hivemq hivemq/hivemq-ce`
