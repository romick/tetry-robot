__author__ = 'roman_000'

import wx


class DirectionPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot    = kwds['bot']
        self.runner = kwds['runner']
        self.buttons = []

        b_metadata = {"forward-left":315, "forward": 0,"forward-right":45, "left":270, "right":90,"backward-left":225, "backward":180, "backward-right":135}
        for button_label, angle in b_metadata.iteritems():
            b = wx.Button(self, wx.ID_ANY, (button_label))
            self.buttons.append(b)
            b.SetMinSize((50, 50))
            self.Bind(wx.EVT_BUTTON, lambda evt, an = angle: self.button_pressed(evt, an))


        grid_sizer_1 = wx.FlexGridSizer(3, 3, 1, 1)

        # self.gaits = ["tripod", "wave", ""]

        grid_sizer_1.Add(self.buttons[0], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[1], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[2], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[3], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((200, 200), 0, 0, 0)
        grid_sizer_1.Add(self.buttons[4], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[5], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[6], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[7], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(grid_sizer_1)


    def button_pressed(self, event, angle):
                    self.runner(self.bot.makeStep,angle)

