import sys

def warning(msg):
    print(f"Warning: {msg}", file=sys.stderr)

def debug(msg):
    print(msg, file=sys.stderr)