from Game import Game
if __name__ == '__main__':
    # Putting game mechanics in a loop. Exiting this script is available at any time.
    while True:
        # Max grid size should not >= 30 since sprite size = 30px & max screen height = 900.
        game: Game = Game(25, 25)