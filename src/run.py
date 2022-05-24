import logging

from src.window.main import mainWindow

from src import __version__, LOGDEBUG, LOGSOLVE

def main():
    print(f"Running Sudoku Solver : Version # {__version__}")
    logging.basicConfig(level=logging.DEBUG)
    app = mainWindow()
    app.mainloop()
    #94..2..38...418..............7.8.5...6.1.3.4...5.6.2..............231...21..4..96
    #7..3.9..1....5....82..6.....59.....36.2...1.93.....65.....7..94....8....9..1.3..7