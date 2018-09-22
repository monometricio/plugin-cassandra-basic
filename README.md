# plugin-cassandra-basic
Monometric.IO cassandra plugin (https://monometric.io)

## Description

This plugin will query cassandra for tablestats using nodetool cfstats. 

## Installation

```mm-plugins install monometricio/plugin-cassandra-basic```

```mm-plugins enable monometricio/plugin-cassandra-basic```

You should see the plugin when running ```mm-plugins list```.

Remember to edit the configuration file ```/etc/mm-agent/plugins/monometricio-plugin-cassandra-basic.conf```.

## Configuration

The plugin has the following optional configuration keys:

- NODETOOL_HOST -- Controls the host that the nodetool utility connects to

By default, this plugin is configured to only run once every 120 seconds.

## Testing configuration

You can test-run the plugin and verify the output by running:

```mm-plugins run monometricio/plugin-cassandra-basic```
