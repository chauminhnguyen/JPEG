import sys
import encoder
import decoder

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
from TkinterDnD2 import *

string = ""
r = 0
time = 0

def drop(event):
    global string
    string =  event.data
    entry_sv.set(event.data)

def click_encoder():
    global r, time
    if string == "":
        res['text'] = "You must drop an image first"
    else:
        res['text'] = "Đang nén..."
        r, time = encoder.main(string[0:])
        r_label['text'] = "Hệ số nén: " + str(r)
        e_time_label['text'] = "Thời gian nén: " + str(time)
        
        res['text'] = "Đang giải nén..."
        time = decoder.main()
        res['text'] = "Kết quả nén và giải nén: "
        d_time_label['text'] = "Thời gian giải nén: " + str(time)
        

drop_pos_y = 10

root = TkinterDnD.Tk()
root.wm_title("JPEG compression")
root.geometry("300x300")
entry_sv = StringVar()
entry_sv.set('Drop Image Here...')
entry = Entry(root, textvar=entry_sv, width=80)
entry.pack(fill=X, padx=10, pady=drop_pos_y, ipady=20)
entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', drop)

encode = Button (None, text="ENCODE", width=6, command=click_encoder)
encode.place(x=5, y=drop_pos_y+220, width=100, height=50)

res = Label (root, text="", font="none 12")
res.place(x = 5, y = drop_pos_y + 80)


r_label = Label (root, text="", font="none 12")
r_label.place(x = 5, y = drop_pos_y + 110)

e_time_label = Label (root, text="", font="none 12")
e_time_label.place(x = 5, y = drop_pos_y + 140)

d_time_label = Label (root, text="", font="none 12")
d_time_label.place(x = 5, y = drop_pos_y + 170)

root.mainloop()