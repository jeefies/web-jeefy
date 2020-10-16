import os

os.chdir(r'C:\Program Files (x86)\3000soft')

li = os.listdir(os.getcwd())

if 'Red Spider' in li:
    os.rename('Red Spider', 'changed')
else:
    os.rename(li[0], 'Red Spider')

print(os.listdir(os.getcwd()))
