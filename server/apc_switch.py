from telnetlib import Telnet
from serial import Serial
import time

# BEGIN CONFIG
username = "script"
password = "EXAMPLE PASSWORD"
hostname = "10.0.0.4"
serial_device = "/dev/cuaU0"
baud_rate = 9600
switched_outlet = 8
default_off_outlets = [6, 7]
# END CONFIG

# Menu options
DEVICE_MANAGER = b"1\r\n"
CONTROL_OUTLET = b"1\r\n"
OUTLET_CONTROL = b"2\r\n"
IMMEDIATE_ON = b"1\r\n"
IMMEDIATE_OFF = b"2\r\n"
IMMEDIATE_REBOOT = b"3\r\n"
PROMPT = b">"

def main():
    serial = Serial(serial_device, baudrate=baud_rate)

    telnet = Telnet(hostname)
    login(telnet)
    for outlet in default_off_outlets:
        control_outlet(telnet, outlet, IMMEDIATE_OFF)
    telnet.close()

    previous_state = ""
    last_changed_time = 0
    while True:
        state = serial.readline().decode("ascii")[:-1]
        # Only allow status to be changed once every second
        if state != previous_state and last_changed_time < (time.time()-1):
            previous_state = state
            action = IMMEDIATE_ON if state == "on" else IMMEDIATE_OFF
            telnet = Telnet(hostname)
            login(telnet)
            control_outlet(telnet, switched_outlet, action)
            telnet.close()
            last_changed_time = time.time()

def login(t):
    t.read_until(b"User Name")
    t.write(username.encode("ascii") + b"\r\n")
    t.read_until(b"Password")
    t.write(password.encode("ascii") + b"\r\n")
    t.read_until(PROMPT)

def control_outlet(t, outlet, method):
    t.write(DEVICE_MANAGER)
    t.read_until(PROMPT)
    t.write(OUTLET_CONTROL)
    t.read_until(PROMPT)
    t.write(str(outlet).encode("ascii") + b"\r\n")
    t.read_until(PROMPT)
    t.write(method)
    t.read_until(b"Enter 'YES' to continue")
    t.write(b"YES\r\n")
    t.read_until(b"Press <ENTER>")
    t.write(b"\r\n")
    t.read_until(PROMPT)
    to_main_menu(t)

def to_main_menu(t):
    while True:
        t.write(b"\x1B") # ESC
        response = t.read_until(PROMPT)
        if b"Control Console" in response:
            return

if __name__ == "__main__":
    main()
