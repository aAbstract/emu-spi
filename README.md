# Emulated Serial Port Interface
This project provides an emulated serial port interface for testing purposes.

## Usage
```
./vspi_up.bash
```
1. Sets up two pseudo-tty devices /dev/ttyUSB0 and /dev/ttyUSB1 using socat. These act as serial port terminals.
2. Opens a TCP socket on port 6543 using socat that connects to /dev/ttyUSB0. This allows external applications to connect and communicate over the virtual bus.

```
python ./emu_spi.py
```

This will open the GUI window. Click "Connect" to connect to the VSPI server.  
The GUI allows sending commands and displays logging information.

You can then send these commands:  
- **wjs**: Send a JSON packet
- **wjsr**: Send a JSON packet with retain flag
