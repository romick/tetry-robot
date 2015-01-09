__author__ = 'roman_000'
import Crawler

from flask import Flask, jsonify

app = Flask(__name__)

class MainLoop():
    """Bot logic"""

    def __init__(self):
        self.bot = Crawler.Controller(sender=self.dummysender)


    def dummysender(self, **kwds):
        print(kwds)

@app.route('/')
def hello_world():
    # some = jsonify(loop.bot)
    bot.sender(log="Hello!")

    return render_template('Hello World!'

if __name__ == '__main__':
    loop = MainLoop()
    bot = loop.bot
    app.debug = True
    app.run()

