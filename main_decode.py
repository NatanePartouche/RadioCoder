#!/usr/bin/env python3
"""Command-line interface for FSK audio recording and decoding."""

import argparse
from fsk.decoder import FSKDecoder

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Record FSK audio and decode it back to text'
    )
    parser.add_argument(
        '--duration',
        '-d',
        type=float,
        required=True,
        help='Recording duration in seconds'
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        # Create decoder and start listening
        decoder = FSKDecoder()
        decoded_text = decoder.listen_and_decode(args.duration)
        
        print("\nDecoded text:")
        print("-" * 40)
        print(decoded_text)
        print("-" * 40)
        
    except KeyboardInterrupt:
        print("\nRecording interrupted by user")
    except Exception as e:
        print(f"Error during recording/decoding: {str(e)}")

if __name__ == '__main__':
    main()
