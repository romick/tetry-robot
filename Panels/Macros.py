__author__ = 'roman_000'

import wx
import inspect
import sys
from Moves import *


#TODO: totally rewrite using usual python commands, not tuple as a list of commands inside a class!
class MovesPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
        self.runner = kwds['runner']
        moves = []
        for mod in sys.modules:
            if mod[:6] == "Moves.":
                for name, obj in inspect.getmembers(sys.modules[mod]):
                    if inspect.isclass(obj) and not name == "Moves.GeneralMove.Move":
                        moves.append(obj(**kwds))
        print(moves)
        buttons = range(len(moves))
        for m in range(len(moves)):
            buttons[m] = wx.Button(self, wx.ID_ANY, moves[m].name)

            def on_button(evt, tasks=moves[m].tasks()):
                self.run_macro(tasks)
            buttons[m].Bind(wx.EVT_BUTTON, on_button)


    def run_macro(self, task_list):
        for m in task_list:
            method = None
            method_name = m[0]
            m = m[1:]
            for name, obj in inspect.getmembers(self.bot):
                if name == method_name:
                    method = obj
            self.runner(method, *m)

