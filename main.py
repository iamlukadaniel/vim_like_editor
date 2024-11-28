# main.py
from adapter.curses_adapter import CursesAdapter
from controllers.controller import Controller
from adapter.interface_tui import ITUI

def main():
    tui: ITUI = CursesAdapter()
    controller = Controller(tui)

    try:
        tui.init()
        controller.run()
    except KeyboardInterrupt:
        pass
    finally:
        tui.cleanup()

if __name__ == "__main__":
    main()
