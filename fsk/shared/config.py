"""Configuration parameters for FSK audio transmission."""

# Audio parameters
SAMPLE_RATE = 44100  # Hz
CHAR_DURATION = 0.15  # seconds
SILENCE_DURATION = 0.1  # seconds

# Frequency parameters
BASE_FREQ = 1200  # Hz
FREQ_STEP = 50  # Hz per character
FREQ_TOLERANCE = 15  # Hz

# Special signal frequencies
START_FREQ = 500  # Hz
END_FREQ = 3000   # Hz
SIGNAL_DURATION = 0.2  # seconds

# Derived parameters
SAMPLES_PER_CHAR = int(CHAR_DURATION * SAMPLE_RATE)
SILENCE_SAMPLES = int(SILENCE_DURATION * SAMPLE_RATE)
BOUNDARY_SILENCE_SAMPLES = int(SILENCE_DURATION * 2 * SAMPLE_RATE)  # Double silence for boundaries
SIGNAL_SAMPLES = int(SIGNAL_DURATION * SAMPLE_RATE)

# FFT parameters
FFT_SIZE = 8192

# Decoding parameters
AMPLITUDE_THRESHOLD = 0.01  # Threshold for silence detection
REPEAT_CHAR_THRESHOLD = SAMPLES_PER_CHAR * 0.75  # Minimum samples between repeated chars
