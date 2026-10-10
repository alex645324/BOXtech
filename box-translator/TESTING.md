# Testing BOX — Beginner Guide

This assumes you know nothing about any of this. Follow it top to bottom, in order. Don't skip ahead.

**What you need in front of you:** your Mac, your iPhone, and the Pi (with the HAT and the new speaker already plugged into it) connected to power.

---

## Step 1 — Turn on the phone hotspot

1. On your iPhone, open **Settings**.
2. Tap **Personal Hotspot**.
3. Turn the toggle at the top **on** (it turns green).
4. Leave this screen open — you'll check it again later. Note the wifi password shown on this screen if you don't already know it.

---

## Step 2 — Power on the Pi

The Pi only looks for wifi once, right when it turns on. So the hotspot must already be on (Step 1) **before** you plug the Pi in.

1. Plug the Pi's power cable in.
2. Wait about 30–60 seconds for it to fully boot.
3. Go back to the iPhone's Personal Hotspot screen — you should see a device listed under "Connect To..." or a similar section. That means the Pi joined successfully.

If nothing shows up there after a minute, the Pi didn't join — unplug it, wait 10 seconds, plug it back in, and check again.

---

## Step 3 — Connect your Mac to the same network

1. On your Mac, click the wifi icon in the top-right menu bar.
2. Click the network named **boxnet**.
3. Type in the hotspot password from Step 1.
4. Wait until it shows as connected.

---

## Step 4 — Open Terminal on your Mac

Terminal is the black-and-white window where you type text commands instead of clicking things.

1. Press `Cmd + Space`.
2. Type `Terminal`.
3. Press Enter.

A window opens with some text and a blinking cursor. That's where every command below gets typed or pasted.

---

## Step 5 — Copy the code onto the Pi

Paste this into the Terminal window and press Enter:

```bash
scp -r /Users/alexpozo/development/BOXtech/box-translator box_tech@BOXtech.local:~/
```

What happens next, in order:
- It may ask: `Are you sure you want to continue connecting (yes/no)?` — type `yes`, press Enter.
- It asks for a password — type the `box_tech` account password (nothing will appear on screen as you type, not even dots — that's normal), press Enter.
- You'll see a list of file names scroll by with percentages. When it stops and gives you a new line, it's done.

**If you see a big red warning about "REMOTE HOST IDENTIFICATION HAS CHANGED"** — this only happens after the SD card has been re-flashed, and it just means your Mac remembers an old version of the Pi. Run this, then try the `scp` command again:
```bash
ssh-keygen -R BOXtech.local
```

---

## Step 6 — Log into the Pi

```bash
ssh box_tech@BOXtech.local
```

Type the password again when asked. Once it logs in, you'll see a welcome message and a new prompt that looks like:
```
box_tech@BOXtech:~ $
```

Everything from here on, you type **inside this Pi session**, not back on your Mac.

---

## Step 7 — Install the software the code needs

Only needs to be done once (skip this if you've already done it successfully before and haven't re-flashed the SD card since).

```bash
cd ~/box-translator
```

```bash
sudo apt install -y python3-pip
```

```bash
pip install --break-system-packages -r requirements.txt
```

---

## Step 8 — Test the LEDs

Paste this whole block and watch the 3 little LEDs on the HAT:

```bash
cd ~/box-translator
python3 - <<'EOF'
import time
from hardware import leds

print("should be RED")
leds.idle()
time.sleep(2)

print("should be GREEN")
leds.listening()
time.sleep(2)

print("should be AMBER")
leds.working()
time.sleep(2)

print("should be BLUE")
leds.speaking()
time.sleep(2)

print("should FLASH RED 3 times then go dark")
leds.error()

print("led test done")
EOF
```

If the colors match what's printed, this works.

---

## Step 9 — Test the button

Paste this whole block, then physically **press and let go of the button** on the HAT within 15 seconds:

```bash
cd ~/box-translator
python3 - <<'EOF'
import time
from hardware import button

button.on_hold(lambda: print("HELD"))
button.on_release(lambda: print("RELEASED"))

print("press and release the button now, you have 15 seconds")
time.sleep(15)
print("button test done")
EOF
```

You should see `HELD` print the moment you press it, and `RELEASED` print the moment you let go.

---

## Step 10 — Test the microphones (recording)

Paste this whole block, then **talk out loud** when it tells you to:

```bash
cd ~/box-translator
python3 - <<'EOF'
import time
from hardware import recorder

print("recording 5 seconds, talk now")
recorder.start()
time.sleep(5)
path = recorder.stop()
print("saved to:", path)
EOF
```

---

## Step 11 — Test the speaker (playback)

This plays back what you just recorded in Step 10, out of the new speaker on the HAT:

```bash
cd ~/box-translator
python3 - <<'EOF'
from hardware import player

player.play("/tmp/box_recording.wav")
EOF
```

You should hear your own voice from Step 10 come out of the speaker. If you hear it clearly, both the microphone and the speaker are confirmed working.

---

## Step 12 — Shut down safely when you're done

**Do this every single time before you unplug the Pi.** Unplugging it without this step can corrupt the SD card and break everything — this already happened once.

```bash
sudo shutdown -h now
```

Then **watch the LEDs on the Pi itself** — wait for the green activity light to stop blinking and go fully dark. Only unplug the power cable after it's dark.

---

## If something goes wrong

Copy the exact error text and send it back — don't guess or try to fix it yourself. Include which Step number you were on.
