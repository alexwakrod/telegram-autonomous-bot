"""
Hypothesis-based fuzzing for the bot's input parsers.
Run with: pytest fuzzing/ --hypothesis-show-statistics
"""

from hypothesis import given, strategies as st, settings, Verbosity
from bot.handlers.commands import parse_reminder_args, validate_time_unit

# Strategy for generating random reminder strings: "<number><unit> <message>"
reminder_strategy = st.builds(
    lambda num, unit, msg: f"{num}{unit} {msg}",
    num=st.integers(min_value=1, max_value=999),
    unit=st.sampled_from(['s', 'm', 'h', 'd']),
    msg=st.text(min_size=1, max_size=100)
)

@given(reminder_strategy)
@settings(max_examples=500, verbosity=Verbosity.verbose)
def test_parse_reminder(fuzz_input):
    """Should never crash; return (value, unit, message) or None"""
    result = parse_reminder_args(fuzz_input)
    if result is not None:
        value, unit, msg = result
        assert isinstance(value, int)
        assert unit in ['s','m','h','d']
        assert isinstance(msg, str)

def run_fuzz():
    """Entry point for fuzzing (called from bot.main with --fuzz)"""
    print("Starting Hypothesis fuzzing...")
    test_parse_reminder()
    print("Fuzzing completed – no crashes found.")

if __name__ == "__main__":
    run_fuzz()