# ORBITZ

<p align="center">
  <img width="1410" height="2000" alt="ORBITZ" src="https://github.com/user-attachments/assets/e5b121f1-b345-42a9-9820-a517a4ea93c1" />
</p>

<p align="center"><i>Desktop satellite, plane, and ISS tracker with a Console-style display and LED halo.</i></p>

---

## 1. What is ORBITZ?

ORBITZ is a desktop satellite, plane, and ISS tracker built on a Raspberry Pi Zero 2W. It features a radar-style LCD display, internal RGB LED lighting, accurate real-time satellite tracking, and is adaptable to any location in the world.

---

## 2. Why did I make it?

I personally love astronomy and being able to stargaze outside. I could never catch a satellite or the ISS due to how fast they orbit, so when I heard of FALLOUT by Hackclub, I saw this as the perfect opportunity to bring my idea to life.

---

## 3. How does it work?

The brain of the operation is the Raspberry Pi Zero 2W. It pulls live telemetry data via CelesTrak, Skyfield calculates satellite passes and positions, and the results are displayed on the ILI9341 LCD screen. The internal RGB strip and built-in buzzer alert you so you never miss a pass.

---

## 4. How do you use it?

1. Plug in via USB-C and connect to Wi-Fi.
2. ORBITZ automatically tracks satellites and planes passing over your location.
3. Use the rotary encoder and button to scroll through targets and select them.
4. The RGB strip indicates tracking status:
   - Blue blinking = planes detected
   - Green blinking = ISS currently above horizon
   - Off = nothing currently visible

---

## 5. Firmware

> **WARNING: Current firmware is MOCK / TESTING ONLY.**
> Runs on any PC or Raspberry Pi, without the custom PCB or display.

### How to run (Windows / PowerShell)

From the `orbitz_firmware/` folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

**Controls:**
- Press `m` then Enter to switch modes (PLANES / ISS).
- Press `q` then Enter to quit.

---

## 6. Bill of Materials (BOM)

Full BOM is in the [`BOM/`](BOM/) folder.

### Key components

| Part | Description | Qty |
|---|---|---|
| Raspberry Pi Zero 2W | Main computer and network | 1 |
| 2.4" ILI9341 SPI LCD (no touch) | Radar / UI display | 1 |
| WS2812B RGB LED strip | Internal status lighting | 1 |
| TP4056 LiPo charger | Charges battery via USB-C | 1 |
| MT3608 boost converter | Boosts 3.7V LiPo to 5V for Pi | 1 |
