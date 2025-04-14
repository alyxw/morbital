import serial
import asyncio


class MatrixOrbitalPanel:
    def __init__(self, port="/dev/ttyUSB1", baudrate=19200):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.button_callbacks = []
        self._running = False

    async def connect(self):
        # connect to the serial port
        self.serial = serial.Serial(
            self.port,
            self.baudrate,
            serial.EIGHTBITS,
            serial.PARITY_NONE,
            serial.STOPBITS_ONE,
            timeout=0,
            rtscts=False
        )
        if not self.serial.is_open:
            self.serial.open()
        print(f"Connected to Matrix Orbital 19264 panel on {self.port}")
        return self

    def close(self):
        # close the serial connection
        if self.serial and self.serial.is_open:
            self.serial.close()
        self._running = False

    def send_action(self, payload):
        # send raw bytes to the panel
        if not self.serial or not self.serial.is_open:
            raise Exception("Serial connection not established")
        self.serial.write(serial.to_bytes(payload))

    def clear_display(self):
        # Clear the display content
        payload = [0xFE, 0x58]
        self.send_action(payload)

    def reset_cursor(self):
        # Send the cursor to the top left corner
        payload = [0xFE, 0x48]
        self.send_action(payload)

    async def reset_display(self):
        # Perform a soft reset of the display
        payload = [0xFE, 0xFD, 0x4D, 0x4F, 0x75, 0x6E]
        self.send_action(payload)
        await asyncio.sleep(4)

    def set_cursor_position(self, x, y):
        # Set cursor to specific row/column
        if x < 1 or x > 27 or y < 1 or y > 8:
            raise Exception("The position specified is out of range.")
        payload = [0xFE, 0x47, x, y]
        self.send_action(payload)

    def set_cursor_coordinate(self, x, y):
        # Set cursor to specific pixel position
        if x < 1 or x > 192 or y < 1 or y > 64:
            raise Exception("The coordinate specified is out of range.")
        payload = [0xFE, 0x79, x, y]
        self.send_action(payload)

    def keypad_backlight_off(self):
        # Turn off the keypad backlight
        payload = [0xFE, 0x9B]
        self.send_action(payload)

    def keypad_backlight_on(self):
        # set keypad backlight to default 255 to turn on
        self.set_keypad_backlight_brightness(255)

    def set_keypad_backlight_brightness(self, brightness):
        # Set keypad backlight brightness
        if brightness < 0 or brightness > 255:
            raise Exception("The brightness specified is out of range.")
        payload = [0xFE, 0x9C, brightness]
        self.send_action(payload)

    def display_backlight_off(self):
        # Turn off the display backlight
        payload = [0xFE, 0x46]
        self.send_action(payload)

    def display_backlight_on(self, minutes):
        # Turn on display backlight for specified minutes
        if minutes > 255 or minutes < 0:
            raise Exception("minutes out of range")
        payload = [0xFE, 0x42, minutes]
        self.send_action(payload)

    def set_backlight_brightness(self, brightness):
        # Set display backlight brightness
        if brightness < 0 or brightness > 255:
            raise Exception("brightness out of range")
        payload = [0xFE, 0x99, brightness]
        self.send_action(payload)

    def set_startup_backlight_brightness(self, brightness):
        # Set startup backlight brightness
        if brightness < 0 or brightness > 255:
            raise Exception("brightness out of range")
        payload = [0xFE, 0x98, brightness]
        self.send_action(payload)

    def set_display_contrast(self, contrast):
        # Set display contrast
        if contrast < 0 or contrast > 255:
            raise Exception("contrast out of range")
        payload = [0xFE, 0x50, contrast]
        self.send_action(payload)

    def set_startup_display_contrast(self, contrast):
        # set startup display contrast
        if contrast < 0 or contrast > 255:
            raise Exception("contrast out of range")
        payload = [0xFE, 0x91, contrast]
        self.send_action(payload)

    def set_device_led(self, led, colour):
        # Set LED color (LED: 0-2, color: 0-3)
        # 0: off, 1: green, 2: red, 3: amber
        if led < 0 or led > 2 or colour > 3 or colour < 0:
            raise Exception("LED must be 0-2 and color must be 0-3")
        payload = [0xFE, 0x5A, led, colour]
        self.send_action(payload)

    def write_text(self, text):
        # Write text to the display
        self.send_action(text.encode('utf-8'))

    def add_button_callback(self, callback):
        # button press callback
        self.button_callbacks.append(callback)

    def write_line(self, line, text):
        self.set_cursor_position(1, line)
        self.write_text(text)
        self.reset_cursor()

    def set_current_font(self, font):
        # set font, default 0x01 is Small Filled, default 0x02 is Futura Bk BT 16
        # using these might render text display until you run a reset_display and reinitialize,
        #  not all panels have properly preloaded fonts
        payload = [0xFE, 0x31, font]
        self.send_action(payload)

    async def listen_for_buttons(self):
        self._running = True
        while self._running:
            if self.serial and self.serial.in_waiting > 0:
                data = self.serial.read(1)
                try:
                    char = data.decode('utf-8')
                    for callback in self.button_callbacks:
                        callback(char)
                except UnicodeDecodeError:
                    print(f"Received non-UTF8 data: {data.hex()}")
            await asyncio.sleep(0.01)
