__author__ = 'roman_000'
import sys
import inspect
import datetime
import time
# import TetryQueue


from flask import Flask, render_template, request, jsonify
# from flask import jsonify, abort


class FlaskRunner:

    def __init__(self):
        # self.log = TetryQueue.TetryQueue()
        self.app = Flask(__name__)

    # def dummysender(self, **kwds):
    #         print(kwds)
    #
    # def dummylogger(self, level, *args, **kwds):
    #     """
    #     Placeholder for logger
    #
    #     """
    #     st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #     calling_frame = inspect.getouterframes(inspect.currentframe(), 2)
    #     record = (st, calling_frame[1][1:4], args, kwds)
    #     self.log.put(record)
    #     if level < 0:
    #         print >> sys.stderr, record
    #     else:
    #         print(record)

fl = FlaskRunner()
app = fl.app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tetry/api/1.0/logs/', methods=['GET'])
def send_log_updates():
    try:
        record = fl.log.get_nowait()
        return jsonify({'empty': fl.log.empty(), 'record': record})
    except:
        return jsonify({'empty': True, 'record': None})

@app.route('/tetry/api/1.0/panels/<panel_name>', methods=['GET'])
def send_panels_list(panel_name):

    return None

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
