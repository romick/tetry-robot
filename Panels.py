__author__ = 'roman_000'
import wx
import sys

class AnglesPanel(wx.Panel):
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

        for i in range(self.bot.servo_number):
            self.Bind(wx.EVT_SCROLL_CHANGED , self.servo_move, self.sliders[i])

    def servo_move(self, event):
                command = []
                for s in range(self.bot.servo_number):
                    command.append(dict(servo=s, position=self.sliders[s].GetValue()))
                self.bot._send(command)

    def update (self, **kwds):
                botcommand = kwds['botcommand']
                if botcommand:
                    for x in botcommand:
                        self.sliders[x['servo']].SetValue(x['position'])



class CoordinatsPanel(wx.Panel):
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

        self.Bind(wx.EVT_BUTTON, self.gocoord_button_pressed, self.button_go)

    def gocoord_button_pressed(self, event):
                    coord_d = {}
                    for n in self.coordinatsPanel.leg_coords:
                        coord_d[n]=[int(self.coordinatsPanel.leg_coords[n][1].GetValue()),
                                    int(self.coordinatsPanel.leg_coords[n][2].GetValue()),
                                    int(self.coordinatsPanel.leg_coords[n][3].GetValue())]

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


class DirectionPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']

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

        self.Bind(wx.EVT_BUTTON, self.forward_button_pressed, self.button_forward)
        self.Bind(wx.EVT_BUTTON, self.left_button_pressed, self.button_left)
        self.Bind(wx.EVT_BUTTON, self.right_button_pressed, self.button_right)
        self.Bind(wx.EVT_BUTTON, self.back_button_pressed, self.button_back)

    def forward_button_pressed(self, event):
                    self.bot.makeStep(0)

    def left_button_pressed(self, event):
                    self.bot.makeStep(270)

    def right_button_pressed(self, event):
                    self.bot.makeStep(90)

    def back_button_pressed(self, event):
                    self.bot.makeStep(180)

    def update (self, **kwds):
        botcommand = kwds['botcommand']



class MovesPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']

    def update (self, **kwds):
        #botcommand = kwds['botcommand']
        None

#worker for LogicPanel sys output redirection
class RedirectText:
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string) #supporting class to redirect stdout to textcontrol

class LogicPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
        #redirect stdout to text_ctrl_log
        self.text_ctrl_log = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        sys.stdout = RedirectText(self.text_ctrl_log)

        self.button_clear_2 = wx.Button(self, wx.ID_ANY, ("clear log"), style= wx.BU_EXACTFIT)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.text_ctrl_log, 1, wx.EXPAND, 0)
        sizer_3.Add(self.button_clear_2, 1,  wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        self.SetSizer(sizer_3)

        self.Bind(wx.EVT_BUTTON, self.clean_log, self.button_clear_2)

    def clean_log(self, event):
            self.text_ctrl_log.Clear()
            pass

    def update (self, **kwds):
        #botcommand = kwds['botcommand']
        None
