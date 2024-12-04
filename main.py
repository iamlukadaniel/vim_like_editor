# main.py
from adapter.curses_adapter import CursesAdapter
from controllers.controller import Controller
from adapter.interface_tui import ITUI
from adapter.interface_control import IControl


def main():
    curses = CursesAdapter()
    tui: ITUI = curses
    control: IControl = curses
    controller = Controller(tui, control)

    try:
        tui.init()
        controller.run()
    except KeyboardInterrupt:
        pass
    finally:
        tui.cleanup()


if __name__ == "__main__":
    main()
