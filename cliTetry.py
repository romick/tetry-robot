__author__ = 'roman_000'
import Crawler

from flask import Flask, jsonify, render_template, request, abort

app = Flask(__name__)

class TaskQueue():
    """
    Placeholder for real task queue
    """
    def put_queue(self,**kwds):
        return None


class MainLoop():
    """
    Bot logic
    """
    def __init__(self):
        self.bot = Crawler.Controller(sender=self.dummysender)


    def dummysender(self, **kwds):
        print(kwds)

@app.route('/')
def index():
    bot.sender(log="Hello!")
    return render_template('index.html')

@app.route('/tetry/api/1.0/tasks/', methods=['POST'])
def add_task_to_queue():
    #TODO: add code to save task to queue
    if not request.json or not 'title' in request.json:
        abort(400)
    q.put_queue(json=request.json)
    return jsonify({'status':'saved'})

@app.route('/tetry/api/1.0/tasks/<filter_group>', methods=['GET'])
def list_available_tasks(filter_group):
    tasks = {
        'moves': ['example', 'test'],
        'direction': ['forward', 'right', 'left', 'backward'],
        'shiftbody': ['bodyforward', 'bodyright', 'bodyleft', 'bodybackward'],
        'tiltbody': ['tiltforward', 'tiltright', 'tiltleft', 'tiltbackward']

    }
    list = tasks[filter_group]
    bot.sender(log=list)
    return render_template('commands.html', commands=list)

if __name__ == '__main__':
    loop = MainLoop()
    bot = loop.bot
    q = TaskQueue()
    app.debug = True
    app.run()

