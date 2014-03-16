__author__ = 'roman_000'

import wx
import os
import re


class MovesPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
    moves = []
    for fileName in os.listdir('Moves'):
        if os.path.splitext(fileName)[1] == '.py':
            fileName = os.path.splitext(fileName)[0]
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', fileName)
            moves.append(s1)