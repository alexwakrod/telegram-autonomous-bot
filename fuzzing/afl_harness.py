"""
AFL++ harness for coverage-guided fuzzing.
Compile with afl-gcc and run: afl-fuzz -i inputs/ -o findings/ -- python afl_harness.py @@
"""

import sys
from bot.handlers.commands import parse_reminder_args

def main():
    if len(sys.argv) != 2:
        print("Usage: afl-fuzz ... -- python afl_harness.py <input_file>")
        sys.exit(1)
    with open(sys.argv[1], 'rb') as f:
        data = f.read().decode('utf-8', errors='replace')
    # Fuzz the reminder parser
    parse_reminder_args(data)
    # Also fuzz help page argument
    if data.strip().isdigit():
        page = int(data.strip())
        # No crash expected

if __name__ == "__main__":
    main()