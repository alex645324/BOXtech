# BOX — Hardware Prototype Build Report

October 8, 2026 · Alieel Pozo

## Purpose and scope

This session proved that the BOX hardware stack can capture speech and accept user input. Three of four subsystems now work: microphones, button, and LEDs. Speaker output remains blocked on a parts problem.

BOX is a single-button device that translates spoken Spanish and English in both directions and speaks the result out loud. It targets small businesses in Spanish-speaking neighborhoods, starting in Allentown, PA, where roughly 54% of residents are Hispanic or Latino. The pitch is price and simplicity: no app, no pairing, no phone.

The CMPSC 460 assignment requires a functioning web application, not a hardware device. The resolution is that BOX Technologies ships a browser-based translator as its graded product, and the physical device runs against the same backend as a later phase. This report covers the hardware phase only.

Nothing in this session required the translation software. The goal was narrower: confirm the board can hear, and confirm the user can tell it when to listen.

## Hardware inventory

| Part | Role | Notes |
| --- | --- | --- |
| Raspberry Pi 3B+ | Host computer | 1 GB RAM, no NPU; cannot run speech recognition locally |
| ReSpeaker 2-Mics Pi HAT v2.0 | Microphones, button, LEDs | TLV320AIC3104 codec at I2C address 0x18 |
| 2× 2W 8Ω mini speaker, JST-PH 1.25 mm | Audio output | Unused — connector pitch does not match the HAT |
| 32 GB microSD, A1 | Storage | SanDisk-class card with SD adapter |
| 5 V micro-USB supply | Power | Marginal but functional; see power section |

The Pi 3B+ has 1 GB of RAM and no neural accelerator. Running Whisper locally is not viable even at the smallest quantized size, so the prototype sends audio to a cloud API. On-device inference is deferred to a later hardware generation.

## Interaction model

BOX uses press-and-hold, and the language is detected rather than selected. The user holds the button, speaks, and releases. The clip goes to a speech-to-text model that returns both the transcript and the detected language. If the input was Spanish, the output is English; if English, Spanish.

This matters because a shared speaker with one button creates a problem earbuds avoid: the device has no way to know who is speaking or which direction to translate. Two alternatives were considered and rejected.

Continuous listening with separate language identification fails on short utterances and breaks badly on code-switching, which is common in Allentown. A session toggle with voice activity detection feels the most natural but has the worst failure modes — it has to guess where turns end.

Press-and-hold removes the guessing entirely. The user defines the turn boundary by holding the button. Language detection comes free with transcription, so no separate detection step can fail. The three RGB LEDs carry state, since the device has no screen: listening, working, speaking, failed.

## Hardware findings

Three hardware constraints surfaced before any software was written. All three were found by reading specifications rather than by debugging, which saved time.

**The speakers do not fit.** The HAT's speaker output is a JST-PH 2.0 mm socket. The purchased speakers use JST-PH 1.25 mm. These are different pitches and will not mate. An adapter lead or a re-crimp is required.

**The HAT has one speaker output, not two.** It is mono. The second speaker is a spare.

**The onboard amplifier is about 1 W into 8 Ω.** Driving a small single-cavity speaker, that is adequate on a desk and marginal at a shop counter with a cooler running. This is a real product finding, not a prototype inconvenience.

The decision was to abandon the HAT's speaker path for now and route audio out through the Raspberry Pi's own 3.5 mm jack into a powered speaker. Both audio devices coexist: the HAT registers as card 1 for capture, the Pi's headphone output as card 0 for playback.

This sidesteps the connector mismatch entirely and delivers more volume than the HAT's amplifier can. The tradeoff is a second power brick and a larger footprint, which works against the premise of one small box. For a shipping device the correct answer is a proper amplifier on the HAT's output. That remains an open hardware question.

## Operating system setup

Raspberry Pi OS Lite (64-bit), Debian Trixie, kernel 6.18.50+rpt-rpi-v8. Lite was chosen over the desktop image because the Pi has 1 GB of RAM, will run audio capture and network calls, and has no monitor attached. A desktop environment would consume memory for a GUI nobody sees.

The install was headless. Raspberry Pi Imager pre-configured hostname, user account, wifi credentials, locale, and SSH before the card was written, so no monitor or keyboard was ever needed.

Two snags worth recording:

The SD adapter's physical write-protect switch was engaged, which showed in Imager as a read-only device with the Next button disabled. Sliding the lock open fixed it.

**Penn State's network cannot be used.** Campus wifi is WPA2-Enterprise, requiring a username, certificate, and EAP method. The Imager's wifi screen only accepts a plain SSID and password, so a Pi configured for campus wifi fails silently and is unreachable. An iPhone personal hotspot named `boxnet` was used instead. Both the Pi and the MacBook join it.

This is a standing constraint, not a one-time workaround. Any demo on campus needs the hotspot, or a pre-configured home network, or wired ethernet.

## Network troubleshooting

The Pi booted and joined the hotspot, but `ssh box@box.local` and `ping box.local` both returned `cannot resolve box.local: Unknown host`. The cause was a hostname mismatch: the device had been named `BOXtech`, not `box`.

The diagnostic that found it was the iPhone's Personal Hotspot data-usage screen, which lists connected devices by name. It showed three entries, one of them `BOXtech` with 163 KB transferred. That single screen proved the Pi had booted, joined the network, and was passing traffic — and gave the correct hostname at the same time.

`ping BOXtech.local` then resolved to 172.20.10.5 with 0% packet loss, and SSH connected on the first try.

Worth keeping as a method: when a headless device is unreachable, confirm whether it is on the network before touching any configuration. The hotspot's client list answers that in one look. Several possible causes — wrong SSID, failed boot, 5 GHz incompatibility, bad credentials — were all eliminated by one screen.

Note that the IP is assigned by DHCP and will change. Prefer the `.local` name.

## Power supply

Power is adequate but has no margin. `vcgencmd get_throttled` returns `0x0` with the HAT attached, meaning no undervoltage or throttling has been recorded.

The investigation started when the red power LED flickered at power-on with the HAT fitted. On a Pi 3B+ that LED should be steady; flicker indicates the supply dropping below 4.63 V.

Isolating the variable: the Pi alone powered up with a steady red LED and reported `throttled=0x0`. With the HAT attached it also reported `0x0`. The flicker was therefore inrush current at power-on — the HAT's capacitors charging at once — rather than a sustained sag or a short circuit.

This matters because undervoltage causes random reboots and SD card corruption, and those present as software bugs. Ruling it out early prevents hours of chasing symptoms with no cause.

The current supply carries the Pi and the HAT. It will not carry a powered amplifier as well. An official 5.1 V 2.5 A supply is the recommended upgrade before any further load is added.

One process note: the HAT was at one point attached while the board was powered. This worked but should not be repeated. Pins make contact in arbitrary order during insertion, and a 5 V rail briefly touching a GPIO pin can destroy the processor.

## HAT driver installation

**The v2.0 board is not the board most documentation describes.** Seeed replaced the WM8960 codec with a Texas Instruments TLV320AIC3104, which also moved the I2C address from 0x1a to 0x18. Most tutorials, including ones currently ranking well in search, describe the v1.0 board.

This was caught by `i2cdetect -y 1` returning a device at 0x18 rather than the expected 0x1a. The address mismatch was the signal to verify the hardware rather than assume a seating problem.

Two consequences. First, the widely-cited `seeed-voicecard` installer is the wrong path — Seeed's own documentation states it no longer works on current Raspberry Pi OS and leaves the device undetectable by `aplay` and `arecord`. Second, no suitable overlay ships with the OS; `ls /boot/firmware/overlays/ | grep -i seeed` returned only CAN-bus overlays.

The working procedure builds the device tree overlay from source:

```
sudo apt install -y git device-tree-compiler build-essential
git clone https://github.com/Seeed-Studio/seeed-linux-dtoverlays.git
cd seeed-linux-dtoverlays
make overlays/rpi/respeaker-2mic-v2_0-overlay.dtbo
sudo cp overlays/rpi/respeaker-2mic-v2_0-overlay.dtbo /boot/firmware/overlays/respeaker-2mic-v2_0.dtbo
echo "dtoverlay=respeaker-2mic-v2_0" | sudo tee -a /boot/firmware/config.txt
sudo reboot
```

After reboot the card appears as `seeed2micvoicec` on card 1, bound to the `bcm2835-i2s-tlv320aic3x-hifi` driver.

**Known risk.** A kernel regression filed against raspberrypi/linux on 5 October 2026 reports that opening either PCM on a TLV320AIC3104 card returns EINVAL on kernel 6.18.50, while 6.18.39 works. The report is from a Raspberry Pi 5. This Pi 3B+ runs 6.18.50 and is unaffected — recording works normally. If a future image shows the card enumerating but refusing to record, pinning to 6.18.39 is the fix.

## Test results

All three testable subsystems passed.

| Subsystem | Test | Result |
| --- | --- | --- |
| Microphones | 5 s capture at 16 kHz stereo | Pass — 313 KB file, speech clearly audible |
| Button | GPIO17 state polling | Pass — value changes on press |
| LEDs | APA102 animation over SPI | Pass — all three animate |
| Speaker output | Not tested | Blocked on hardware |

**Microphone capture.** The command was `arecord -D plughw:1,0 -f S16_LE -r 16000 -c 2 -d 5 ~/test.wav`. The file was pulled to the MacBook with `scp` and played back. Audio quality was notably better than a laptop microphone.

That quality is expected and worth understanding: the codec digitises on the HAT before the Pi's electrical noise reaches the signal, the two analog microphones sit at opposite corners with a proper preamp and bias, and the capture is uncompressed PCM. 16 kHz is the speech band that recognition models are trained on, not a quality compromise.

**The practical conclusion is that input quality will not limit this product.** The risks sit elsewhere — latency, translation accuracy on code-switched speech, and output volume in a noisy room.

**Button.** Confirmed on GPIO17, matching Seeed's v2.0 documentation. One false negative occurred first: a script written in `nano` saved incorrectly and exited immediately, printing nothing. Writing the file with a heredoc instead of an editor avoided the problem. The lesson is that a script producing no output at all has usually not run, rather than failed.

**LEDs.** Three APA102s on the SPI bus. SPI was enabled via `raspi-config`, then the demo from the `respeaker/mic_hat` repository animated all three.

## Quick reference

| Item | Value |
| --- | --- |
| Hostname | `BOXtech.local` |
| User | `box_tech` |
| Connect | `ssh box_tech@BOXtech.local` |
| Capture device | card 1, `seeed2micvoicec` |
| Playback device | card 0, `bcm2835 Headphones` (3.5 mm) |
| Codec | TLV320AIC3104, I2C 0x18 |
| Button | GPIO17, active low |
| LEDs | 3× APA102 on SPI |
| Overlay | `dtoverlay=respeaker-2mic-v2_0` |

Record five seconds:

```
arecord -D plughw:1,0 -f S16_LE -r 16000 -c 2 -d 5 ~/test.wav
```

Pull a file to the Mac (run on the Mac, not the Pi):

```
scp box_tech@BOXtech.local:~/test.wav ~/Desktop/
```

Check power health:

```
vcgencmd get_throttled
```

`0x0` means clean. Any other value means undervoltage or throttling has occurred.

Shut down before unplugging:

```
sudo shutdown -h now
```

Wait for the green LED to go dark before removing power. Pulling power mid-write corrupts the SD card.

The hotspot must be running before the Pi boots. The Pi only scans for wifi at startup.

## Open items and next steps

**Hardware purchases.** A powered speaker with 3.5 mm input, roughly $15–25, plus a 3.5 mm cable. An official 5.1 V 2.5 A supply before adding any load. A JST-PH 2.0 mm to 1.25 mm adapter only if the HAT's own amplifier is revisited.

**Untested.** Speaker output, end to end latency, microphone range across a counter in a noisy room, and behaviour on code-switched Spanglish.

**Next build phase — the translation pipeline.** Button press triggers a recording, the clip goes to a speech-to-text model, the transcript is translated, and the result is spoken. All of it can be built and tested without a speaker by pulling the output file to the MacBook.

The open decision is the API. A single-vendor path using one provider for transcription, translation, and speech synthesis is simplest, and transcription that returns the detected language removes a separate detection step. Other providers offer more direct speech-to-speech translation. An API key and billing are required either way; testing costs are small.

**Unresolved design question.** The deck's "Under $100" claim has not been tested. Cloud translation carries a recurring per-unit cost, and on-device inference needs silicon that likely breaks that price. This has to be answered before the value proposition can be defended.

**For the assignment.** This session is testing evidence for Step 6. The commands, outputs, and the codec correction are the kind of documented technical work the Paradigm Auditing and QA sections call for.
