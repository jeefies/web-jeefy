from jeefy import app as jeefy
from school.School import app as school
from multiprocessing import Process

def run(app, port):
    app.run(host='0.0.0.0', port=port)

li = [Process(target=run, args=(jeefy, '80')), Process(target=run, args=(school, '5000'))]
for l in li:
    l.run()
while li:
    li.pop().join()
