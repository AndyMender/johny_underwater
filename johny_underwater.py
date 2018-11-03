from libs.engine import Engine

if __name__ == '__main__':

    # load and start game engine
    game_engine = Engine()

    game_engine.init_pygame()

    game_engine.pg.draw.rect(game_engine.SCREEN, (0, 120, 255), game_engine.pg.Rect(30, 30, 60, 60))

    game_engine.pg.display.flip()

    game_engine.main_loop()
