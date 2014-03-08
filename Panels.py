__author__ = 'roman_000'
import wx

class Angles(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']

        grid_sizer_1     = wx.FlexGridSizer(len(self.bot.legs)*2, 3, 2, 2)
        self.sliders     = []
        #self.name_label  = []

        #n=0
        for i in range(self.bot.servo_number):
            #self.name_label.append(wx.StaticText(self, wx.ID_ANY, str(l.name)))
            #grid_sizer_1.Add(self.name_label[n], 0,  wx.ALL, 4)
            #for j in range(2):
            #    grid_sizer_1.Add((1, 1), 0, wx.ALL, 4)

            self.sliders.append(wx.Slider(self, wx.ID_ANY, 1500, 500, 2500,
                                          style=wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_TOP,
                                          name="servo%i" % i))
            self.sliders[i].SetMinSize((150, -1))
            grid_sizer_1.Add(self.sliders[i], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
            #n += 1

        self.SetSizer(grid_sizer_1)


class Coordinats(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']

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



class Direction(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        #self.bot = kwds['bot']

        self.button_forward = wx.Button(self, wx.ID_ANY, ("forward"))
        self.button_left = wx.Button(self, wx.ID_ANY, ("left"))
        self.button_right = wx.Button(self, wx.ID_ANY, ("right"))
        self.button_back = wx.Button(self, wx.ID_ANY, ("backward"))

        self.button_forward.SetMinSize((140, 140))
        self.button_left.SetMinSize((140, 140))
        self.button_right.SetMinSize((140, 140))
        self.button_back.SetMinSize((140, 140))

        grid_sizer_1 = wx.FlexGridSizer(3, 3, 1, 1)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_forward, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_left, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((150, 150), 0, 0, 0)
        grid_sizer_1.Add(self.button_right, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_back, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(grid_sizer_1)


class Moves(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        #self.bot = kwds['bot']

