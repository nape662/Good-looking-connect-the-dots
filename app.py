from window import *


def run():
    pg.init()
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    dots = [[0] * 6 for i in range(6)]
    screen.fill(BG_COLOR)
    for i in range(6):
        for j in range(6):
            dots[j][i] = (Dot(j, i, screen, dots))

    # main loop
    running = True
    while running:
        # inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                x = int((x - (SCREEN_WIDTH - 600) / 2)//100)
                y = int((y - 175)//100)
                dots[x][y].pop()

        # draws to screen
        for i in dots:
            for j in i:
                screen.blit(j.surface, j.rect)
        pg.display.flip()
    return 0


run()
