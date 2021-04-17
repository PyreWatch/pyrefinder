# PyreFinder

## Brokers and setup

In order to utilize MQTT in our system we decided to use HiveMQ. HiveMQ is an idustry strength broker which can easily scale in addition to supporting the full MQTTv3.1 protocol and has options for enterprise support and security. Specifically, we take advantage of the scalability and clustering abilities of HiveMQ to serve as our bridge for both our backend and for third parties. To launch the broker use the following docker command: `docker run -d -p 1883:1883 -p 1884:1884 -v {:project_root}config.xml:/opt/hivemq/conf/config.xml --name hivemq hivemq/hivemq-ce`
