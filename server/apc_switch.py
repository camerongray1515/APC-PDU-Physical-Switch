from telnetlib import Telnet

# BEGIN CONFIG
username = "apc"
password = "apc"
hostname = "10.0.2.161"
# END CONFIG

# Menu options
DEVICE_MANAGER = b"1\r\n"
CONTROL_OUTLET = b"1\r\n"
OUTLET_CONTROL = b"3\r\n"
IMMEDIATE_ON = b"1\r\n"
IMMEDIATE_OFF = b"2\r\n"
IMMEDIATE_REBOOT = b"3\r\n"
PROMPT = b">"

def main():
    telnet = Telnet(hostname)
    login(telnet)
    for i in range(1,9):
        control_outlet(telnet, i, IMMEDIATE_REBOOT)

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
    t.write(CONTROL_OUTLET)
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
