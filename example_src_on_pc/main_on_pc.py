"""
Example showing for tkinter and ttk:
  -- MQTT for communicating with another device through the Internet.
  -- Use the  mqtt_helper  module to communicate with the other device.

This example shows communication between a PC (this program)
and a Pico (running  code.py  from src_on_pico).

A GUI will appear.  Do what it suggests.
The Console output will appear on the Run window in PyCharm.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

import mqtt_helper_pc  # Library for MQTT message-passing
import tkinter  # For starting the GUI
import GUI  # For details of the GUI


def main():
    """
    Initialize the MQTT client, the root TK object, and the GUI object.
    Set the latter as the dispatcher for the former.
    Start the MQTT client's loop.
    Enter and stay in the root's mainloop.
    """
    # MqttClient object, properly initialized.  Note suffixes.
    mqtt_client = mqtt_helper_pc.MqttClient("pc", "pico")

    # Root (main) window.
    root = tkinter.Tk()
    root.title("MQTT example")

    # Make the GUI.  # It is the dispatcher for the MqttClient
    # (i.e., it acts upon messages from the MqttClient).
    gui = GUI.Gui(root, mqtt_client)  # The ttk.Frame that covers the root
    mqtt_client.set_dispatcher(gui)

    # Start the event loop for the MqttClient, in its own thread.
    mqtt_client.start()

    # Stay in the event loop for the rest of the program's run.
    root.mainloop()


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
