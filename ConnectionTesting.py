import paho.mqtt.client as mqtt
import ssl

client = mqtt.Client(transport="websockets", userdata=True,
                     clean_session=True)


def onConnect(client, userdata, flags, rc):
    print('connected!')
    print('subscribing to topic')
    client.subscribe('test')
    client.publish('test', '▓')


def onDisconnect(client, userdata, rc):
    print('disconnected!')
    print(rc)


def onMessage(client, userdata, message):
    print('got message: ' + str(message.payload))


backup_str = "this is everything you have missed so far"

client.tls_set(ca_certs=None, certfile=None, keyfile=None,
               cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS,
               ciphers=None)
client.on_connect = onConnect
client.on_disconnect = onDisconnect
client.on_message = onMessage

client.username_pw_set('solace-cloud-client',
                       password='isabr7e7kn29vqagqtehe81gan')
client.connect('mr4b11zr9hl.messaging.mymaas.net', 8443, 20)

client.publish('test', 'small boy', qos=1)
client.publish('test', 'Big boy', qos=1)
client.publish('test', 'All boy', qos=0)
client.publish('test', 'My boy', qos=1)
client.loop_forever()
