"""FSK decoder for converting audio signals back to text."""

import numpy as np
from scipy.fft import fft
from scipy.signal import windows
import sounddevice as sd
from fsk.shared.config import (
    SAMPLE_RATE, CHAR_DURATION, SILENCE_DURATION,
    SAMPLES_PER_CHAR, SILENCE_SAMPLES, FFT_SIZE,
    START_FREQ, END_FREQ, SIGNAL_DURATION, SIGNAL_SAMPLES,
    FREQ_TOLERANCE, BOUNDARY_SILENCE_SAMPLES,
    AMPLITUDE_THRESHOLD, REPEAT_CHAR_THRESHOLD
)
from fsk.shared.frequency_map import FrequencyMap

class FSKDecoder:
    def __init__(self):
        self.freq_map = FrequencyMap()
        # Pre-compute window function
        self.window = windows.blackman(FFT_SIZE)

    def record_audio(self, duration: float) -> np.ndarray:
        """Record audio for the specified duration."""
        print(f"Recording for {duration} seconds...")
        recording = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1
        )
        sd.wait()  # Wait until recording is done
        return recording.flatten()

    def find_peak_frequency(self, signal: np.ndarray) -> float:
        """Find the dominant frequency in a signal segment using FFT."""
        if len(signal) < FFT_SIZE:
            # Zero-pad if signal is shorter than FFT size
            signal = np.pad(signal, (0, FFT_SIZE - len(signal)))
        
        # Use multiple overlapping windows for better accuracy
        num_windows = 4
        window_step = len(signal) // (num_windows + 1)
        magnitudes = []
        
        for i in range(num_windows):
            # Extract window
            start = i * window_step
            end = start + FFT_SIZE
            if end > len(signal):
                break
                
            # Apply Blackman window and compute FFT
            windowed = signal[start:end] * self.window
            fft_result = fft(windowed)
            fft_freqs = np.fft.fftfreq(FFT_SIZE, 1/SAMPLE_RATE)
            
            # Consider only positive frequencies
            positive_freqs_mask = fft_freqs > 0
            magnitude_spectrum = np.abs(fft_result)[positive_freqs_mask]
            freq_bins = fft_freqs[positive_freqs_mask]
            
            # Store magnitude spectrum
            magnitudes.append((magnitude_spectrum, freq_bins))
        
        # Average magnitude spectra
        avg_magnitude = np.mean([m[0] for m in magnitudes], axis=0)
        freq_bins = magnitudes[0][1]  # Frequency bins are the same for all windows
        
        # Find peak in averaged spectrum
        peak_idx = np.argmax(avg_magnitude)
        return freq_bins[peak_idx]

    def is_start_signal(self, freq: float) -> bool:
        """Check if a frequency corresponds to the start signal."""
        return abs(freq - START_FREQ) < FREQ_TOLERANCE * 1.5

    def is_end_signal(self, freq: float) -> bool:
        """Check if a frequency corresponds to the end signal."""
        return abs(freq - END_FREQ) < FREQ_TOLERANCE * 1.5

    def is_silence(self, signal: np.ndarray) -> bool:
        """Check if a signal segment is silence."""
        return np.mean(np.abs(signal)) < AMPLITUDE_THRESHOLD

    def find_signal_boundaries(self, signal: np.ndarray) -> tuple[int, int]:
        """Find the start and end positions of the message in the signal."""
        start_pos = -1
        end_pos = -1
        
        # Search for start marker
        i = 0
        while i < len(signal) - SIGNAL_SAMPLES:
            if self.is_start_signal(self.find_peak_frequency(signal[i:i + SIGNAL_SAMPLES])):
                # Look for the end of the silence after start signal
                silence_end = i + SIGNAL_SAMPLES
                while silence_end < len(signal) - SAMPLES_PER_CHAR:
                    if not self.is_silence(signal[silence_end:silence_end + SAMPLES_PER_CHAR]):
                        start_pos = silence_end
                        break
                    silence_end += SAMPLES_PER_CHAR // 2
                break
            i += SIGNAL_SAMPLES // 4
        
        if start_pos == -1:
            return -1, -1
        
        # Search for end marker
        i = start_pos
        while i < len(signal) - SIGNAL_SAMPLES:
            if self.is_end_signal(self.find_peak_frequency(signal[i:i + SIGNAL_SAMPLES])):
                # Look backwards for the last non-silence segment
                silence_start = i - SAMPLES_PER_CHAR
                while silence_start > start_pos:
                    if not self.is_silence(signal[silence_start:silence_start + SAMPLES_PER_CHAR]):
                        end_pos = silence_start + SAMPLES_PER_CHAR
                        break
                    silence_start -= SAMPLES_PER_CHAR // 2
                break
            i += SIGNAL_SAMPLES // 4
        
        return start_pos, end_pos

    def decode_signal(self, signal: np.ndarray) -> str:
        """Decode an FSK audio signal back to text."""
        # Find message boundaries
        start_pos, end_pos = self.find_signal_boundaries(signal)
        if start_pos == -1 or end_pos == -1:
            print("Warning: Could not detect start/end signals")
            return ""
        
        # Extract the message portion
        message_signal = signal[start_pos:end_pos]
        
        decoded_text = []
        last_char_pos = {}  # Track last position of each character
        segment_size = SAMPLES_PER_CHAR
        
        # Process each character segment
        i = 0
        while i < len(message_signal) - segment_size:
            # Extract segment for current character
            segment = message_signal[i:i + segment_size]
            
            # Skip if segment is silence
            if self.is_silence(segment):
                i += segment_size
                continue
            
            # Find the dominant frequency
            freq = self.find_peak_frequency(segment)
            
            # Convert frequency to character
            char = self.freq_map.freq_to_char(freq)
            if char:
                # Check if this is a valid repeated character
                if char not in last_char_pos or (i - last_char_pos[char]) >= REPEAT_CHAR_THRESHOLD:
                    decoded_text.append(char)
                    last_char_pos[char] = i
            
            # Skip to next character (including silence gap)
            i += segment_size + SILENCE_SAMPLES
        
        return ''.join(decoded_text)

    def listen_and_decode(self, duration: float) -> str:
        """Record audio and decode it to text."""
        # Record the audio
        signal = self.record_audio(duration)
        
        # Decode the signal
        return self.decode_signal(signal)
