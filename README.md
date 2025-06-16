# 🎧 RadioCoder

**Transmit text using sound. Offline, simple, effective.**

RadioCoder is a Python-based system that transmits and receives text over audio using **Frequency-Shift Keying (FSK)**. It includes:
- An encoder that converts your text to sound,
- A decoder that listens to audio and reconstructs the original message.

This can be used in offline environments, between devices, or as an educational tool for digital communication concepts.

---

## 📡 How It Works

RadioCoder uses **FSK modulation**, where each character is converted to a unique frequency tone:

- A **base frequency** (e.g. 1200 Hz) is assigned to the first character.
- Each additional character uses a **step** above the base (e.g. 50 Hz).
- The **encoder** plays a sine wave per character, separated by short silences.
- Special **start and end tones** mark the message boundaries.
- The **decoder** uses **FFT (Fast Fourier Transform)** to detect the dominant frequencies and convert them back to characters.

---

## 📁 Project Structure

```
RadioCoder/
├── fsk/
│   ├── __init__.py
│   ├── encoder.py            # Converts text to audio tones
│   ├── decoder.py            # Analyzes audio and extracts text
│   └── shared/
│       ├── __init__.py
│       ├── config.py         # Global configuration and parameters
│       └── frequency_map.py  # Maps characters to frequencies
├── main_encode.py            # CLI encoder script
├── main_decode.py            # CLI decoder script
├── requirements.txt          # Python dependencies
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/NatanePartouche/RadioCoder.git
cd RadioCoder
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Usage

### ➤ Encode and Transmit Text as Audio

```bash
PYTHONPATH=$PYTHONPATH:. python main_encode.py -t "Hello from RadioCoder"
```

This will play the encoded message through your default speaker.

---

### ➤ Record and Decode Audio into Text

```bash
PYTHONPATH=$PYTHONPATH:. python main_decode.py -d 5
```

This listens to audio for **5 seconds** and prints the decoded message.

---

## 🛠 Configuration

You can customize transmission settings in [`fsk/shared/config.py`](fsk/shared/config.py):

| Parameter         | Description                                | Default      |
|------------------|--------------------------------------------|--------------|
| `SAMPLE_RATE`     | Audio sampling rate (Hz)                   | `44100`      |
| `CHAR_DURATION`   | Duration of each tone (sec)                | `0.15`       |
| `SILENCE_DURATION`| Pause between characters (sec)             | `0.10`       |
| `BASE_FREQ`       | Start frequency for encoding (Hz)          | `1200`       |
| `FREQ_STEP`       | Frequency spacing between characters (Hz)  | `50`         |
| `FREQ_TOLERANCE`  | Acceptable deviation for decoding (Hz)     | `15`         |
| `START_FREQ`      | Start signal frequency (Hz)                | `500`        |
| `END_FREQ`        | End signal frequency (Hz)                  | `3000`       |

---

## 🧩 Requirements

- Python ≥ 3.6  
- [NumPy](https://numpy.org/)  
- [SciPy](https://scipy.org/)  
- [sounddevice](https://python-sounddevice.readthedocs.io/)

Install them with:

```bash
pip install -r requirements.txt
```

---

## 📌 Notes & Tips

- Use in a **quiet environment** for best decoding results.
- Check that your **microphone and speakers are properly configured**.
- Works best with **consistent volume** and **no clipping**.
- Can handle **repeated characters**, e.g., `"HELLO"` with double 'L'.
- Start and end tones help the decoder isolate the message.

---

## 📄 License

MIT License. See `LICENSE` for details.

---

## 💡 Inspiration

This project is inspired by the idea that **sound itself can be a transport layer**, and that meaningful digital communication can happen without cables, networks, or Wi-Fi.

---

## 🔗 Related

- [FSK - Frequency-Shift Keying (Wikipedia)](https://en.wikipedia.org/wiki/Frequency-shift_keying)
- [Fourier Transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform)
