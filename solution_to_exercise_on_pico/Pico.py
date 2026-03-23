"""
An example showing for a Pico:
  -- MQTT for communicating with another device through the Internet.
  -- Using the  mqtt_helper_pico  module to communicate with the other device.

This module is the Pico code with details of what the Pico does.
See   main_on_pico_ie_code.py   for the main function.
See   mqtt_helper_pico.py   for the MQTT library for a Pico.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

import mqtt_helper_pico  # Library for MQTT message-passing
import time  # For blinking

# Imports specific to the Pico:
import board
import digitalio


class Pico:
    """
    A simple example of Pico code. In this example:
      1. Every half-second, it sends a message indicating
           whether or not the simulated button is pressed.
      2. It listens for messages from the PC.
           When it receives a "blink" message, it blinks the built-in
           LED rapidly 4 times. It prints all received messages in the Console
           (but otherwise ignores all except the "blink" message).
    """

    def __init__(self, mqtt_client: mqtt_helper_pico.MqttClient):
        # Required instance variables:
        self.mqtt_client = mqtt_client
        self.is_done = False
        # Set the following as desired:
        self.seconds_to_sleep_at_each_iteration_of_pico_loop = 0.5

        # Initialize the built-in LED:
        self.led = digitalio.DigitalInOut(board.LED)
        self.led.direction = digitalio.Direction.OUTPUT

        # Initialize a simulated button (touching wires from GP15 to GND):
        self.button = digitalio.DigitalInOut(board.GP15)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

        self.count = 0

    # Required method (but it can do whatever you want it to do):
    def receive_message(self, message):
        """
        This is the specially-named method that the MqttClient will call
        when the MqttClient receives a message from the Broker.
        In this example, when the message is "blink", the Pico
        blinks the built-in LED rapidly 4 times.
        """
        if message == "blink":
            self.blink(4, 0.5)
        elif message == "quit":
            self.is_done = True
        elif message == "restart":
            self.count = 0
        elif "blink " in message:
            try:
                n = int(message.split()[1])
                self.blink(n)
            except Exception:
                print("Bad message format in blink n times")

    # Required method (but it can do whatever you want it to do):
    def do_one_iteration_of_the_pico_loop(self):
        """
        In this example:
          1. Display the state of the simulated button on the Console.
          2. If the simulated button is pushed, send a message indicating so.
        """
        if not self.button.value:
            print("Simulated button is pushed (i.e., down, connected.)")
            self.count = self.count + 1
            self.mqtt_client.send_message(f"Button is pushed {self.count}")
        else:
            print("Simulated button is NOT pushed (i.e., up, disconnected.)")

    # Helper method for this example:
    def blink(self, number_of_times_to_blink=10, seconds_between_blinks=0.1):
        for _ in range(number_of_times_to_blink):
            self.led.value = True
            time.sleep(seconds_between_blinks)
            self.led.value = False
            time.sleep(seconds_between_blinks)
