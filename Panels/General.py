__author__ = 'roman_000'

import wx

class GeneralPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
        self.button_6 = wx.Button(self, wx.ID_ANY, ("reset all servos"))
        self.button_7 = wx.Button(self, wx.ID_ANY, ("Start robot"))
        sizer_left = wx.BoxSizer(wx.VERTICAL)
        sizer_left.Add(self.button_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_left.Add(self.button_7, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(sizer_left)

        self.Bind(wx.EVT_BUTTON, self.reset_button_pressed, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.OnStartRobot, self.button_7)

    def OnStartRobot(self, event):
        self.bot.initBot()

    def reset_button_pressed(self, event):
                    self.bot.initBot()

    def update (self, **kwds):
        #botcommand = kwds['botcommand']
        pass
