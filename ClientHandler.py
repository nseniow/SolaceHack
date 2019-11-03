import paho.mqtt.client as mqtt
import ssl
import GUI
import json

Notepad = GUI.Notepad

backup = None


# Fix spaghetti if possible

def onConnect(client, userdata, flags, rc):
    print('connected!')


def onDisconnect(client, userdata, rc):
    print('disconnected!')
    print(rc)
    client.loop_stop()


def onMessage(client, userdata, message):
    try:
        content = json.loads(message.payload)
        backup.receive(content)
        print('got message:')
    except Exception as e:
        print('Decode failure.')
        print(e)


class ClientHandler:
    username: str
    password: str
    broker_ip: str
    broker_port: int

    nickname: str
    doc_serial: str

    client: mqtt
    is_host: bool

    gui: GUI

    def __init__(self, id, username='solace-cloud-client',
                 password='isabr7e7kn29vqagqtehe81gan',
                 broker_ip='mr4b11zr9hl.messaging.mymaas.net',
                 broker_port=8443):

        self.client = mqtt.Client(client_id=id, transport="websockets",
                                  userdata=True, clean_session=False)

        self.client.tls_set(ca_certs=None, certfile=None, keyfile=None,
                            cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLS, ciphers=None)
        global backup
        backup = self
        self.client.on_connect = onConnect
        self.client.on_disconnect = onDisconnect
        self.client.on_message = onMessage
        self.client.username_pw_set(username, password=password)
        self.is_host = False

    def attempt_connection(self):
        self.nickname = str(self.client._client_id, 'UTF-8')
        self.client.connect('mr4b11zr9hl.messaging.mymaas.net', 8443, 20)
        self.client.loop_start()

    def connect_doc(self, doc_serial: str):
        # Assume the GUI reference has the done
        self.doc_serial = doc_serial
        self.client.subscribe("doc/" + doc_serial)
        if not self.is_host:
            self.request_update()

    def request_update(self):
        self.client.subscribe("doc/" + self.doc_serial + "/update")

        self.client.publish("doc/" + self.doc_serial,
                            json.dumps({"name": self.nickname,
                                        "target": "requestupdate"}))

        # TODO 1) Request Update 2) Update Cursor 3) Insertion 4) Deletion 5) Disconnection

    def receive(self, message):

        name = message["name"]
        target = message['target']

        self.gui.check_existing_editors(name)

        if target == "cursorupdate":
            self.gui.update_cursors(name, message)
        elif target == "insert":
            if name == self.nickname:
                return
            position = message['position']
            text = message['text']
            self.gui.insert_text(position, text)
        elif target == "delete":
            if name == self.nickname:
                return
            p1 = message['p1']
            p2 = message['p2']
            self.gui.delete_text(p1, p2)
        elif target == "requestupdate":
            if self.is_host:
                self.client.publish("doc/" + self.doc_serial + "/update",
                                    json.dumps({'name': self.nickname,
                                                'target': 'update',
                                                'text': self.gui.get_text()}))
            print('update request received')
        elif target == "update":
            self.client.unsubscribe("doc/" + self.doc_serial + "/update")
            self.gui.set_text(message['text'])
        elif target == "chat":
            pass
        elif target == "disconnect":
            pass

    def send(self, dict):
        if dict['target'] == 'chat':
            print('s')
        else:
            self.client.publish('doc/' + self.doc_serial, json.dumps(dict))
