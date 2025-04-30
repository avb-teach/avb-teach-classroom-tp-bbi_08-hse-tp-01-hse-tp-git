import os
import sys

args = sys.argv
mx = 1
command_mkdr = "mkdir -p ?"
command_cp = "cp ? ?"

if len(args) == 5:
    mx = int(args[4])
for elem in os.walk(args[1]):
    sz = len(args[1].split('/'))
    pth = elem[0].split(
        '/'
    )[sz:]
    for i in range(max(0, len(pth) - mx + 1), len(pth)):
        os.system(command_mkdr.replace('?', args[2] + "/" + '/'.join(pth[:i + 1])))

    for file in elem[2]:
        os.system(command_cp.replace('?', elem[0] + "/" + file, 1)
            .replace('?', args[2] + "/" + '/'.join(pth[max(0, len(pth) - mx + 1):])))




