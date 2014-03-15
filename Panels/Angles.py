__author__ = 'roman_000'

import wx
import sys


class AnglesPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']

        if self.bot.inited:
            self.start()
        self.grid_sizer_1   = wx.FlexGridSizer(1, 1, 2, 2)
        self.sliders        = []

    def clean(self):
        for sl in self.sliders:
            sl.Destroy()
        self.grid_sizer_1.Clear()
        self.grid_sizer_1.Destroy()
        self.sliders        = []


    def start(self):
        self.clean()
        self.grid_sizer_1   = wx.FlexGridSizer(len(self.bot.legs)*2, 3, 2, 2)
        self.sliders        = []
        for i in range(self.bot.servo_number):

            self.sliders.append(wx.Slider(self, wx.ID_ANY, 1500, 500, 2500,
                                          style=wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_TOP,
                                          name="servo%i" % i))
            self.sliders[i].SetMinSize((150, -1))
            self.grid_sizer_1.Add(self.sliders[i], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(self.grid_sizer_1)
        self.Layout()

        for i in range(self.bot.servo_number):
            self.Bind(wx.EVT_SCROLL_CHANGED , self.servo_move, self.sliders[i])


    def servo_move(self, event):
                command = []
                for s in range(self.bot.servo_number):
                    command.append(dict(servo=s, position=self.sliders[s].GetValue()))
                self.bot._send(command)

    def update (self, **kwds):
                botcommand  = kwds['botcommand']
                # print >> sys.stderr, botcommand
                if botcommand:
                    for x in botcommand:
                        # print >> sys.stderr, x
                        self.sliders[x['servo']].SetValue(x['position'])

