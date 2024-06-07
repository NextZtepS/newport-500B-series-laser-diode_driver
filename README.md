# Newport Model 300-500B Series Laser Diode Driver Python USB Package (for Linux)


This package is developed within the advisory of the Gallicchio Research Group, Harvey Mudd College.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Pre-requisites](#pre-requisites)
- [Set-up](#set-up)
  - [Allow the Newport Laser Diode Driver USB device to be managed by Python](#allow-the-newport-laser-diode-driver-usb-device-to-be-managed-by-python)
- [Usage](#usage)
- [Compatibility and Testing](#compatibility-and-testing)
- [Troubleshooting](#troubleshooting)

## Pre-requisites

- Permission to connect to the Newport Laser Diode Driver USB device
- Python version >= 3


## Set-up

### Allow the Newport Laser Diode Driver USB device to be managed by Python

Run the Run the following shell command:

```shell
usb-devices  # this allows us to see the idVendor and idProduct of all USB devices 
```

Ensure that the idVendor and idProduct match the example below unless change the idVendor and idProduct to the appropriate values. The process below grants permission for our package to manage the specified Newport USB device.

Run the following shell command:

```shell
cd /etc/udev/rules.d/ ;
sudo vim 99-usb-permissions.rules ;  # you can use other text editor of your choosing
```

Copy & paste the following lines into the file: 

```
# Newport Model 300-500B Series Laser Diode Driver
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="104d", ATTRS{idProduct}=="1001", MODE="0666"
```

Then, type `:wq` and press `ENTER` to save the changes and close the file

Run the following shell command:

```shell
sudo udevadm control --reload ;
sudo udevadm trigger ;
```


## Usage

In your desired Python environment, run the following shell command:

```shell
pip install newport-laser-diode-driver
```

Here is an example snippet of how a Laser Driver object could be instantiated:

```python
from newport_laser_diode_driver import NewportLaserDiodeDriver

model_535B = NewportLaserDiodeDriver(idVendor=0x104d, idProduct=0x1001)

print(model_535B.identifier)  # obtain the identification string of the device

model_535B.set_current_set_point(10.0)  # set current set point to be 10.0 mA
current = model_535B.get_current_set_point()  # get the current set point
print(current)  # 10.0
model_535B.enable_laser_output()  # enable laser output
```


## Compatibility and Testing

I have tested this package with the Newport Model 500B Series devices that I have accessed including 505B and 535B. On paper, this package should work with Model 300B Series as well; however, I have no access to the devices to test them out.


## Troubleshooting

To check if the device is recognized by the PC, run `usb-devices` to list all USB devices connected to your PC. If the Newport device is not found, try connecting the USB cable from the device to your PC first and then restart the Newport device.
