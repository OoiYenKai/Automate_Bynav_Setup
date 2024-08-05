#!/usr/bin/env python3

import serial
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def config_serial_port():
    try:
        COM_port = input("Which COM port are you using (e.g., COM5)? ").strip()
        ser = serial.Serial(
            port=COM_port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        logging.info(f"Connected to {COM_port}")
        return ser
    except serial.SerialException as e:
        logging.error(f"Error opening serial port {COM_port}: {e}")
        return None
    
# Define the commands to be sent
commands = {
    "check_firmware_version": "LOG VERSION", # Check firmware version
    "config_ip_address": "IPCONFIG ETHA STATIC 192.168.2.152 255.255.255.0 192.168.2.1", # Configure the static IP address
    "set_ICOM": "ICOMCONFIG ICOM1 TCP :1111", # set ICOM port as TCP client
    "setup_RTK": "RTK_command", # RTK configuration
    # set antenna lever arm and RBV parameters
    "set_antenna_lever_arm": [
        "SETINSTRANSLATION ANT1 -0.43 0.0 0.8 0.05 0.05 0.05 VEHICLE",
        "SETINSTRANSLATION ANT2 0.43 0.0 0.8 0.05 0.05 0.05 VEHICLE",
        "SETINSTRANSLATION USER 0.0 -0.7 -0.6 0.05 0.05 0.05 VEHICLE",
        "SETINSROTATION RBV 0 0 0 0.05 0.05 0.05"
    ],
    # add logging topics to ICOM port
    "add_logging_topics": [
        "RAWIMUOUT ON",
        "LOG ICOM1 INSPVAXA ONTIME 0.008",
        "LOG ICOM1 CORRIMUDATAA ONNEW",
        "LOG ICOM1 INSSTDEVA ONTIME 0.008"
    ],
    # save configuration
    "save_configuration": "SAVECONFIG"
}

def send_command(command, ser):
    try:
        if command is "RTK_command":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            rtk_command = f"NTRIPCONFIG NCOM1 CLIENT V1 199.184.151.36:2101 RTK_SNUS_32 {username} {password} ALL"
            logging.info(f"Sending command: {rtk_command}")
            ser.write((rtk_command + '\n').encode('utf-8'))
            time.sleep(1)
            response = ser.read_all().decode('utf-8').strip()
            logging.info(f"Response: \n{response}")
        elif isinstance(command, list):
            for cmd in command:
                logging.info(f"Sending command: {cmd}")
                ser.write((cmd + '\n').encode('utf-8'))
                time.sleep(1)
                response = ser.read_all().decode('utf-8').strip()
                logging.info(f"Response: \n{response}")
        else:
            logging.info(f"Sending command: {command}")
            ser.write((command + '\n').encode('utf-8'))
            time.sleep(1)
            response = ser.read_all().decode('utf-8').strip()
            logging.info(f"Response: \n{response}")
    except serial.SerialException as e:
        logging.error(f"Error sending command '{command}': {e}")

def main():
    ser = config_serial_port()
    if ser is None:
        logging.error("Failed to configure serial port. Exiting.")
        return
    
    try:
        logging.info("Checking firmware version...")
        send_command(commands["check_firmware_version"], ser)

        logging.info("Configuring Static IP address...")
        send_command(commands["config_ip_address"], ser)

        logging.info("Setting ICOM port as TCP client")
        send_command(commands["set_ICOM"], ser)

        skip_RTK = input("Do you want to skip RTK setup? (yes/no): ").strip().lower()
        if skip_RTK != 'yes':
            logging.info("Setting up RTK...")
            send_command(commands["setup_RTK"], ser)
        else:
            logging.info("Skipping RTK setup...")
        
        logging.info("Setting antenna lever arm and RBV parameters...")
        send_command(commands["set_antenna_lever_arm"], ser)
    
        logging.info("Adding logging topics to ICOM port...")
        send_command(commands["add_logging_topics"], ser)

        logging.info("Saving configuration...")
        send_command(commands["save_configuration"], ser)
    except Exception as e:
        logging.error(f"An unexpected error occured: {e}")
    except KeyboardInterrupt as e:
        logging.error("Keyboard interrupt received. Exiting...")
    finally:
        if ser.is_open:
            ser.close()
            logging.info("Serial port closed.")

if __name__ == "__main__":
    main()