import os, glob

al = os.listdir('.')
li = []
for l in al:
    if l.endswith('.txt'):
        li.append(l)
input(li)
for n in li:
    with open(n, 'r', encoding='utf-8') as f:
        con=f.read()
    con=con.replace('@#;', chr(1138)).replace('&#:', chr(1136))
    with open(n, 'w', encoding='utf-8') as f:
        f.write(con)
