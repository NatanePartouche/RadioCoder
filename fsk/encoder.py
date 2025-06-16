"""FSK encoder for converting text to audio signals."""

import numpy as np
import sounddevice as sd
from fsk.shared.config import (
    SAMPLE_RATE, CHAR_DURATION, SILENCE_DURATION,
    SAMPLES_PER_CHAR, SILENCE_SAMPLES, SIGNAL_DURATION,
    START_FREQ, END_FREQ, BOUNDARY_SILENCE_SAMPLES
)
from fsk.shared.frequency_map import FrequencyMap

class FSKEncoder:
    def __init__(self):
        self.freq_map = FrequencyMap()
    
    def generate_tone(self, frequency: float, duration: float) -> np.ndarray:
        """Generate a sine wave of given frequency and duration."""
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), False)
        return np.sin(2 * np.pi * frequency * t)

    def generate_silence(self, samples: int) -> np.ndarray:
        """Generate a period of silence."""
        return np.zeros(samples)

    def generate_start_signal(self) -> np.ndarray:
        """Generate the start signal."""
        return np.concatenate([
            self.generate_tone(START_FREQ, SIGNAL_DURATION),
            self.generate_silence(BOUNDARY_SILENCE_SAMPLES)  # Extra silence after start
        ])

    def generate_end_signal(self) -> np.ndarray:
        """Generate the end signal."""
        return np.concatenate([
            self.generate_silence(BOUNDARY_SILENCE_SAMPLES),  # Extra silence before end
            self.generate_tone(END_FREQ, SIGNAL_DURATION),
            self.generate_silence(SILENCE_SAMPLES)  # Final silence
        ])

    def encode_text(self, text: str) -> np.ndarray:
        """Encode text into an FSK audio signal with start/end markers."""
        # Initialize signal with start marker
        signal = self.generate_start_signal()
        
        # Generate tones for each character
        for char in text:
            # Get frequency for current character
            freq = self.freq_map.char_to_freq(char)
            
            # Generate and append tone
            tone = self.generate_tone(freq, CHAR_DURATION)
            signal = np.append(signal, tone)
            
            # Add silence between characters
            signal = np.append(signal, self.generate_silence(SILENCE_SAMPLES))
        
        # Add end marker
        signal = np.append(signal, self.generate_end_signal())
        
        return signal

    def play_signal(self, signal: np.ndarray) -> None:
        """Play the encoded signal through speakers."""
        # Normalize signal to prevent clipping
        signal = signal / np.max(np.abs(signal))
        
        # Apply fade in/out to reduce pops
        fade_samples = int(0.01 * SAMPLE_RATE)  # 10ms fade
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        signal[:fade_samples] *= fade_in
        signal[-fade_samples:] *= fade_out
        
        # Play the signal
        sd.play(signal, SAMPLE_RATE)
        sd.wait()  # Wait until the signal is done playing

    def encode_and_play(self, text: str) -> None:
        """Encode the text and play it immediately."""
        signal = self.encode_text(text)
        self.play_signal(signal)
