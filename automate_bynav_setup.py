#!/usr/bin/env python3

import serial
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def config_serial_port():
    try:
        COM_Port = input("Which COM port are you using (e.g., COM5)? ").strip()
        ser = serial.Serial(
            port=COM_Port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        logging.info(f"Connected to {COM_Port}")
        return ser
    except serial.SerialException as e:
        logging.error(f"Error opening serial port {COM_Port}: {e}")
        return None

# Define the commands to be sent
commands = [
    "LOG VERSION",  # Check firmware version
    "IPCONFIG ETHA STATIC 192.168.2.152 255.255.255.0 192.168.2.1",  # Configure the static IP address
    "ICOMCONFIG ICOM1 TCP :1111",  # Set ICOM port as TCP client
    # Set antenna lever arm and RBV parameters
    "SETINSTRANSLATION ANT1 -0.43 0.0 0.8 0.05 0.05 0.05 VEHICLE",
    "SETINSTRANSLATION ANT2 0.43 0.0 0.8 0.05 0.05 0.05 VEHICLE",
    "SETINSTRANSLATION USER 0.0 -0.7 -0.6 0.05 0.05 0.05 VEHICLE",
    "SETINSROTATION RBV 0 0 0 0.05 0.05 0.05",
    # Add logging topics to ICOM port
    "RAWIMUOUT ON",
    "LOG ICOM1 INSPVAXA ONTIME 0.008",
    "LOG ICOM1 CORRIMUDATAA ONNEW",
    "LOG ICOM1 INSSTDEVA ONTIME 0.008",
    # Save configuration
    "SAVECONFIG"
]

def send_command(command, ser):
    try:
        logging.info(f"Sending command: {command}")
        ser.write((command + '\n').encode('utf-8'))
        time.sleep(1)
        response = ser.read_all().decode('utf-8').strip()
        logging.info(f"Response: \n{response}")
    except serial.SerialException as e:
        logging.error(f"Error sending command '{command}': {e}")

def check_firmware_version(ser):
    send_command(commands[0], ser)

def config_ip_address(ser):
    send_command(commands[1], ser)

def set_ICOM(ser):
    send_command(commands[2], ser)

def setup_RTK(ser):
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    rtk_command = f"NTRIPCONFIG NCOM1 CLIENT V1 199.184.151.36:2101 RTK_SNUS_32 {username} {password} ALL"
    send_command(rtk_command, ser)

def set_antenna_lever_arm(ser):
    for command in commands[3:7]:
        send_command(command, ser)

def add_logging_topics(ser):
    for command in commands[7:11]:
        send_command(command, ser)

def save_configuration(ser):
    send_command(commands[11], ser)

def main():
    ser = config_serial_port()
    if ser is None:
        logging.error("Failed to configure serial port. Exiting.")
        return

    try:
        logging.info("Checking firmware version...")
        check_firmware_version(ser)

        logging.info("Configuring Static IP address...")
        config_ip_address(ser)

        logging.info("Setting ICOM port as TCP client...")
        set_ICOM(ser)

        logging.info("Setting up RTK...")
        setup_RTK(ser)

        logging.info("Setting antenna lever arm and RBV parameters...")
        set_antenna_lever_arm(ser)

        logging.info("Adding logging topics to ICOM port...")
        add_logging_topics(ser)

        logging.info("Saving configuration...")
        save_configuration(ser)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if ser.is_open:
            ser.close()
            logging.info("Serial port closed.")

if __name__ == "__main__":
    main()