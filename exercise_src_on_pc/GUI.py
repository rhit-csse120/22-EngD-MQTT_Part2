"""
An example showing for tkinter and ttk:
  -- MQTT for communicating with another device through the Internet.
  -- Using the  mqtt_helper_pc  module to communicate with the other device.

This module is the GUI on the pc which communicates with the Pico.
See   main_on_pc.py   for the main function.
See   mqtt_helper_pc.py   for the MQTT library for a pc.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

import tkinter
from tkinter import ttk
import mqtt_helper_pc  # Library for MQTT message-passing


class Gui:
    """
    The GUI by which the PC communicates with the Pico.
    In this example, it displays the most recent message from the Pico
    in a Label and sends messages to the Pico via an Entry
    (to hold the message to send) and Button (to initiate sending).
    """

    def __init__(self, root: tkinter.Tk, mqtt_client: mqtt_helper_pc.MqttClient):
        # Required instance variables:
        self.root = root
        self.mqtt_client = mqtt_client

        # Frame that covers the root Toplevel.
        frame = ttk.Frame(root, padding=10)
        frame.grid()

        # Entry box with data to send to the Pico.
        entry = ttk.Entry(frame)
        entry.grid()

        # Button that sends data in the Entry box to the Pico.
        button = ttk.Button(frame, text="Send Entry box data to the Pico")
        button.grid()
        button["command"] = lambda: self.do_button(entry)

        # Label that shows data sent from the Pico, as it arrives.
        self.label = ttk.Label(frame, text="No data yet")
        self.label.grid()

    # Required method (but it can do whatever you want it to do):
    def receive_message(self, message):
        """
        This is the specially-named method that the MqttClient will call
        when the MqttClient receives a message from the Broker.
        In this case, the method puts the given message onto the label.
        """
        self.label["text"] = message

    # Helper function for this example:
    def do_button(self, entry: ttk.Entry):
        """
        Called with the button is pressed.
        Sends whatever text is in the given Entry to the Pico.
        """
        message = entry.get()
        self.mqtt_client.send_message(message)
