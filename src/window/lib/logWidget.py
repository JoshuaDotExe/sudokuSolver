import tkinter as tk
import logging

class logWidget(logging.Handler):
    def __init__(self, container):
        logging.Handler.__init__(self)
        self.container = container
        self.textBox = tk.Text(container, wrap=tk.WORD, height=15)
        self.textBox.configure(state='disabled')
        self.textBox.pack(side=tk.LEFT)
        self.scrollB = tk.Scrollbar(container, command=self.textBox.yview)
        self.scrollB.pack(side=tk.RIGHT, fill='y')
        
        self.textBox['yscrollcommand'] = self.scrollB.set
    def emit(self, record):
        msg = self.format(record)
        def append():
            self.textBox.configure(state='normal')
            self.textBox.insert(tk.END, msg + '\n')
            self.textBox.configure(state='disabled')
            self.textBox.yview(tk.END)
        self.textBox.after(0, append)