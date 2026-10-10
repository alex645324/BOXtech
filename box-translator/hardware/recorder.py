import subprocess
import tempfile
from pathlib import Path

DEVICE = "plughw:CARD=seeed2micvoicec,DEV=0"
SAMPLE_RATE = "16000"
CHANNELS = "1"

OUTPUT_PATH = str(Path(tempfile.gettempdir()) / "box_recording.wav")

_process = None


def start():
    global _process
    _process = subprocess.Popen([
        "arecord",
        "-D", DEVICE,
        "-f", "S16_LE",
        "-r", SAMPLE_RATE,
        "-c", CHANNELS,
        OUTPUT_PATH,
    ])


def stop():
    global _process
    _process.terminate()
    _process.wait()
    return OUTPUT_PATH
