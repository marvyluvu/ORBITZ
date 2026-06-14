<h1 align="center">ORBITZ</h1>

<img width="1410" height="2000" alt="ORBITZ (3)" src="https://github.com/user-attachments/assets/e5b121f1-b345-42a9-9820-a517a4ea93c1" />



<p align="center">
  <i>Desktop satellite, plane, and ISS tracker with a Console-style display and LED halo.</i>
</p>

---

#  1. What is ORBITz

<p>
Its a desktop satellite, Plane and ISS tracker, it has a radar style round display, LED notifying ring, accurate satellite tracking and adaptable to any location you use it in!!
</p>

---

#  2. Why did I make it?

<p>
I personally love astronomy and being able to stargaze outside with the stars, but I could never catch a satellite or the ISS due to how fast they orbit, so when I heard of FALLOUT by hackclub, I saw this as the perfect opportunity to work and bring my idea to life!!
</p>

---

#  3. How does it work?

<p>
The brains of the operation is the Raspberry pi zero, it pulls telemetry data via CelesTrak, skyfield calculates the passes and it gets displayed on the screen and the led halo alerts you alongside buzzing with the built in buzzer, to make sure you dont miss it.
</p>

---

#  4. How do you use it?

<p>
Plug it into usb c, Connect it to wifi, and it shows satellites and planes passing over your location
using the rotary dial and the button, you can scroll through targets and select them</p>

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
11. connect to power, flash firmware and enjoy!

---

#  5. Firmware
  **WARNING**: CURRENT FIRMWARE IS MOCK/ TESTING REASONS ONLY
  Runs on any pc or rpi, without the custom pcb or display

  How to run (Windows / PowerShell)
  1) open terminal in the root folder (firmware)
  2) python -m venv .venv
  3) .\.venv\Scripts\Activate.ps1
  4) pip install -r requirements.txt
  5) python main.py

- Press `m` then Enter to switch modes (PLANES / ISS).
- Press `q` then Enter to quit.

#  6. Images

#  7. Bill of Materials (BOM)

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
| TP4056 LiPo charger   | Charges LiPo battery from USB-C                 | 1   |
| MT3608 boost converter| Boosts 3.7 V LiPo to 5 V for Pi                 | 1   |
