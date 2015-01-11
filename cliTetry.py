__author__ = 'roman_000'
import sys
import Crawler
import inspect
import datetime, time
from TetryQueue import TetryQueue


from flask import Flask, jsonify, render_template, request, abort


app = Flask(__name__)
log_q = TetryQueue()

def dummysender(**kwds):
        print(kwds)

def dummylogger(level, *args, **kwds):
    """
    Placeholder for logger

    """
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    calling_frame = inspect.getouterframes(inspect.currentframe(),2)
    record = (st, calling_frame[1][1:4], args, kwds)
    log_q.put(record)
    if level < 0:
        print >> sys.stderr, record
    else:
        print(record)

@app.route('/')
def index():
    bot.sender(log="Hello!")
    return render_template('index.html')

@app.route('/tetry/api/1.0/tasks/', methods=['POST'])
def add_task_to_queue():
    #TODO: add code to save task to queue
    dummylogger(1, request.json)
    if not request.json or not 'name' in request.json:
        abort(400)

    if hasattr(bot, request.json['command']):
        func = getattr(bot, request.json['command'])
        result = func(int(request.json['data']))
        return jsonify({'status':'saved', 'name': request.json['name']})
    else:
        return jsonify({'status':'fail'})

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

@app.route('/tetry/api/1.0/logs/', methods=['GET'])
def send_log_updates():
    record = log_q.get_nowait()
    return jsonify({'empty':log_q.empty(), 'record': record})

if __name__ == '__main__':
    bot = Crawler.Controller(sender=dummysender, logger=dummylogger)
    bot.load_settings("./Robots/tetry.json")
    queue = TetryQueue()
    app.debug = True
    app.run(host='0.0.0.0')

