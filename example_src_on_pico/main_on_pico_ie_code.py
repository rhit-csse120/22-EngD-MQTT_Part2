"""
Example showing a Pico, running CircuitPython,
communicating with another device through MQTT.

*** This runs on a PICO, not on a PC / laptop! ***
*** It must be renamed  code.py  on the Pico.  ***

Author:  David Mutchler, Rose-Hulman Institute of Technology,
         based on examples from the internet.
"""

import mqtt_helper_pico  # Library for MQTT message-passing
import Pico  # Details of what the Pico does
import time


def main():
    """
    Initialize Wifi and the MQTT client. Start the MQTT client.
    Enter and stay in the Pico's main loop.
    """
    # Wifi and MqttClient objects, properly initialized.  Note suffixes.
    wifi = mqtt_helper_pico.Wifi()
    mqtt_client = mqtt_helper_pico.MqttClient(wifi, "pico", "pc")

    # Make the Pico object.  # It is the dispatcher for the MqttClient
    # (i.e., it acts upon messages from the MqttClient).
    pico = Pico.Pico(mqtt_client)
    mqtt_client.set_dispatcher(pico)

    # Start the event loop for the MqttClient, in its own thread.
    mqtt_client.start()

    # Stay in the Pico's loop until done.
    while not pico.is_done:
        # Poll for up to 1.0 second to see if any messages have arrived
        mqtt_client.loop(timeout=1.0)  # Tune as desired
        pico.do_one_iteration_of_the_pico_loop()
        time.sleep(pico.seconds_to_sleep_at_each_iteration_of_pico_loop)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
