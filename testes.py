while (True): 
    entrar = input(f'digite zero: ')
    if entrar == '0':
        print('O Sistema Fodeu!!!')
        break
    elif entrar == '1': 
        print('Tudo ok')
    else:
        print(f'um {entrar}, Fudeu o sistema')
        break

