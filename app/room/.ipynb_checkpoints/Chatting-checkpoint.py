class Chatting:

def __init__(self, name):
self.name = name + ".txt"

def add(self, context):
with open(self.name, 'a', encoding = "utf-8") as f:
f.writeline(context)

@property
def context(self):
with open(self.name, "r", encoding = 'utf-8') as f:
con = f.readlines()
return con

@context.setter
def context(self, *args):
for arg in args:
self.add(arg)