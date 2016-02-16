# Overview

This interface layer handles the communication between the Flume HDFS service and the Flume agents (eg, syslog, tweeter).
The provider end of the relation provides the sink service where mesages are persisted.
The other end requires the existence of the provider to function.


# Usage

## Provides

Charms providing the sink service can make use of the provides interface.

This interface layer will set the following states, as appropriate:

  * `{relation_name}.connected`   The relation to a Flume agent has been
    established, though the service list may not be available yet. At this point the
    provider should broadcast the connection properties using:
      * `send_configuration(self, port, protocol = 'avro')`

  * `{relation_name}.available`   The connection to the agent is now available and correctly setup.


Flume-HDFS is a charm that persists data from various agents. As soon a an agent get connected
the charm provides the connection details (port):

```python
@when('hadoop.ready', 'flume-agent.connected')
@when_not('flume-agent.available')
def waiting_availuable_flume(hadoop, flume_agent):
    flume_agent.send_configuration(hookenv.config()['source_port'])
    hookenv.status_set('waiting', 'Waiting for a Flume agent to become available')
```

When the agent becomes available, the Flume sink service is started.

```python
@when('flumehdfs.installed', 'hadoop.ready', 'flume-agent.available')
@when_not('flumehdfs.started')
def configure_flume(hdfs, flume_agent_rel):
    hookenv.status_set('maintenance', 'Setting up Flume')
    flume = Flume(get_dist_config())
    flume.configure_flume()
    flume.restart()
    set_state('flumehdfs.started')
    hookenv.status_set('active', 'Ready')
```


## Requires

A Flume agent charm acting as a source of information requires a Flume sink.
The Flume agent makes use of the requires part of the interface to connect to the
Flume sink.

This interface layer will set the following states, as appropriate:

  * `{relation_name}.connected` The charm has connected to the Flume sink. 
    At this point the requires intrface waits for connection details (port, ip, protocol).

  * `{relation_name}.available` The connection has been established, and the agent charm
    can get the connection details via the following calls:
      * `get_flume_ip()`
      * `get_flume_port()`
      * `get_flume_protocol()`
    In case of an error a generic exception is thrown.

Example:

```python
@when('flumesyslog.installed', 'flume-agent.connected')
@when_not('flume-agent.available')
def waiting_for_flume_available(flume):
    hookenv.status_set('waiting', 'Waiting for availability of Flume HDFS')


@when('flumesyslog.installed', 'flume-agent.available')
@when_not('flumesyslog.started')
def configure_flume(flumehdfs):
    port = flumehdfs.get_flume_port()
    ip = flumehdfs.get_flume_ip()
    protocol = flumehdfs.get_flume_protocol()
```


# Contact Information

- <bigdata@lists.ubuntu.com>
