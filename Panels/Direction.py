__author__ = 'roman_000'

import wx


class DirectionPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot    = kwds['bot']
        self.runner = kwds['runner']

        self.button_forward = wx.Button(self, wx.ID_ANY, ("forward"))
        self.button_left = wx.Button(self, wx.ID_ANY, ("left"))
        self.button_right = wx.Button(self, wx.ID_ANY, ("right"))
        self.button_back = wx.Button(self, wx.ID_ANY, ("backward"))

        self.button_forward.SetMinSize((100, 100))
        self.button_left.SetMinSize((100, 100))
        self.button_right.SetMinSize((100, 100))
        self.button_back.SetMinSize((100, 100))

        grid_sizer_1 = wx.FlexGridSizer(3, 3, 1, 1)

        self.gaits = ["tripod", "wave", ""]

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

        self.Bind(wx.EVT_BUTTON, self.forward_button_pressed, self.button_forward)
        self.Bind(wx.EVT_BUTTON, self.left_button_pressed, self.button_left)
        self.Bind(wx.EVT_BUTTON, self.right_button_pressed, self.button_right)
        self.Bind(wx.EVT_BUTTON, self.back_button_pressed, self.button_back)

    def forward_button_pressed(self, event):
                    self.runner(self.bot.makeStep,0)

    def left_button_pressed(self, event):
                    self.runner(self.bot.makeStep, 270)

    def right_button_pressed(self, event):
                    self.runner(self.bot.makeStep, 90)

    def back_button_pressed(self, event):
                    self.runner(self.bot.makeStep, 180)
