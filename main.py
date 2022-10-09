import pyautogui as pag
import tkinter as tk
import tkinter.font as tfont
import tkinter.messagebox as msgbox
from getpass import getuser
from datetime import datetime, timedelta
from os.path import isdir
from os import mkdir, startfile
import threading
import time


class MainWin(tk.Tk):
    def setup(self):
        self.zoom = tk.IntVar()
        self.title("Capture")
        self.resizable(False, False)
        self.iconbitmap("capture.ico")
        font = tfont.Font(family="맑은 고딕", size=20)
        delay_label = tk.Label(self, text="지연: ", font=font)
        delay_entry = tk.Entry(self, font=font, justify="center")
        capture_btn = tk.Button(self, command=self.capture_thread, text="캡처", font=font)
        zoom_check = tk.Checkbutton(self, text="Zoom", variable=self.zoom, font=font)
        delay_entry.insert(0, "5")
        delay_entry.bind("<Enter>", self.capture)
        delay_entry.focus_set()
        zoom_check.select()
        delay_label.pack()
        delay_entry.pack()
        zoom_check.pack()
        capture_btn.pack(expand=True)
        self.delay = delay_entry
        if not isdir(f"C:/Users/{getuser()}/Desktop/캡처/"):
            mkdir(f"C:/Users/{getuser()}/Desktop/캡처/")

    def capture_thread(self):
        thread = threading.Thread(target=self.capture)
        thread.daemon = True
        thread.start()

    def capture(self):
        if self.zoom.get() == 1:
            try:
                pag.getWindowsWithTitle("Zoom 회의")[0].maximize()
            except IndexError:
                msgbox.showerror("오류", "Zoom 회의가 열려있지 않습니다.")
                return
        self.attributes("-alpha", 0)
        filename = f'C:/Users/{getuser()}/Desktop/캡처/{(datetime.utcnow() + timedelta(hours=9)).strftime("%Y년 %m월 %d일 %H시 %M분 %S초")}.png'
        time.sleep(int(self.delay.get()))
        pag.screenshot(filename)
        self.attributes("-alpha", 1)
        result = msgbox.askyesno("스크린샷", "스크린샷이 저장되었습니다.\n확인하시겠습니까?")
        if result:
            startfile(f"C:/Users/{getuser()}/Desktop/캡처")


win = MainWin()
win.setup()
win.mainloop()
