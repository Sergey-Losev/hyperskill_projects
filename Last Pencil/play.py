players = ['John', 'Jack']
possible_values = [1, 2, 3]


def pencils_qty():
    print("How many pencils would you like to use:")
    while True:
        qty = input()
        if not qty.isdigit():
            print('The number of pencils should be numeric')
        elif int(qty) <= 0:
            print('The number of pencils should be positive')
        else:
            return int(qty)


def who_is_the_first():
    global players
    while True:
        first = input(f'Who will be the first ({", ".join(players)}):\n')
        if first not in players:
            print(f'Choose between {players[0]} and {players[1]}')
        else:
            return players.index(first)


def pencils_minus(player, pencils):
    global players
    global possible_values
    print(f"{players[player]}'s turn:")
    if players[player] == 'John':
        while True:
            minus = input()
            if not minus.isdigit() or int(minus) not in possible_values:
                print("Possible values: '1', '2' or '3'")
            else:
                return int(minus)
    else:
        if pencils % 4 == 0:
            print('3')
            return 3
        elif pencils % 4 == 3:
            print('2')
            return 2
        elif pencils % 4 == 2:
            print('1')
            return 1
        else:
            print('1')
            return 1


def main():
    pencils = pencils_qty()
    first_player = who_is_the_first()
    next_player = first_player
    while pencils > 0:
        print('|' * pencils)
        next_minus = pencils_minus(next_player, pencils)
        if next_minus > pencils:
            print('Too many pencils were taken')
        else:
            pencils -= next_minus
            next_player = (len(players) - 1) - next_player
            if pencils == 0:
                break
    print(f'{players[next_player]} won')


if __name__ == '__main__':
    main()
