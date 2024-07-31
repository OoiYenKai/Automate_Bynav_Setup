# Bynav Automation Script
## Overview
The Bynav Automation Script is designed to streamline the setup process for Bynav devices. This script automates the configuration steps, reducing setup time and minimizing the potential for human error. It includes features such as error handling, logging, and resource management to ensure a reliable and efficient workflow.

## Features
- **Automated Serial Communication**: Configures the serial port based on specified settings.
- **Command Execution**: Sends configuration commands to the Bynav device.
- **Response Verification**: Reads and interprets responses from the device to confirm successful command execution.
- **Error Handling**: Catches and logs errors to prevent crashes and provide diagnostic information.
- **Resource Management**: Ensures that serial port connections are properly closed.
- **Modular Design**: Organized functions for easier maintenance and testing.
## Requirements
- Python 3.x
- **pyserial** library
- Access to a Bynav device
## Installation
1. **Clone the Repository**:
```
git clone https://github.com/yourusername/bynav-automation.git
cd bynav-automation
```
2. **Install Required Packages**:
```
pip install -r requirements.txt
```

## Configuration
Before running the script, ensure the serial port is correctly set up:

- **Baud Rate**: 115200
- **Parity Bits**: None
- **Stop Bits**: 1
- **Data Bits**: 8

These settings are configured in the script and match the Bynav device's requirements.

## Usage
1. **Setup the Serial Port**:

Ensure the Bynav device is connected to your machine. The serial port should be set according to the device's specifications.
Type "device manager" in start to find what COM port is the Bynav connected to.

2. **Run the Script**:

Execute the script by running:
```python3 bynav_setup.py```

3. **Follow the On-Screen Instructions**:

The script will prompt for any necessary input, such as the COM port.

4. **Monitor Output**:

The script will log detailed information about the setup process, including any errors or warnings. Ensure that the commands are executed successfully and that the responses from the Bynav device are as expected.

## Troubleshooting
- **No Response from Device**: Ensure that the Bynav device is correctly connected and that the COM port is specified correctly.
- **Connection Issues**: Verify that the serial port settings match those required by the Bynav device.

## Contact
For any questions or issues, please contact **@Yen Kai** on slack.