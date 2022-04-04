import os

cwd = os.getcwd().replace("\\", "/")

exec(open(cwd + '/app/lib/window.py').read())