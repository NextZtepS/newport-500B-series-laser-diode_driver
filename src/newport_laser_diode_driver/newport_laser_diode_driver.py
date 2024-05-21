import usb.core
import usb.util


class NewportLaserDiodeDriver:

    # Device Manual (USB interface is explained on Section 5 pg. 33)
    # https://www.newport.com/medias/sys_master/images/images/hbf/h21/8797013508126/500B-LDD-Users-Manual.pdf

    # Data Member
    _dev: usb.core.Device

    @property
    def identifier(self) -> str:
        """
        Get the identification string of the device.

        Returns:
            str: identification string
        """
        return self.get_identification()
    
    @property
    def key_switch_status(self) -> int:
        """
        Get the status of the key switch.

        Returns:
            int: 0 for OFF, 1 for ON
        """
        return self.get_key_switch_status()
    
    @property
    def hardware_temp(self) -> float:
        """
        Get the hardware temperature.

        Returns:
            float: temperature in Celsius
        """
        return self.get_hardware_temp()
    
    @property
    def current_set_point(self) -> float:
        """
        Get the current set point setting.

        Returns:
            float: current set point in mA
        """
        return self.get_current_set_point()
    
    @current_set_point.setter
    def current_set_point(self, current: float):
        """
        Set the current set point.

        Args:
            current (float): current set point in mA
        """
        self.set_current_set_point(current)

    @property
    def photodiode_current_set_point(self) -> float:
        """
        Get the photodiode current set point setting.

        Returns:
            float: photodiode current set point in mA
        """
        return self.get_photodiode_current_set_point()
    
    @photodiode_current_set_point.setter
    def photodiode_current_set_point(self, current: float):
        """
        Set the photodiode current set point.

        Args:
            current (float): photodiode current set point in mA
        """
        self.set_photodiode_current_set_point(current)

    @property
    def measured_current(self) -> float:
        """
        Get the measured current.

        Returns:
            float: measured current in mA
        """
        return self.get_measured_current()
    
    @property
    def current_limit(self) -> float:
        """
        Get the current limit setting.

        Returns:
            float: current limit in mA
        """
        return self.get_current_limit()
    
    @current_limit.setter
    def current_limit(self, current: float):
        """
        Set the current limit.

        Args:
            current (float): current limit in mA
        """
        self.set_current_limit(current)

    @property
    def laser_mode(self) -> str:
        """
        Get current laser mode.

        Returns:
            str: "Ilbw" constant current mode, low bandwidth; "Ihbw" constant current mode, high bandwidth; "Mdi" constant power mode
        """
        return self.get_laser_mode()
    
    @property
    def bandwidth_switch(self) -> int:
        """
        Get bandwidth switch setting.

        Returns:
            int: 0 for Low, 1 for High
        """
        return self.get_bandwidth_switch()
    
    @property
    def laser_output_enable(self) -> int:
        """
        Get current laser output enable status.

        Returns:
            int: 0 for OFF, 1 for ON
        """
        return self.get_laser_output_enable()
    
    @laser_output_enable.setter
    def laser_output_enable(self, enable: int):
        """
        Enable or disable laser output.

        Args:
            enable (int): 0 for OFF, 1 for ON
        """
        if enable:
            self.enable_laser_output()
        else:
            self.disable_laser_output()

    @property
    def laser_range(self) -> int:
        """
        Get current laser range setting.

        Returns:
            int: 0 for Low, 1 for High
        """
        return self.get_laser_range()
    
    @laser_range.setter
    def laser_range(self, rng: int):
        """
        Set laser range.

        Args:
            rng (int): 0 for Low, 1 for High
        """
        if rng:
            self.set_laser_range_high()
        else:
            self.set_laser_range_low()
    

    def __init__(self, idVendor=0x104d, idProduct=0x1001):
        """
        A constructor for the NewportLaserDiodeDriver class.

        Args:
            idVendor (hexadecimal, optional): Vendor Id of the device. Defaults to 0x104d.
            idProduct (hexadecimal, optional): Product Id of the device. Defaults to 0x1001.

        Raises:
            ValueError: No Device that matches the parameters found
        """
        self._dev = usb.core.find(idVendor=idVendor, idProduct=idProduct) # type: ignore
        if self._dev is None:
            raise ValueError('Device not found')
        else:
            print(f"Connected to {self._dev.manufacturer} {self._dev.product}")
            self._dev.set_configuration()

    def send_helper(self, cmd_str: str):
        """
        Helper function to send a command to the device. This device uses port 0x04 for sending commands.

        Args:
            cmd_str (str): string command to send
        """
        cmd_bytes = cmd_str.encode()
        self._dev.write(endpoint=0x04, data=cmd_bytes)

    def read_helper(self) -> str:
        """
        Helper function to read the response from the device. This device uses port 0x88 for reading responses.

        Returns:
            str: string equivalent of the response from the device
        """
        res_bytearray = self._dev.read(endpoint=0x88, size_or_buffer=64)
        res_str = bytes(res_bytearray).decode().replace("\r", "").replace("\n", "")
        # self.clear_buffer()
        return res_str

    def clear_buffer(self):
        """
        Clear status and response buffer 
        """
        self.send_helper("*CLS")
        print("Cleared buffer")

    def get_identification(self) -> str:
        """
        Ask for identification string of the device in a format of "NEWPORT XXXX vYYY mm/dd/yy, SNZZZZ"

        Returns:
            str: identification string ("NEWPORT XXXX vYYY mm/dd/yy, SNZZZZ")
        """
        self.send_helper("*IDN?")
        idn = self.read_helper()
        print(f"Identification: {idn}")
        return idn

    def recall_settings(self):
        """
        Restores the instrument to the (user) setup state which was last saved using save_setting() function.
        """
        self.send_helper("*RCL 2")
        print("Recalled user settings")

    def reset(self):
        """
        Reset the device to the default settings.
        """
        self.send_helper("*RST")
        print("Reset device")

    def save_settings(self):
        """
        Saves the current (user) settings.
        """
        self.send_helper("*SAV 2")
        print("Saved user settings")

    def get_status_byte(self) -> bytes:
        """
        Read the Status Byte Register.

        Returns:
            bytes: Status Byte Register
        """
        self.send_helper("*STB?")
        stb = bytes(self._dev.read(0x88, 64))
        print(f"Status byte: {stb}")
        return stb

    def set_address(self, address: int):
        """
        Set the USB address of the device.

        Args:
            address (int): USB address

        Raises:
            NotImplementedError: We do not support setting address since it requires reinitialization
        """
        print(f"Setting address requires the device to be reinitialized")
        raise NotImplementedError

    def get_address(self) -> int:
        """
        Acquire the USB address of the controller.

        Returns:
            int: Valid USB address from 0 to 99
        """
        self.send_helper("ADDR?")
        adr = self.read_helper()
        print(f"Address: {adr}")
        return int(adr)

    def get_error(self) -> tuple[str, str]:
        """
        Get error code and its description.

        Returns:
            tuple[str, str]: error code and its description
        """
        self.send_helper("ERRSTR")
        err = self.read_helper()
        ERR_DICT = {
            "0": "No error",
            "099": "Firmware not valid",
            "115": "Identifier not valid",
            "200": "Remote Mode",
            "201": "Value Out of Range",
            "501": "Interlock Error",
            "502": "Hard Current Limit Error",
            "505": "Comp Voltage Limit Error",
            "513": "Range Change",
            "514": "Mode Change",
            "901": "System Over Temperature Error",
            "902": "Laser Enable Off"
        }
        print(f"Error code: {err} means {ERR_DICT[err]}")
        return err, ERR_DICT[err]

    def return_to_local(self):
        """
        Return to local mode from USB remote, so that the front panel can be used.
        """
        self.send_helper("LOCAL")
        print("Return to local mode (from USB remote)")

    def get_key_switch_status(self) -> int:
        """
        Get the status of the key switch.

        Returns:
            int: 0 for OFF, 1 for ON
        """
        self.send_helper("KEY?")
        key_status = self.read_helper()
        print(f"Key switch status: {key_status}")
        return int(key_status)

    def get_hardware_temp(self) -> float:
        """
        Get the hardware temperature.

        Returns:
            float: temperature in Celsius
        """
        self.send_helper("HWT?")
        temp = self.read_helper()
        print(f"Hardware temperature: {float(temp):.2f} C")
        return float(temp)

    def set_current_set_point(self, current: float):
        """
        Set the current set point.

        Args:
            current (float): current set point in mA
        """
        self.send_helper(f"LAS:LDI {current}")
        print(f"Set current set point to {current} mA")

    def get_current_set_point(self) -> float:
        """
        Get the current set point setting.

        Returns:
            float: current set point in mA
        """
        self.send_helper("LAS:SET:LDI?")
        current = self.read_helper()
        print(f"Current set point: {float(current):.2f} mA")
        return float(current)

    def get_measured_current(self) -> float:
        """
        Get the measured current.

        Returns:
            float: measured current in mA
        """
        self.send_helper("LAS:LDI?")
        current = self.read_helper()
        print(f"Measured current: {float(current):.2f} mA")
        return float(current)

    def set_photodiode_current_set_point(self, current: float):
        """
        Set the photodiode current set point.

        Args:
            current (float): photodiode current set point in mA
        """
        self.send_helper(f"LAS:MDI {current}")
        print(f"Set photodiode current set point to {current} mA")

    def get_photodiode_current_set_point(self) -> float:
        """
        Get the photodiode current set point setting.

        Returns:
            float: photodiode current set point in mA
        """
        self.send_helper("LAS:SET:MDI?")
        current = self.read_helper()
        print(f"Photodiode current set point: {float(current):.2f} mA")
        return float(current)

    def get_measured_photodiode_current(self) -> float:
        """
        Get the measured photodiode current.

        Returns:
            float: measured photodiode current in mA
        """
        self.send_helper("LAS:MDI?")
        current = self.read_helper()
        print(f"Measured photodiode current: {float(current):.2f} mA")
        return float(current)

    def get_measured_forward_voltage(self) -> float:
        """
        Get measured forward voltage.

        Returns:
            float: measured voltage in V
        """
        self.send_helper("LAS:LDV?")
        voltage = self.read_helper()
        print(f"Measured forward voltage: {float(voltage):.2f} V")
        return float(voltage)

    def set_current_limit(self, current: float):
        """
        Set the current limit.

        Args:
            current (float): current limit in mA
        """
        self.send_helper(f"LAS:LIM:LDI {current}")
        print(f"Set current limit to {current} mA")

    def get_current_limit(self) -> float:
        """
        Get the current limit setting.

        Returns:
            float: current limit in mA
        """
        self.send_helper("LAS:LIM:LDI?")
        current = self.read_helper()
        print(f"Current limit: {float(current):.2f} mA")
        return float(current)

    def get_laser_mode(self) -> str:
        """
        Get current laser mode.

        Returns:
            str: "Ilbw" constant current mode, low bandwidth; "Ihbw" constant current mode, high bandwidth; "Mdi" constant power mode
        """
        self.send_helper("LAS:MODE?")
        mode = self.read_helper()
        print(f"Laser mode: {mode}")
        return mode

    def enter_constant_current_mode(self):
        """
        Enter constant current mode.
        """
        self.send_helper("LAS:MODE:I")
        print("Entered constant current mode")

    def enter_constant_photodiode_current_mode(self):
        """
        Enter constant photodiode current mode.
        """
        self.send_helper("LAS:MODE:MDI")
        print("Entered constant photodiode current mode")

    def get_bandwidth_switch(self) -> int:
        """
        Get bandwidth switch setting.

        Returns:
            int: 0 for Low, 1 for High
        """
        self.send_helper("LAS:MODE:BW?")
        bw = self.read_helper()
        print(f"Bandwidth switch: {int(bw)}")
        return int(bw)

    def disable_laser_output(self):
        """
        Disable laser output.
        """
        self.send_helper("LAS:OUT 0")
        print("Disabled laser output")

    def enable_laser_output(self):
        """
        Enable laser output.
        """
        self.send_helper("LAS:OUT 1")
        print("Enabled laser output")

    def get_laser_output_enable(self) -> int:
        """
        Get current laser output enable status.

        Returns:
            int: 0 for OFF, 1 for ON
        """
        self.send_helper("LAS:OUT?")
        enable = self.read_helper()
        print(f"Laser enable: {int(enable)}")
        return int(enable)

    def get_laser_range(self) -> int:
        """
        Get current laser range setting.

        Returns:
            int: 0 for Low, 1 for High
        """
        self.send_helper("LAS:RANGE?")
        rng = self.read_helper()
        print(f"Laser range: {int(rng)}")
        return int(rng)

    def set_laser_range_low(self):
        """
        Set laser range to Low.
        """
        self.disable_laser_output()
        self.send_helper("LAS:RANGE 0")
        print(f"Set laser range to Low")

    def set_laser_range_high(self):
        """
        Set laser range to High.
        """
        self.disable_laser_output()
        self.send_helper("LAS:RANGE 1")
        print(f"Set laser range to High")
