"""
Library built on top of  adafruit_minimqtt  for two devices to communicate
through the Internet, using a MQTT Broker as the intermediary.
Use as is except where TODO indicates otherwise.

This library is for a Pico running CircuitPython as one of the two devices.
See   mqtt_helper_pc.py   for the corresponding library for a PC / laptop.

See the  main_on_pico.py  file in this project for how to USE
this library on a Pico.

USAGE: In both cases, the key steps in USING this library
in your project are simply:

  1. In main, create an instance of the MqttClient class below.
     Let's call that instance mqtt_client.

  2. The applications using this library will need mqtt_client
     to call its  send_message  method to send messages
     from one device to the other device.

     For example, on the Pico the application will be the Pico.
     It will need  mqtt_client  to send messages to the PC / laptop.
     So, pass the  mqtt_client  object to the Pico
     when it is constructed.

  3. Additionally, the application will need the
     mqtt_client  object to use its  set_dispatcher  method
     to establish the Pico (in the case of the Pico) as the
     object to "dispatch" messages.

     In this protocol, the Pico must have a method
     called  receive_message  that is the method that
     the  mqtt_object  invokes on the Pico when the  mqtt_object
     receives a message.  The Pico can then do what it wants
     with the message received by its  receive_message  method.

  4. After the above, main must call the  start  method
     on the  mqtt_client  object to start the  mqtt_client's
     event loop (receiving messages) in its own thread.

Using the  mqtt_helper_pc  library on the PC (laptop) is similar.

RESOURCE:  See
   https://cdn-learn.adafruit.com/downloads/pdf/mqtt-in-circuitpython.pdf
for an explanation of MQTT in CircuitPython.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

# -----------------------------------------------------------------------------
# You need the following Adafruit libraries in the  lib  folder on the Pico:
#    adafruit_minimqtt
#    adafruit_connection_manager.mpy
#    adafruit_ticks.mpy
#
# You also need a  secrets.py  file with the required information.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# These imports are for the WIFI and MQTT communication, specific to the Pico:
# -----------------------------------------------------------------------------
import ssl
import sys
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt

# The UNIQUE_ID, BROKER and TCP_PORT must match that of the PC / laptop.
UNIQUE_ID = "DavidMutchler1019"  # TODO: Use something that no one else will use
BROKER = "broker.emqx.io"  # Or: "broker.hivemq.com", but must match PC
TCP_PORT = 1883


class MqttClient(adafruit_minimqtt.adafruit_minimqtt.MQTT):
    def __init__(self, wifi: Wifi, suffix1="pico", suffix2="pc", broker=BROKER):
        """
        wifi    -- the required Wifi object, properly initialized.
        suffix1 -- the suffix used in the topic to which the pc PUBLISHES.
        suffix2 -- the suffix used in the topic to which the pc SUBSCRIBES.
        broker  -- the broker to which to publish and subscribe.
        """
        self.wifi = wifi
        super().__init__(
            broker=self.wifi.secrets["broker"],
            port=self.wifi.secrets["port"],
            username=self.wifi.secrets["mqtt_username"],
            password=self.wifi.secrets["mqtt_key"],
            socket_pool=self.wifi.pool,
            ssl_context=ssl.create_default_context(),
        )

        self.suffix1 = suffix1
        self.suffix2 = suffix2
        self.pico_to_pc_topic = UNIQUE_ID + "/" + suffix1 + "_to_" + suffix2
        self.pc_to_pico_topic = UNIQUE_ID + "/" + suffix2 + "_to_" + suffix1
        self.broker = broker
        self.message_dispatcher = None  # This is set later
        self.print_who_am_i()

    def print_who_am_i(self):
        print(f"\nI am {self.suffix1}, talking to {self.suffix2}\n")

    def set_dispatcher(self, message_dispatcher):
        self.message_dispatcher = message_dispatcher

    def start(self):
        print("Connecting to the broker...")
        self.connect()
        print(f"\nSubscribing to {self.pc_to_pico_topic}...")
        self.subscribe(self.pc_to_pico_topic)

    def on_connect(self, mqtt_client, topic, flags, reason_code):
        """
        Called when a connection to the Broker has been established
        or when the code has given up trying to do so (timeout).
        """
        if reason_code == "Success":
            print(f"CONNECTED to MQTT broker {self.broker}")
        else:
            print(f"Failed to connect to broker {self.broker}.\n")
            print(f"The return code was {reason_code}.\n")

    def on_subscribe(self, mqtt_client, userdata, topic, granted_qos):
        """Called when subscribed to a topic."""
        print(f"Subscribed to topic {topic}, which is:")
        print(f"{self.pc_to_pico_topic}\n")

    def on_message(self, mqtt_client, topic, message):
        """
        Called when a message arrives.  Display it on Console.
        Send it to the dispatcher (e.g. the GUI) for processing.
        """
        # Show the message on the Console, for debugging as needed.
        # Then dispatch the message to the message_dispatcher object.
        print(f"\nReceived message: {message}")
        self.message_dispatcher.receive_message(message)

    def send_message(self, message: str):
        """Publish (send to other device) the given message."""
        # Show the message on the Console, for debugging as needed.
        # Then publish the message to the broker.
        print(f"Sending message: {message}")
        self.publish(self.pico_to_pc_topic, message)


class Wifi:
    def __init__(self):
        # ---------------------------------------------------------------------
        # Load the WiFi and broker credentials from the file: secrets.py
        # ---------------------------------------------------------------------
        try:
            from secrets import secrets
        except ImportError:
            print("WiFi secrets are kept in secrets.py, please add them there!")
            raise
        self.secrets = secrets

        # ---------------------------------------------------------------------
        # Connect to the configured WiFi network
        # ---------------------------------------------------------------------
        print(f"\nAttempting to connect to WiFi: {secrets['ssid']} ...")
        try:
            wifi.radio.connect(secrets["ssid"], secrets["password"])
        except Exception as e:
            print("  Could NOT connect to WiFi. Error message was:")
            print(e)
            sys.exit(1)

        print(f"  CONNECTED to wifi {secrets['ssid']}")

        # Create a socket pool
        self.pool = socketpool.SocketPool(wifi.radio)
