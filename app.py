from window import *


def run():
    pg.init()
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.fill(BG_COLOR)

    dots = [[0] * 6 for i in range(6)]
    for i in range(6):
        for j in range(6):
            dots[j][i] = (Dot(j, i, screen, dots))
    connected = list()
    lines = list()

    last_dot_in_line = None
    # main loop
    running = True
    while running:
        # inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif pg.mouse.get_pressed()[0]:
                # THIS SHIT IS UGLY AS FUCK I NEED TO CHANGE IT ALL
                # CLASS GAME IS REAL UNFORTUNATELY
                try:
                    x, y = event.pos
                    dotx = int((x - (SCREEN_WIDTH - 600) / 2) // 100)
                    doty = int((y - 175) // 100)
                    if last_dot_in_line is None:
                        last_dot_in_line = dots[dotx][doty]
                        connected.append(last_dot_in_line)
                    elif dots[dotx][doty] != last_dot_in_line:
                        draw_line(screen, connected, last_dot_in_line, dots[dotx][doty])
                        last_dot_in_line = dots[dotx][doty]
                except AttributeError:  # if click on screen release off screen get AttributeError
                    pass
            elif event.type == pg.MOUSEBUTTONUP:
                last_dot_in_line = None
                if len(connected) > 1:
                    pop_connected(screen, dots, connected)

        # draws to screen
        for i in dots:
            for j in i:
                screen.blit(j.surface, j.rect)
        pg.display.flip()
    return 0


run()
