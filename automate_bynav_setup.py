#!/usr/bin/env python3

import serial
import time
import logging
import argparse
import json

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

def load_commands(file_path):
    try:
        with open(file_path, 'r') as file:
            commands = json.load(file)
        return commands
    except Exception as e:
        logging.error(f"Error reading JSON file {file_path}: {e}")
        return None

def send(command, ser):
    try:
        if isinstance(command, list):
            for cmd in command:
                logging.info(f"Sending command: {cmd}")
                ser.write((cmd + '\n').encode('utf-8'))
                time.sleep(1)
                response = ser.read_all().decode('utf-8').strip()
                logging.info(f"Response: \n{response}")
        elif command == "RTK_command":
            # Handle dynamic input for RTK setup
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            rtk_command = f"NTRIPCONFIG NCOM1 CLIENT V1 199.184.151.36:2101 RTK_SNUS_32 {username} {password} ALL"
            logging.info(f"Sending command: {rtk_command}")
            ser.write((rtk_command + '\n').encode('utf-8'))
            time.sleep(1)
            response = ser.read_all().decode('utf-8').strip()
            logging.info(f"Response: \n{response}")
    except serial.SerialException as e:
        logging.error(f"Error sending command '{command}': {e}")

def main():
    parser = argparse.ArgumentParser(description='Send commands to a Bynav device via serial port.')
    parser.add_argument('json_file', help='Path to the JSON file containing the commands.')
    args = parser.parse_args()

    commands = load_commands(args.json_file)
    if commands is None:
        logging.error("Failed to load commands from JSON file. Exiting.")
        return

    ser = config_serial_port()
    if ser is None:
        logging.error("Failed to configure serial port. Exiting.")
        return

    try:
        logging.info("Checking firmware version...")
        send(commands["check_firmware_version"], ser)

        logging.info("Configuring Static IP address...")
        send(commands["config_ip_address"], ser)

        logging.info("Setting ICOM port as TCP client...")
        send(commands["set_ICOM"], ser)

        skip_RTK = input("Do you want to skip RTK setup? (y/n): ").strip().lower()
        if skip_RTK != 'y':
            logging.info("Setting up RTK...")
            send(commands["setup_RTK"], ser)
        else:
            logging.info("Skipping RTK setup...")

        logging.info("Setting antenna lever arm and RBV parameters...")
        send(commands["set_antenna_lever_arm"], ser)

        logging.info("Adding logging topics to ICOM port...")
        send(commands["add_logging_topics"], ser)

        logging.info("Saving configuration...")
        send(commands["save_configuration"], ser)
    except KeyboardInterrupt:
        logging.warning("Keyboard interrupt received. Exiting...")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if ser.is_open:
            ser.close()
            logging.info("Serial port closed.")

if __name__ == "__main__":
    main()