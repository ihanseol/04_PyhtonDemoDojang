from screeninfo import get_monitors

def get_screen_width() -> int:
    hmonitor = len(get_monitors())
    print('get_monitors:', hmonitor)

    screen1 = get_monitors()[0]
    if hmonitor != 1:
        screen2 = get_monitors()[1]

    if hmonitor == 1:
        screen = screen1
    else:
        if screen1.width > screen2.width:
            screen = screen1
        else:
            screen = screen2

    print(f'screen width : {screen.width}')
    return screen.width


def get_screen_height() -> int:
    hmonitor = len(get_monitors())
    print('get_monitors:', hmonitor)

    screen1 = get_monitors()[0]
    if hmonitor != 1:
        screen2 = get_monitors()[1]

    if hmonitor == 1:
        screen = screen1
    else:
        if screen1.width > screen2.width:
            screen = screen1
        else:
            screen = screen2

    print(f'screen width : {screen.width}')
    return screen.height


def check_screen_dimension():
    print('get screen width ', get_screen_width())
    print('get screen height ', get_screen_height())


if __name__ == '__main__':
    check_screen_dimension()
