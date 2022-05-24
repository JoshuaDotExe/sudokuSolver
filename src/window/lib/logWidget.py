import queue
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import logging

from src import LOGSOLVE

class logWidget(ScrolledText):
    def __init__(self, container, parent):
        super().__init__(container, wrap=tk.WORD, height=18, state='disabled')
        self.logQueue = queue.Queue()
        self.queueHandler = widgetLogger(self.logQueue)
        self.takeLog = True
        LOGSOLVE.addHandler(self.queueHandler)
        parent.after(10, self.logQueueGrab, parent.game.solved)
        
    def pushText(self, log):
        msg = self.queueHandler.format(log)
        self.configure(state='normal')
        self.insert(tk.END, msg + '\n') # + '\n', log.levelname
        self.configure(state='disabled')
        # Autoscroll to the bottom
        self.yview(tk.END)
    
    def logQueueGrab(self, solved):
        # Check every 50ms if there is a new message in the queue to display
        while True:
            try:
                record = self.logQueue.get(block=False)
            except queue.Empty:
                break
            else:
                self.pushText(record)
        #if solved == True: self.takeLog == False
        self.after(50, self.logQueueGrab, solved)
    
        
class widgetLogger(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue
        self.setFormatter(logging.Formatter('%(message)s')) #%(levelname)-8s | %(name)-8s
    
    def emit(self, record):
        self.log_queue.put(record)