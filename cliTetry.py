__author__ = 'roman_000'
import Crawler

from flask import Flask, jsonify, render_template, request, abort
from redis import Redis
from rq import Queue


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
    print request.json
    if not request.json or not 'name' in request.json:
        abort(400)
    # func = bot.make_step
    # for name, obj in inspect.getmembers(panel):
    if hasattr(bot, request.json['command']):
        func = getattr(bot, request.json['command'])
        result = func(int(request.json['data']))

    # bot.make_step(int(request.json['angle']))
    return jsonify({'status':'saved', 'name': request.json['name']})

# @app.route('/tetry/api/1.0/tasks/<filter_group>', methods=['GET'])
# def list_available_tasks(filter_group):
#     tasks = {
#         'moves': [('example', ""), ('test', "")],
#         'direction': [('forward', 0), ('right', 90), ('left', 270), ('backward', 180)],
#         'shiftbody': [('shiftforward', 0), ('shiftright', 90), ('shiftleft', 270), ('shiftbackward', 180)],
#         'tiltbody':  [('tiltforward', 0), ('tiltright', 90), ('tiltleft', 270), ('tiltbackward', 180)],
#         'undefined': [None]
#
#     }
#     list = tasks[filter_group]
#     bot.sender(log=list)
#     return render_template('commands.html', commands=list)

if __name__ == '__main__':
    loop = MainLoop()
    bot = loop.bot
    bot.load_settings("./Robots/tetry.json")
    q = Queue(connection=Redis())
    # q = TaskQueue()
    app.debug = True
    app.run(host='0.0.0.0')

