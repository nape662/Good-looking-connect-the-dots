from dots import *


def initial_game_draw():
    pass
    # for i in dots:
    # drop
    # hide/delete menu stuff
    # draw text for time, score


def draw_line(surface, connected, last_dot, new_dot):
    pg.draw.line(surface, last_dot.colour, last_dot.rect.center, new_dot.rect.center, width = 10)
    connected.append(new_dot)
    # also plays sound


def pop_connected(screen, dots, connected):
    last_dot_in_line = None
    screen.fill(BG_COLOR)
    for i in connected:
        i.pop()
    connected.clear()


# if connected:
#   for i in connected:
#   find slices per column?
# if there's loop inside connected pop_dots({all of that colour})


# def end_game():
#    pass
    # running = False
    # menu_draw()
    # finish draw_line() and stop running it
    # stop updating time


# def start():
#    reset_constants()
    # initial_game_draw()
    # running = True


# def menu_draw():
#    pass
    # draw New Game button
    # idk honestly


# def update_time():
#    pass
    # updates time text
    # when reaches 0: end_game()

