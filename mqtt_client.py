from paho.mqtt import client as mqtt_client


class Publisher:
    def __init__(self, host="localhost", port=1833):
        self.client = mqtt_client.Client()
        self.client.connect(host=host, port=port, keepalive=60)

    def start_client(self):
        self.client.loop_start()

    def stop_client(self):
        self.client.loop_stop()

    def publish(self, topic, payload):
        self.client.publish(topic=topic, payload=payload)


class Subscriber:
    def __init__(self, host="localhost", port=1833):
        self.client = mqtt_client.Client()
        # self.client.on_connect = self.__on_connect()
        self.client.connect(host=host, port=port, keepalive=60)
        self.topic = None
        self.payload = None
        self.counter = 0

    def start_client(self):
        self.client.loop_start()

    def stop_client(self):
        self.client.loop_stop()

    def subscribe(self, topic):
        msg = self.client.subscribe(topic=topic)
        self.client.on_message = self.__on_message
        return msg
        # self.client.on_message=self.__on_message(client=self.client)

    def __on_message(self, client, userdata, msg):
        self.counter = self.counter + 1
        self.topic = msg.topic
        self.payload = msg.payload
        # print("{topic: " +str(msg.topic) +", payload: "+ str(msg.payload)+"}")
