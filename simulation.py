import threading
import random
import time
import socket
from datetime import datetime

total_tries = 0
total_fives = 0


patchdupes = True
log4s = False
write_to_file = True
write_to_console = True
statistics_server = True
nmax = 90  # maximum szám ami generálható
repeat = 99999  # ismétlés statisztika előtt
ltype = 5


def get_ip():
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.settimeout(0)
     try:

         s.connect(('8.8.8.8', 1))
         IP = s.getsockname()[0]
     except Exception:
         IP = '127.0.0.1'
     finally:
         s.close()
     return IP


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 9500
ADDRESS = get_ip()
print('My IP is:', ADDRESS + ":" + str(PORT))
broadcast_list = []
s.bind((ADDRESS, PORT))


def stat_server():
    def accept_loop():
        start_bc_thread()
        while True:
            s.listen()
            client, client_address = s.accept()
            broadcast_list.append(client)

    def broadcast(message):
        for client in broadcast_list:
            try:
                client.send(message.encode())
            except:
                broadcast_list.remove(client)

    def bc_loop():
        while 1:
            message = str(total_tries)+';'+str(total_fives)
            broadcast(message)
            time.sleep(1)

    def start_bc_thread():
        thread_1 = threading.Thread(
            target=bc_loop,
        )
        thread_1.start()

    thr = threading.Thread(target=accept_loop)
    thr.start()




path = 'logs.txt'
if statistics_server:
    stat_thread = threading.Thread(target=stat_server)
    stat_thread.start()


# Új nyerő számok henerálása
# Kimenet: lista
def gen():
    nyero = []
    for i in range(ltype):
        uj = random.randint(1, nmax)
        while uj in nyero:
            uj = random.randint(1, nmax)
        nyero.append(uj)
    return nyero


def addlog(string):
    with open(path, "a+") as logfile:
        logfile.write(string)


now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

addlog('------------------------------')
addlog(dt_string+"\n")
# változók
talalt = 0
gens = 0
tps = 0
list1 = []  # 5-ös találatoknál lévő próbálkozások listája
time1 = time.time()  # a program elején lévő cpu idő
for x in range(repeat):
    talalt = 0
    gens = 0
    while talalt != 5:  # amíg nincsen 5 találat
        if ((gens % 10000) == 0) and (gens != 0):
            time2 = time.time()  # jelenlegi cpu idő
            current_runtime = time2 - time1
            tps = str(round((total_tries / current_runtime), 2)) + 'tps'
        talalt = 0
        bemenet = []
        # random tipp generálás
        for i in range(ltype):
            szam = random.randint(1, nmax)
            if patchdupes:
                # ha igaz, nem lehetnek dupla számon
                while szam in bemenet:
                    szam = random.randint(1, nmax)
            bemenet.append(szam)
        # -------------------------
        nyero = gen()  # nyerő szám generálás
        num = 0
        # találatok ellenőrzése
        for item in bemenet:
            if int(item) in nyero:
                talalt += 1
        num += 1
        run = str(x) + '/' + str(repeat)
        console_str = 'Run: ' + run + ' | ' \
                      + 'Try:' + str(gens) + ' (' + str(total_tries) + ') | ' \
                      + str(talalt) + ' | ' \
                      + "Sebesség: " + str(tps)

        if write_to_console:
            print(console_str)
        if talalt == 5:
            list1.append(gens)
            total_fives += 1
            if write_to_file:
                addlog(console_str + '\n')
        if talalt == 4:
            if log4s:
                if write_to_file:
                    addlog(console_str + '\n')
        gens += 1
        total_tries += 1
    time.sleep(0.25)

a = 0
for item in list1:
    print(item)
    a += item
b = a / repeat
print('Átlag próba: ' + str(b))
addlog('------------------------------')