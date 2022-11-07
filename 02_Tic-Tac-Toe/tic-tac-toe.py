game = '         '
checker = True
counter = 1


def print_grid():
    global game
    print("---------")
    print("|", game[0], game[1], game[2], "|")
    print("|", game[3], game[4], game[5], "|")
    print("|", game[6], game[7], game[8], "|")
    print("---------")


def winning_symbol():
    global checker
    winner = 'X'
    wins = 0
    if game[0] != ' ' and game[0] == game[1] and game[0] == game[2]:
        winner = game[0]
        wins += 1
    if game[0] != ' ' and game[0] == game[3] and game[0] == game[6]:
        winner = game[0]
        wins += 1
    if game[0] != ' ' and game[0] == game[4] and game[0] == game[8]:
        winner = game[0]
        wins += 1
    if game[4] != ' ' and game[4] == game[3] and game[4] == game[5]:
        winner = game[4]
        wins += 1
    if game[4] != ' ' and game[4] == game[1] and game[4] == game[7]:
        winner = game[4]
        wins += 1
    if game[4] != ' ' and game[4] == game[2] and game[4] == game[6]:
        winner = game[4]
        wins += 1
    if game[8] != ' ' and game[8] == game[7] and game[8] == game[6]:
        winner = game[8]
        wins += 1
    if game[8] != ' ' and game[8] == game[5] and game[8] == game[2]:
        winner = game[8]
        wins += 1
    if wins > 1:
        print('Impossible')
        checker = False
    if ' ' not in game:
        print('Draw')
        checker = False
    if wins == 1:
        print(winner, 'wins')
        checker = False
    if (game.count('X') - game.count('O') > 1) or \
            (game.count('X') - game.count('O') < -1):
        # print(game.count('X'), game.count('O'))
        print('Impossible')
        checker = False
    elif wins == 0 and '_' in game:
        print('Game not finished')
        checker = False


def next_symbol():
    global game, counter
    checker1 = True
    while checker1:
        row, column = input('Enter the coordinates: ').split()
        row, column = int(row), int(column)
        if row > 3 or column > 3:
            print('Coordinates should be from 1 to 3!')
        else:
            index = ((row - 1) * 3 + (column + 2)) - 3
            game = list(game)
            if game[index] != ' ':
                print('This cell is occupied! Choose another one!')
            else:
                if counter % 2 == 1:
                    game[index] = 'X'
                else:
                    game[index] = 'O'
                print_grid()
                break
        counter += 1


def game_proceed():
    global game
    print_grid()
    while checker:
        next_symbol()
        winning_symbol()


if __name__ == '__main__':
    game_proceed()
