# BOX hardware prototype

The saved prototype contains modules for the GPIO17 button, APA102 LEDs,
microphone recording, and playback through the Pi's 3.5 mm headphone jack.
It does not yet contain the cloud translation pipeline or a main application loop.

Connect with `ssh box_tech@BOXtech.local`. The home Wi-Fi SSID is
`head first if your not my fam `, including the final space.

The microphone device is `plughw:CARD=seeed2micvoicec,DEV=0` and the speaker
device is `plughw:CARD=Headphones,DEV=0`. Named devices avoid relying on ALSA
card numbers, which can change after a reflash.

Run hardware modules using the project environment:

```bash
cd ~/box-translator
source .venv/bin/activate
```

After compiling Seeed's v2.0 overlay in `~/seeed-linux-dtoverlays`, install it
and enable SPI/I2C with:

```bash
sudo bash ~/box-translator/scripts/restore-hardware.sh
```

The script backs up the boot configuration and reboots the Pi. It follows the
[official Seeed v2.0 instructions](https://wiki.seeedstudio.com/respeaker_2_mics_pi_hat_raspberry_v2/).

Always shut down before disconnecting power:

```bash
sudo shutdown -h now
```
