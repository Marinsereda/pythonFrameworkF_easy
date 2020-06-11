list = ['Vanya', 'Petya', 'Vova', 'Vova and Petya and Serega', 'Vova and Petya']


def check_list(name, equals=False):
    for option in list:
        if name in option:
            if equals:
                if name != option:
                    continue
            print('Found !!!')
            return


check_list('Vova and Petya', equals=True)