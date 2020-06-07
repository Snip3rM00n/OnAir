# OnAir
A MicroPython Project an On Air Wireless Notification System.

## Requirements
To run this repository you need two ESP8266 NodeMCU CP2102 ESP-12E micro controllers.
    * https://www.amazon.com/gp/product/B010N1SPRK

These microcontrollers will need to be flashed with MicroPython (binary provided in shared_esources/micropython_binary)

You'll also need some wires, 4 LEDs (2 red, 2 green), 4 220Ohm resisters, a ceramic capacitor and slider switch.
It's recommeneded you get these from a kit such as: https://www.amazon.com/gp/product/B07QT78FXF

### Flashing the microcontrollers on Windows
1. Install the requirements.txt
    `pip install -r requirements.txt`
2. Plug in the micro controller via USB
3. Get the COM port of the device
    `python -m serial.tools.list_ports`
    This example will assume its on COM4, replace COM4 with the correct port during your set up.
4. Erase the device
    `esptool --port COM4 erase_flash`
5. Flash MicroPython onto the device
    `esptool --port COM4 --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-20170612-v1.9.1.bin`
6. Once flashed, connect to the device in PuTTy
    Serial Line: COM4
    Speed: 115200
    Connection Type: Serial
7. Configure WebRepl
    `import webrepl_setup`
8. Reboot the device
9. Connect to the device's wifi signal
10. Connect to the device via WebRepl (https://github.com/micropython/webrepl).

## Set up the code and devices
For each device there is a fritzing schematic (the ESP8266 NodeMCU CP2102 ESP-12E is not available in Frizing  so the schematic uses Teensy devices, however the pins are correct, TODO: better fritzing).  Set up each device with a breadboard and the components displayed in the fritzing.  Once that is done, add the files for each device using WebREPL.  Each device files is listed below.  Before adding the "passwords.txt" you'll need to update it with your WIFI credenials for your local network.

### Order of Operations:
1. Setup the reciever and reboot it.
2. Get the IP address of the reciever.
    *   This can be done through the DHCP Clients table of your router, the device name will be something like: `ESP_3CE17F`
3. Setup the swicher and reboot it.
2. Get the IP address of the switcher.
    *   This can be done through the DHCP Clients table of your router, the device name will be something like: `ESP_3CE255`

### Files for Reciever:
*   reciever_device/main.py
    *   Update this file with the IP address of the switcher in the `ACCEPTABLE_IPS` list
*   shared_resources/boot.py
*   shared_resources/passwords.txt
    *   Update this file with your WIFI credentials before uploading.  The format is: `network_name network_password`

### Files for Switcher:
*   switch_device/main.py
    *   Update this file with the IP of the reciever device in the `RECIEVER` variable in the format of a web URL
        * Example: `http://127.0.0.1:8080`
*   shared_resources/boot.py
*   shared_resources/passwords.txt
    *   Update this file with your WIFI credentials before uploading.  The format is: `network_name network_password`

## Start Up Sequence:
To start up everything correctly, follow this order:
1. Boot up the reciever device, wait for its power-on-self-test to finish
    *   The power-on-self-test is indicated by 3 flashes of the red and green LEDs
    *   Once its on, the green and red LEDs will be on at the same time until it recieves a signal from the switcher.
2. Boot up the switcher device, wait for its power-on-self-test to finish
    *   The power-on-self-test is indicated by 3 flashes of the red and green LEDs
    *   Once its on, the LED thats powered on will be whatever the switch is set to.
        *   Value 0 = Green LED
        *   Value 1 = Red LED
3. Toggle the switch on the switcher.
    *   You can confirm that it is working by the same colored LED will be powered on on both devices.

## Switcher Error Signals:
The switcher will show different LED patterns when an error occurs.

### Bad Request Error:
This is indicated by an alternating flashing of the red and green LEDs in the pattern: `red, green, red, green...`

Causes:
*   Invalid path set to the reciever.

### Unauthorized Error:
This is indicated by an double flash of the red LED followed by a double flash of the green LED.  Example pattern: `red, red, green, green...`

Causes:
*   IP Address of switcher not provided in the `ACCEPTABLE_IPS` list of the reciever's `main.py` file.

### Cannot Connect:
This is indecated by the red LED flashing.

Causes:
*   IP Address of reciever not provided to the `RECIEVER` variable of the switcher's `main.py` file.
*   The `RECIEVER` variable is not in an URI format.
*   No Wifi connection on either the switcher or reciever device.
*   Connection Refused - possibly because the TCP port is not provided in the `RECIEVER` variable