__author__ = 'roman_000'

import wx

class MovesPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']

    def update (self, **kwds):
        #botcommand = kwds['botcommand']
        pass
