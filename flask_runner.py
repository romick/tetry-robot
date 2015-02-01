__author__ = 'roman_000'
import sys
import inspect
import datetime
import time
import TetryQueue


from flask import Flask, render_template, request, jsonify
# from flask import jsonify, abort


class FlaskRunner:

    def __init__(self):
        self.log = TetryQueue.TetryQueue()
        self.app = Flask(__name__)

    def dummysender(self, **kwds):
            print(kwds)

    def dummylogger(self, level, *args, **kwds):
        """
        Placeholder for logger

        """
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        calling_frame = inspect.getouterframes(inspect.currentframe(), 2)
        record = (st, calling_frame[1][1:4], args, kwds)
        self.log.put(record)
        if level < 0:
            print >> sys.stderr, record
        else:
            print(record)

fl = FlaskRunner()
app = fl.app


@app.route('/')
def index():
    # bot.sender(log="Hello!")
    return render_template('index.html')


@app.route('/tetry/api/1.0/tasks/', methods=['POST'])
def add_task_to_queue():
    # TODO: add code to save task to queue
    fl.dummylogger(1, request.json)
    # if not request.json or not 'name' in request.json:
    #     abort(400)
    #
    # if hasattr(bot, request.json['command']):
    #     func = getattr(bot, request.json['command'])
    #     result = func(int(request.json['data']))
    #     return jsonify({'status':'saved', 'name': request.json['name']})
    # else:
    #     return jsonify({'status':'fail'})
    return "result"

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
    try:
        record = fl.log.get_nowait()
        return jsonify({'empty': fl.log.empty(), 'record': record})
    except:
        return jsonify({'empty': True, 'record': None})
    # else:
    #     raise
    # return "result"


if __name__ == '__main__':
    # bot = Crawler.Controller(sender=dummysender, logger=dummylogger)
    # bot.load_settings("./Robots/tetry.json")
    # queue = TetryQueue.TetryQueue()
    app.debug = True
    app.run(host='0.0.0.0')
