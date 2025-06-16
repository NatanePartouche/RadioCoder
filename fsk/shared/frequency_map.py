"""Maps characters to frequencies and vice versa for FSK transmission."""

from fsk.shared.config import BASE_FREQ, FREQ_STEP, FREQ_TOLERANCE

class FrequencyMap:
    @staticmethod
    def char_to_freq(char: str) -> float:
        """Convert a character to its corresponding frequency."""
        if not char or len(char) != 1:
            raise ValueError("Input must be a single character")
        
        # Use ASCII value to determine frequency offset
        ascii_val = ord(char)
        return BASE_FREQ + (ascii_val * FREQ_STEP)

    @staticmethod
    def freq_to_char(freq: float) -> str:
        """Convert a frequency back to its corresponding character."""
        # Calculate the closest character based on frequency
        freq_offset = freq - BASE_FREQ
        ascii_val = round(freq_offset / FREQ_STEP)
        
        # Check if the frequency is within reasonable bounds
        if ascii_val < 0 or ascii_val > 127:  # ASCII range
            return ''
        
        # Check if the frequency is within tolerance
        expected_freq = BASE_FREQ + (ascii_val * FREQ_STEP)
        if abs(freq - expected_freq) > FREQ_TOLERANCE:
            return ''
            
        return chr(ascii_val)
