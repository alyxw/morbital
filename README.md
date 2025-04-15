# morbital.py

morbital.py is a work-in-progress python library for interacting with Matrix Orbital Human Machine Interfaces.

## Background

morbital requires a Matrix Orbital 19264 series HMI panel and a Linux system. It may work with other models of Matrix Orbital panels, but I only have the EGLK19264A-7T-USB-WB-PL available to test with.

The Matrix Orbital panel we use is a EGLK19264A-7T-USB-WB-PL, which identifies itself as the following:

```Bus 002 Device 002: ID 1b3d:01f1 MO EGLK19264-7T-USB```

```
T:  Bus=02 Lev=01 Prnt=01 Port=02 Cnt=01 Dev#=  2 Spd=12  MxCh= 0
D:  Ver= 2.00 Cls=00(>ifc ) Sub=00 Prot=00 MxPS= 8 #Cfgs=  1
P:  Vendor=1b3d ProdID=01f1 Rev=06.00
S:  Manufacturer=MO
S:  Product=EGLK19264-7T-USB
S:  SerialNumber=0xHygbs1
C:  #Ifs= 1 Cfg#= 1 Atr=80 MxPwr=500mA
I:  If#= 0 Alt= 0 #EPs= 2 Cls=ff(vend.) Sub=ff Prot=ff Driver=ftdi_sio
E:  Ad=02(O) Atr=02(Bulk) MxPS=  64 Ivl=0ms
E:  Ad=81(I) Atr=02(Bulk) MxPS=  64 Ivl=0ms
```

The panel presents itself as a simple serial device using the ftdi_sio driver, and has a default baud of 19200.


## Getting Started


Below is a basic script that utilizes the morbital.py library to print "Hello World" and listen to button presses.

```
import morbital
import asyncio

async def main():
    panel = MatrixOrbitalPanel("/dev/ttyUSB0")
    await panel.connect()
    
    panel.clear_display()
    panel.reset_cursor()

    panel.write_text("Hello World!")
    
    def on_button_press(char):
        print(f"Button pressed: {char}")
    
    panel.add_button_callback(on_button_press)
    
    try:
        await panel.listen_for_buttons()
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        panel.close()

if __name__ == "__main__":
    asyncio.run(main())
```
