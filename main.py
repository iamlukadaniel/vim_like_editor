# main.py
from adapter.curses_adapter import CursesAdapter
from controller.controller import Controller
from interfaces.adapter.base_tui import ITUI
from interfaces.adapter.base_control import IControl


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
