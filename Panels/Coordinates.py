__author__ = 'roman_000'

import wx
import wx.grid
# import sys


class CoordinatesPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
        self.runner = kwds['runner']

        if self.bot.inited:
            self.start()
        self.grid_sizer_1 = wx.FlexGridSizer(1, 6, 1, 1)
        self.button_go = wx.Button(self, wx.ID_ANY, "Go!")
        self.leg_coordinates = []

    def clean(self):
        for ch in self.leg_coordinates:
            for i in ch:
                i.Destroy()
        self.grid_sizer_1.Clear()
        self.grid_sizer_1.Destroy()
        self.leg_coordinates = []

    def start(self):

        self.clean()
        self.grid_sizer_1 = wx.FlexGridSizer(len(self.bot.legs), 7, 1, 1)

        self.leg_coordinates = range(len(self.bot.legs))

        for l in self.bot.legs:
            self.leg_coordinates[l.id] = [wx.StaticText(self, wx.ID_ANY, str(l.name)),
                                     wx.StaticText(self, wx.ID_ANY, "X:"),
                                     wx.TextCtrl(self, wx.ID_ANY, str(l.stateX)),
                                     wx.StaticText(self, wx.ID_ANY, "Y:"),
                                     wx.TextCtrl(self, wx.ID_ANY, str(l.stateY)),
                                     wx.StaticText(self, wx.ID_ANY, "Z:"),
                                     wx.TextCtrl(self, wx.ID_ANY, str(l.stateZ))]

            for t in self.leg_coordinates[l.id]:
                self.grid_sizer_1.Add(t, 0, wx.ALL, 4)

        for i in range(13):
            self.grid_sizer_1.Add((1, 1), 0, wx.ALL, 4)
        self.grid_sizer_1.Add(self.button_go, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(self.grid_sizer_1)
        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.go_coordinates_button_pressed, self.button_go)

    def go_coordinates_button_pressed(self, event):
        coord_d = range(len(self.leg_coordinates))
        for n in range(len(self.leg_coordinates)):
            coord_d[n] = [int(self.leg_coordinates[n][2].GetValue()),
                          int(self.leg_coordinates[n][4].GetValue()),
                          int(self.leg_coordinates[n][6].GetValue())]

        self.runner(self.bot.move_to_coordinates, coord_d)

    def update(self, **kwds):
        for l in self.bot.legs:
            # print >> sys.stderr, l #.stateX, l.stateY, l.stateZ
            self.leg_coordinates[l.id][2].SetValue(str(self.bot.legs[l.id].stateX))
            self.leg_coordinates[l.id][4].SetValue(str(self.bot.legs[l.id].stateY))
            self.leg_coordinates[l.id][6].SetValue(str(self.bot.legs[l.id].stateZ))
            self.Update()
