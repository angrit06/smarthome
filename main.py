from mqtt_client import Publisher, Subscriber
from db_service import DBService
from time import sleep


def main():
    # ********************* mqtt section ********************************
    publisher = Publisher(host='raspberrypi', port=1883)
    publisher.start_client()
    subscriber = Subscriber(host='raspberrypi', port=1883)
    subscriber.start_client()
    old_counter = subscriber.counter
    # subscriber.subscribe("/bedroom/corner/#")
    subscriber.subscribe("/cellar/electricity_meter/# ")
    # ********************* database section ****************************
    db_service = DBService(
        db_address='mongodb+srv://angrit:writer@cluster0.bt8uy.mongodb.net/smarthome?retryWrites=true&w=majority')
    while True:
        if old_counter < subscriber.counter:
            if subscriber.topic == "/cellar/electricity_meter/X":
                print("magnetic value X : ", subscriber.payload)
                # db_service.save_data(topic=subscriber.topic, payload=float(subscriber.payload.decode('utf8')))
                subscriber.topic = None
            elif subscriber.topic == "/cellar/electricity_meter/Y":
                print("magnetic value Y : ", subscriber.payload)
                # db_service.save_data(topic=subscriber.topic, payload=float(subscriber.payload.decode('utf8')))
                subscriber.topic = None
            elif subscriber.topic == "/cellar/electricity_meter/Z":
                print("magnetic value Z : ", subscriber.payload)
                # db_service.save_data(topic=subscriber.topic, payload=float(subscriber.payload.decode('utf8')))
                subscriber.topic = None
            # if subscriber.topic == "/bedroom/room/temperature":
            #     print("bedroom temperature: ", subscriber.payload)
            #     db_service.save_data(topic=subscriber.topic, payload=float(subscriber.payload.decode('utf8')))
            #     subscriber.topic = None
            # elif subscriber.topic == "/bedroom/room/humidity":
            #     print("bedroom humidity: ", subscriber.payload)
            #     db_service.save_data(topic=subscriber.topic, payload=float(subscriber.payload.decode('utf8')))
            #     subscriber.topic = None
            # elif subscriber.topic == "/bedroom/corner/temperature":
            #     print("bedroom corner temperature: ", subscriber.payload)
            #     db_service.save_data(topic=subscriber.topic, payload=float(subscriber.payload.decode('utf8')))
            #     subscriber.topic = None
            # elif subscriber.topic == "/bedroom/corner/humidity":
            #     print("bedroom corner humidity: ", subscriber.payload)
            #     db_service.save_data(topic=subscriber.topic, payload=float(subscriber.payload.decode('utf8')))
            #     subscriber.topic = None
            # elif subscriber.topic == "/bedroom/corner/dew_point":
            #     print("bedroom corner dew point: ", subscriber.payload)
            #     db_service.save_data(topic=subscriber.topic, payload=float(subscriber.payload.decode('utf8')))
            #     subscriber.topic = None
        old_counter = subscriber.counter
        sleep(0.25)


if __name__ == '__main__':
    main()
