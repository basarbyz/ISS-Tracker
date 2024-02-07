# ISS Tracker Robot Arm

This project aims to build an ISS (International Space Station) tracker robot arm. The robot arm's pointer will show the real-time location of the ISS. The project utilizes a combination of Python and STM32 microcontroller programming.

## Overview

The project consists of two main parts:

1. **Python Code (`iss_tracker.py`):**
   - Fetches the ISS location data using the "Where the ISS at?" API.
   - Calculates the angles required for the robot arm to point towards the ISS.
   - Sends the calculated angles to the STM32 microcontroller using UART (Universal Asynchronous Receiver-Transmitter).

2. **STM32 Code (`main.c`):**
   - Receives the angles from Python via UART.
   - Controls the stepper motors of the robot arm to point towards the calculated angles.

## Hardware Components

- **Stepper Motors:** Two 17HS15-1504S-X1 stepper motors are used for the robot arm movement.
- **Stepper Motor Drivers:** Two A4988 stepper motor drivers are used to drive the stepper motors.
- **Limit Switches:** Two Panasonic AV-FS FS-T switches are used as limit switches for endstop detection.
- **Power Supply:** A 12V power supply is used to power the stepper motors and other components.
- **3D Printed Parts:** Various 3D printed parts are used to construct the robot arm.
- **Bearings:** Bearings are used for smooth movement of the robot arm.
- **CNC Shield:** The Arduino CNC Shield, as described in [this resource](https://blog.protoneer.co.nz/arduino-cnc-shield/), is used to interface between the STM32 board and the stepper motor drivers.

## Requirements

- STM32 development board.
- Python environment with `requests` library installed.
- USB cable for serial communication with the STM32 board.
- Arduino CNC Shield for stepper motor control.

## How to Use

1. **Setup STM32 Environment:**
   - Connect the stepper motors to the appropriate pins on the STM32 board.
   - Flash the provided STM32 code (`main.c`) onto your STM32 development board using your preferred development environment (e.g., STM32CubeIDE).

2. **Setup Python Environment:**
   - Ensure Python is installed on your system.
   - Install the required libraries by running `pip install -r requirements.txt`.
   
3. **Connect the Hardware:**
   - Connect the STM32 board to your computer using a USB cable.
   - Connect the stepper motors, limit switches, and power supply.

4. **Run the Python Script:**
   - Run the Python script (`iss_tracker.py`) on your computer.
   - The script will fetch the ISS location and send the angles to the STM32 board.

5. **Calibrate the Robot Arm:**
   - Before running the Python script, calibrate the robot arm to ensure accurate pointing.
   - After calibration, the pointer should point to the north direction.

6. **Monitor the Output:**
   - Monitor the output of the STM32 board to ensure that it receives the angles correctly.
   - Ensure that the robot arm moves accordingly to point towards the ISS location.


