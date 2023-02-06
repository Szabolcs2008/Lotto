
import tkinter as tk
import threading
import time
import socket
import tkinter.messagebox

ip = 'localhost'
port = 9500

root = tk.Tk()
root.title("Lottó-kliens.py")

number_frame = tk.LabelFrame(master=root, text='Számok:')
number_frame.grid(column=0, row=0, padx=20, pady=20)

filename = "numbers.txt"


numbers = []
winner = []

buttons = []
answer='Nem kapcsolódott'
win = 'Unknown'

def button_press(num, btn):
    global numbers

    numbers.append(num)
    btn.config(bg='gray', state='disabled')
    with open(filename, "w") as file:
        file.write(" ".join(str(num) for num in numbers))
    text.config(state='disabled')
    if len(numbers) == 5:
        for button in buttons:
            button.config(state='disabled')

def check():
    talalatok = 0
    global answer
    global winner
    global win
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send('__checkanswer__'.encode())
        msg = s.recv(1024).decode()
        winner = msg.split('_')
        for item in numbers:
            if str(item) in winner:
                talalatok += 1
        answer = f'Nem nyert ({talalatok} találat)'
        win = 'NEM'
        if talalatok == 5:
            answer = 'Nyertél!'
            win = 'IGEN!'

        if msg == '__alreadychecked__':
            win = 'Unknown'
            answer = 'Már egyszer próbálkoztál!'

    except:
        win = 'Unknown'
        answer = 'Szerver hiba'
        tkinter.messagebox.showerror(message="A megadott szerver nem elérhető!")

def reset():
    global numbers
    numbers = []
    for button in buttons:
        button.config(bg='SystemButtonFace', state='normal')


text = tk.Text(root, width=33, height=15, state='disabled')
text.grid(row=0, column=19, rowspan=20, padx=20)
def update():
    global numbers
    while 1:
        try:
            console = f'Konzol: \n------------\nSzerver: localhost:9500\n------------\nSzámaid: {numbers}\nNyert: {win}\n' \
                      f'Válasz: {answer}'
            text.config(state='normal')
            text.delete("1.0", tk.END)
            text.insert(tk.END, console)
            time.sleep(0.04)
        except:
            pass


console_thread = threading.Thread(target=update)
console_thread.start()


for i in range(1, 91):
    btn = tk.Button(number_frame, text=str(i), width=2, height=1, command=lambda num=i: button_press(num, buttons[num-1]))
    btn.grid(row=(i-1)//10, column=(i-1)%10)
    buttons.append(btn)

reset_button = tk.Button(root, text="Újra", command=reset)
reset_button.grid(row=21, column=0, columnspan=12, sticky="WE")

check_answers = tk.Button(root, text='Ellenőrzés', command=check)
check_answers.grid(row=21, column=19, sticky='E')

# run the main loop
root.mainloop()
