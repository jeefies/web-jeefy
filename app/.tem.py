import os
import sys

walker = os.walk('templates')


def change(con):
    con = con.replace('{ %', '{%').replace('% }', '%}')
    con = con.replace('{ #', '{#').replace('# }', '#}')
    con = con.replace('< /', '</').replace(' = ', '=')
    con = con.replace('> ', '>').replace(' <', '<')
    con = con.replace('{{', '{{ ').replace('}}', ' }}')
    return con


for root, paths, files in walker:
    for file in files:
        if file.endswith('.html'):
            with open(os.path.join(root, file)) as f:
                res = change(f.read())
            with open(os.path.join(root, file), 'w') as f:
                f.write(res)
