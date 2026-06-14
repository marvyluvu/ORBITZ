<h1 align="center">ORBITZ</h1>


<img width="1410" height="2000" alt="ORBITZ (2)" src="https://github.com/user-attachments/assets/81082f73-be17-4f3b-b523-16ac138b90c7" />


<p align="center">
  <i>Desktop satellite, plane, and ISS tracker with a Console-style display and LED halo.</i>
</p>

---

<h2>#1. What is ORBITZ</h2>

<p>
Its a desktop satellite, Plane and ISS tracker, it has a radar style round display, LED notifying ring, accurate satellite tracking and adaptable to any location you use it in!!
</p>

---

<h2>#2. Why did I make it?</h2>

<p>
I personally love astronomy and being able to stargaze outside with the stars, but I could never catch a satellite or the ISS due to how fast they orbit, so when I heard of FALLOUT by hackclub, I saw this as the perfect opportunity to work and bring my idea to life!!
</p>

---

<h2>#3. How does it work?</h2>

<p>
The brains of the operation is the Raspberry pi zero, it pulls telemetry data via CelesTrak, skyfield calculates the passes and it gets displayed on the screen and the led halo alerts you alongside buzzing with the built in buzzer, to make sure you dont miss it.
</p>

---

<h2>#4. How do you use it?</h2>

<p>
Plug it into usb c, Connect it to wifi, and it shows satellites and planes passing over your location
using the rotary dial and the button, you can scroll through targets and select them
</p>

---
<h2>#5. Firmware
  **CURRENT FIRMWARE IS MOCK/ TESTING REASONS ONLY**
  instructions for use
  1. open terminal in the root folder (orbitz_firmware)
  2. python -m venv .venv
  3. .\.venv\Scripts\Activate.ps1
  4. pip install -r requirements.txt
  5. python main.py
  
- Press `m` then Enter to switch modes (PLANES / ISS).
- Press `q` then Enter to quit.
  
<h2>#6. Images</h2>

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
