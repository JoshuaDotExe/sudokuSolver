import os

cwd = os.getcwd().replace("\\", "/")
# Calls tests
for fileName in os.listdir(cwd + "/app/testing"):
    if fileName[0:5] == "test_":    # Only allows test_* files
        exec(open(cwd + "/app/testing/" + fileName).read())

print("Done!")
exec(open(cwd + "/app/lib/sudoku").read())