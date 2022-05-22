import tkinter as tk

class subGrid(tk.Frame):
    def __init__(self, container, gridBox, markBox, SQRT, charSet):
        super().__init__(container, bg='#C0C0C0')
        for itemIndex, item in enumerate(gridBox):
            x = (itemIndex%SQRT) * SQRT
            y = (itemIndex//SQRT) * SQRT
            if item != '0':
                tk.Label(self, text=item, fg='blue', width=4, height=2, font=("Helvetica", "20")).grid(row=y, column=x, rowspan=SQRT, columnspan=SQRT, padx=1, pady=1)
                continue
            finStr = str()
            for charIndex, char in enumerate(charSet):
                finStr += f'{char}' if char in markBox[itemIndex] else ' '
                finStr += '\n' if charIndex%SQRT == 2 else ' '
            finStr += ' '
            tempLabel = tk.Label(self, text=finStr[:-2], width=8, height=4, font=("courier", "10"))
            tempLabel.grid_propagate(False)
            tempLabel.grid(row=y, column=x, rowspan=SQRT, columnspan=SQRT, padx=1, pady=1)