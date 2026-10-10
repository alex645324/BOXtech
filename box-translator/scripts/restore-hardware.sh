#!/bin/bash
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo 'Run this script with sudo.' >&2
    exit 1
fi

pi_home=$(getent passwd box_tech | cut -d: -f6)
overlay="$pi_home/seeed-linux-dtoverlays/overlays/rpi/respeaker-2mic-v2_0-overlay.dtbo"
test -s "$overlay"
test -f /boot/firmware/config.txt
backup="/boot/firmware/config.txt.before-box-restore-$(date +%Y%m%d-%H%M%S)"
cp /boot/firmware/config.txt "$backup"
install -m 644 "$overlay" /boot/firmware/overlays/respeaker-2mic-v2_0.dtbo

python3 - <<'PY'
from pathlib import Path
config = Path('/boot/firmware/config.txt')
text = config.read_text()
marker = '# BOX hardware restoration'
if marker not in text:
    text += '\n[all]\n' + marker + '\n'
    text += 'dtparam=i2c_arm=on\ndtparam=spi=on\ndtparam=audio=on\n'
    text += 'dtoverlay=respeaker-2mic-v2_0\n'
    config.write_text(text)
PY

usermod -aG audio,gpio,spi,i2c box_tech
amixer -c Headphones sset PCM 70% unmute || true
sync
echo "Microphone overlay and SPI/I2C settings restored. Backup: $backup"
echo 'Rebooting BOX to activate the hardware. SSH will disconnect.'
systemctl reboot
