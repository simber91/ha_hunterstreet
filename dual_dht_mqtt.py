import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

state_topic1 = '/hunterstreet/rpi6_temp1'
state_topic2 = '/hunterstreet/rpi6_temp2'
state_topic3 = '/hunterstreet/rpi6_humid1'
state_topic4 = '/hunterstreet/rpi6_humid2'
client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.0.69", 1883, 60)
time.sleep(1)


dhtDevice1 = adafruit_dht.DHT11(board.D2, use_pulseio=False)
dhtDevice2 = adafruit_dht.DHT11(board.D3, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        temperature1_c = dhtDevice1.temperature
        temperature2_c = dhtDevice2.temperature
#        temperature_f = temperature_c * (9 / 5) + 32
        humidity1 = dhtDevice1.humidity
        humidity2 = dhtDevice2.humidity
#        print(
#            "Temp1: {:.1f} C  Temp2: {:.1f}   Humidity1: {}%   Humidity2: {}% ".format(
#                temperature1_c, temperature2_c, humidity1, humidity2
#            )
#        )
        client.loop_start()
        client.publish(state_topic1, payload=str(temperature1_c), qos=0, retain=False)
        client.publish(state_topic2, payload=str(temperature2_c), qos=0, retain=False)
        client.publish(state_topic3, payload=str(humidity1), qos=0, retain=False)
        client.publish(state_topic4, payload=str(humidity2), qos=0, retain=False)
#        print("Send it")
        time.sleep(5)
        client.loop_stop()

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(5)

