import sys

def read_encoder() -> int:
    """
    Development stub:
    -1 = turn left, +1 = turn right, 0 = no movement.
    for now it will always return 0
    Possibly later keyboard can be mapped for future testing if needed.
    """
    return 0

def read_buttons() -> dict:
    print("\n[INPUT] Press enter=None, m=mode, q=quit", end="")
    sys.stdout.flush()
    ch = sys.stdin.readline().strip().lower()

    buttons= {
        "mode": False,
        "back": False,
        "select": False,
        "quit": False,
    }
    
    if ch == "m":
        buttons["mode"]= True
    elif ch == "q":
        buttons["quit"]= True

    return buttons
    