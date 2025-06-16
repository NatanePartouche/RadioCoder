#!/usr/bin/env python3
"""Command-line interface for FSK text encoding and playback."""

import argparse
from fsk.encoder import FSKEncoder

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Encode text as FSK audio and play it through speakers'
    )
    parser.add_argument(
        '--text',
        '-t',
        type=str,
        required=True,
        help='Text to encode and transmit'
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        # Create encoder and transmit text
        encoder = FSKEncoder()
        print(f"Encoding and playing: {args.text}")
        encoder.encode_and_play(args.text)
        print("Transmission complete!")
        
    except KeyboardInterrupt:
        print("\nTransmission interrupted by user")
    except Exception as e:
        print(f"Error during transmission: {str(e)}")

if __name__ == '__main__':
    main()
