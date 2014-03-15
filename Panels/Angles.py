__author__ = 'roman_000'

import wx


class AnglesPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']

        if self.bot.inited:
            self.start()

    def start(self):
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
                if botcommand:
                    for x in botcommand:
                        self.sliders[x['servo']].SetValue(x['position'])

