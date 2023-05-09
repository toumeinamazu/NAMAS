#! /usr/bin/env python3

import sys
args = sys.argv


splist=args[1]
originaltre=args[2]
newtre=args[3]


baka=[]
with open(splist, mode='r') as f:
    for line in f:
        baka.append(line.strip())
print(baka)


with open(originaltre, mode='r') as f:
    for line in f:
        print(line)
        for aho in baka:
            aho_trim=aho.split('_')
            aho_trim=aho_trim[0]+'_'+aho_trim[1]
            line=line.replace(aho_trim, aho)

with open(newtre, mode="w") as f:
    for uma in line:
        f.write(uma)
    
            
            