<h1 align="center">ORBITZ</h1>

<img width="1410" height="2000" alt="ORBITZ (3)" src="https://github.com/user-attachments/assets/e5b121f1-b345-42a9-9820-a517a4ea93c1" />



<p align="center">
  <i>Desktop satellite, plane, and ISS tracker with a Console-style display and LED halo.</i>
</p>

---

##  1. What is ORBITZ

<p>
Orbit is a desktop satellite, plane, and ISS tracker with a radar-style display, LED halo, live ADS-B plane data, and GPS aware tracking
</p>

---

##  2. Why did I make it?

<p>
I personally love astronomy and being able to stargaze outside with the stars, but I could never catch a satellite or the ISS due to how fast they orbit, so when I heard of FALLOUT by hackclub, I saw this as the perfect opportunity to work and bring my idea to life!!
</p>

---

##  3. How does it work?

<p>
The brains of the operation is a Raspberry Pi Zero 2W. 
    It:

    Fetches TLEs from CelesTrak and uses Skyfield to compute live satellite and ISS passes.
    Reads your location from GPSD (USB GPS) or falls back to a configured location.
    Receives live ADS‑B aircraft data either from a local RTL‑SDR + dump1090 or from the OpenSky API.
    The display shows a radar view, the LED halo indicates visibility, and the buzzer alerts you before passes so you don’t miss them.
</p>

---

##  4.Hardware schematic

<p>
You can view the full schematic for the ORBITZ PCB below.
  
![ORBITZ schematic](hardware/orbitz_schematic.svg)
</p>

---

##  5. How do you use it?

<p>
Plug it into usb c, Connect it to wifi, and it shows satellites and planes passing over your location
using the rotary dial and the button, you can scroll through targets and select them

If you plug in the USB GPS AND SDR DONGLE, Orbitz will automagically :
use gpsd for your location
use live ADS-B data from planes flying nearby for fully local tracking (or fall back to Opensky if no receiver is present)
</p>

Assembly:

1. First print the enclosure, and order all the items in the BOM.
2. Insert heat inserts in all screw standoffs.
3. insert battery into pcb.
4. insert pcb into enclosure, and make sure the battery is UNDER the pcb.
5. screw in pcb board.
6. attach screen with screws (MAKE SURE ITS ORIENTED PROPERLY with the row of pins pointing upwards
7. insert joystick and wire to the pcb
8. cut rgb strip to size, then stick near the top of the enclosure.
9. wire rgb strip to pcb board.
10. Attach acrylic lid and back.
11. using super glue, attach the usb hub to the slot.
12. connect both the GPS and SDR dongle to the usb hub.
13. connect to power, flash firmware and enjoy!

## ASSEMBLED DESIGN 
Below is what your fully assembled design should look like.

![ORBITZ enclosure interior](hardware/orbitz_case_interior.png)  

---

## 6. Firmware

There are two ways to run ORBITZ:

### 6.1 Desktop/mock firmware (no hardware required)

This runs the radar UI in a Pygame window on any PC or Pi, using mock drivers instead of the real display, LEDs, and buttons.

How to run (Windows / PowerShell):

1. Open a terminal in the `firmware` folder.
2. `python -m venv .venv`
3. `.\.venv\Scripts\Activate.ps1`
4. `pip install -r requirements.txt`
5. `python main.py`

Controls in mock mode:

- `m` + Enter: toggle between PLANES and SATS/ISS modes.
- `j` / `k` + Enter: move selection to next/previous target.
- `q` + Enter: quit.

### 6.2 Hardware firmware (Pi + PCB)

On the Pi Zero 2W with the ORBITZ PCB attached:

- The display shows the radar UI.
- The rotary encoder controls target selection.
- The encoder button toggles modes.
- The LED halo and buzzer reflect visibility/alerts.
- GPSD and dump1090/readsb are used automatically if available.

##  7. Images

<table>
  <tr>
    <td align="center">
      <strong>FINAL PCB SCREENSHOTS</strong><br><br>
      <img width="400" alt="FINAL PCB SCREENSHOTS"
        src="https://github.com/user-attachments/assets/bd019cbe-858b-401e-93b5-4572d05ddfc6" />
    </td>
  </tr>
  <tr>
    <td align="center">
      <strong>PCB</strong><br><br>
      <img width="400" alt="PCB"
        src="https://github.com/user-attachments/assets/b6102816-e6c7-4078-b330-d672943b4513" />
    </td>
  </tr>
  <tr>
    <td align="center">
      <strong>FINAL BUILD</strong><br><br>
      <img width="300" alt="FINAL BUILD"
        src="https://github.com/user-attachments/assets/b351456f-1b2b-45ee-8724-4b84135ccd16" />
    </td>
  </tr>
</table>

##  8. Bill of Materials (BOM)

The full detailed BOM is included in this repository:

- [`/ORBITZ_BILL_OF_MATERIALS.csv`](https://github.com/marvyluvu/ORBITZ/blob/main/hardware/BOM.csv)

You can open this file in Excel, Google Sheets, or any spreadsheet tool.
It includes part names, descriptions, quantities, prices, and direct purchase links.

Key components

| Product name          | Description                                      | Qty |
|-----------------------|--------------------------------------------------|-----|
| Raspberry Pi Zero 2W  | Main computer, runs satellite tracking software  | 1   |
| 2.4" NO TOUCH ILI9341| SPI LCD display for Orbitz radar UI              | 1   |
| WS2812B LED STRIP     | Internal RGB status lighting (1 m)              | 1   |
| RTL‑SDR USB dongle    | ADS‑B receiver for local aircraft (dump1090)    | 1   |
| USB GPS dongle (VK‑172 or similar) | Provides live GPS position via GPSD | 1   |
