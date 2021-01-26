#include <DHT.h>
#include <Adafruit_Sensor.h>

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define DHTPIN_corner D2 
#define DHTPIN_room D5       
#define DHTTYPE DHT11    // DHT 11

DHT dht_corner(DHTPIN_corner, DHTTYPE);
DHT dht_room(DHTPIN_room, DHTTYPE);
 
const char* SSID = "WLAN-886311";
const char* PSK = "59696816459236044341";
const char* MQTT_BROKER = "raspberrypi";
 
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
float Temperature_corner;
float Temperature_room;
float Humidity_corner;
float Humidity_room;
float DewPoint_corner;
 
void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(MQTT_BROKER, 1883);
    pinMode(D1, INPUT); 
    pinMode(LED_BUILTIN, OUTPUT);

    dht_corner.begin();
    dht_room.begin();
}

void blink() {
  for(int i=0; i<10; i++){
    digitalWrite(LED_BUILTIN, LOW);   
    delay(50);                       
    digitalWrite(LED_BUILTIN, HIGH);    
    delay(50);  
  }
}

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(SSID);
    WiFi.mode(WIFI_STA);
 
    WiFi.begin(SSID, PSK);
 
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        blink();
        Serial.print(".");
    }
 
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
 
void reconnect() {
    while (!client.connected()) {
        blink();
        Serial.print("Reconnecting...");
        if (!client.connect("ESP_bedroom")) {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying in 5 seconds");
            delay(5000);
        }
    }
}


void loop() {
    Temperature_corner = dht_corner.readTemperature(); // Gets the values of the temperature
    Humidity_corner = dht_corner.readHumidity(); // Gets the values of the humidity
    Temperature_room = dht_room.readTemperature(); // Gets the values of the temperature
    Humidity_room = dht_room.readHumidity(); // Gets the values of the humidity
    DewPoint_corner = (Temperature_corner - (100 - Humidity_corner) / 5); // approximation for the dew point

// Check if any reads failed and exit early (to try again).
//    if (isnan(Humidity_room) || isnan(Temperature_room)|| isnan(Temperature_corner)|| isnan(Humidity_corner)) {
//      Serial.println("Failed to read from DHT sensor!");
//      delay(1000);
//      return;
//    }
//    float hi = dht.getHeatIndex();
//    float dp = dht.getDewPoint();
 
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    client.publish("/bedroom/corner/temperature", String(Temperature_corner).c_str());
    delay(500);
    client.publish("/bedroom/corner/humidity", String(Humidity_corner).c_str());
    delay(500);
    client.publish("/bedroom/corner/dew_point", String(DewPoint_corner).c_str());
    delay(500);
    client.publish("/bedroom/room/temperature", String(Temperature_room).c_str());
    delay(500);
    client.publish("/bedroom/room/humidity", String(Humidity_room).c_str());
//    delay(600000); //wait 10 minutes
    delay(5000);
}
