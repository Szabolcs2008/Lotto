import socket
import random
import threading

ip = 'localhost'
port = 9500

print('A szerver indul...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
print('IP és port lefoglalva')

broadcast_list = []
already_checked = []
winner = []


def accept_loop():
    while True:
        s.listen()
        client, client_address = s.accept()
        start_listenning_thread(client, client_address)
        broadcast_list.append(client)


def gen():
    nyero = []
    for i in range(5):
        uj = str(random.randint(1, 90))
        while uj in nyero:
            uj = str(random.randint(1, 90))
        nyero.append(uj)
    nyero = '_'.join(nyero)
    return nyero


def control_thread():
    global winner
    global already_checked
    while 1:
        command = input('> ')
        inp_list = command.split()
        if inp_list[0] in ('/gen', '/generate'):
            already_checked = []
            winner = gen()
            print('Nyerő számok generálva: ** ** ** ** **')
        if inp_list[0] in ('/resetchecked', '/reset'):
            already_checked = []
        if inp_list[0] == '/removeip':
            try:
                already_checked.remove(inp_list[1])
                print(f'{inp_list[1]} eltávolítva')
            except:
                print('Ez az IP még nem lépett be')
        if inp_list[0] == '/printnumbers':
            print(f'A nyerő számok: {winner.split("_")}')



def broadcast(message):
    for client in broadcast_list:
        try:
            client.send(message.encode())
        except:
            broadcast_list.remove(client)


def listen_loop(client, client_address):
    message = client.recv(1024).decode()
    if message:
        if message == '__checkanswer__':
            client_ip = client_address[0]
            if client_ip in already_checked:
                client.send('__alreadychecked__'.encode())
            if client_ip not in already_checked:
                already_checked.append(client_ip)
                client.send(str(winner).encode())


def start_listenning_thread(client, client_address):
    client_thread = threading.Thread(
        target=listen_loop,
        args=(client, client_address,)
    )
    client_thread.start()


control = threading.Thread(target=control_thread)
control.start()
accept_loop()
