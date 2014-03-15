__author__ = 'roman_000'

import wx

class CoordinatesPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']

        if self.bot.inited:
            self.start()



    def start(self):
        grid_sizer_1 = wx.FlexGridSizer(len(self.bot.legs)*2, 6, 1, 1)
        self.leg_coords  = {}

        self.button_go = wx.Button(self, wx.ID_ANY, ("Go!"))

        n=0
        for l in self.bot.legs.values():
            #print >> sys.stderr, l

            self.label_x = wx.StaticText(self, wx.ID_ANY, "X:")
            self.label_y = wx.StaticText(self, wx.ID_ANY, "Y:")
            self.label_z = wx.StaticText(self, wx.ID_ANY, "Z:")

            self.leg_coords[l.name]  = [wx.StaticText(self, wx.ID_ANY, str(l.name)),
                                        wx.TextCtrl(self, wx.ID_ANY, str(l.stateX)),
                                        wx.TextCtrl(self, wx.ID_ANY, str(l.stateY)),
                                        wx.TextCtrl(self, wx.ID_ANY, str(l.stateZ))]

            grid_sizer_1.Add(self.leg_coords[l.name][0], 0,  wx.ALL, 4)
            for i in range(5):
                grid_sizer_1.Add((1, 1), 0, wx.ALL, 4)

            grid_sizer_1.Add(self.label_x, 0, wx.ALL, 4)
            grid_sizer_1.Add(self.leg_coords[l.name][1], 0, wx.ALL, 4)
            grid_sizer_1.Add(self.label_y, 0, wx.ALL, 4)
            grid_sizer_1.Add(self.leg_coords[l.name][2], 0, wx.ALL, 4)
            grid_sizer_1.Add(self.label_z, 0, wx.ALL, 4)
            grid_sizer_1.Add(self.leg_coords[l.name][3], 0, wx.ALL, 4)
            n = n+1

        for i in range(11):
            grid_sizer_1.Add((1, 1), 0, wx.ALL, 4)
        grid_sizer_1.Add(self.button_go, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(grid_sizer_1)
        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.gocoord_button_pressed, self.button_go)

    def gocoord_button_pressed(self, event):
                    coord_d = {}
                    for n in self.leg_coords:
                        coord_d[n]=[int(self.leg_coords[n][1].GetValue()),
                                    int(self.leg_coords[n][2].GetValue()),
                                    int(self.leg_coords[n][3].GetValue())]

                    self.bot.moveToCoordinates(coord_d)

    def update (self, **kwds):
                #botcommand = kwds['botcommand']
                n=0
                for l in self.bot.legs.keys():
                    #print >> sys.stderr, l.stateX, l.stateY, l.stateZ
                    self.leg_coords[l][1].SetValue(str(self.bot.legs[l].stateX))
                    self.leg_coords[l][2].SetValue(str(self.bot.legs[l].stateY))
                    self.leg_coords[l][3].SetValue(str(self.bot.legs[l].stateZ))
                    self.Update()
                    n += 1
