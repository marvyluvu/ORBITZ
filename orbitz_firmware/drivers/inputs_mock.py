import sys


def read_buttons():
    buttons = {
        "quit": False,
        "mode": False,
        "next": False,
        "prev": False,
    }

    if sys.platform.startswith("win"):
        import msvcrt
        while msvcrt.kbhit():
            ch = msvcrt.getwch().lower()
            if ch == "q":
                buttons["quit"] = True
            elif ch == "m":
                buttons["mode"] = True
            elif ch == "j":
                buttons["next"] = True
            elif ch == "k":
                buttons["prev"] = True

    return buttons