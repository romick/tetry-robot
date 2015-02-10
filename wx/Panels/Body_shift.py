__author__ = 'roman_000'

import wx
from wx.lib.floatcanvas import FloatCanvas
from TetryTools import MathTools
# import os


class ShiftBodyPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
        self.runner = kwds['runner']
        self.buttons = []

        b_labels = ["forward-left",
                    "forward",
                    "forward-right",
                    "left",
                    "right",
                    "backward-left",
                    "backward",
                    "backward-right"]
        b_angles = [315, 0, 45, 270, 90, 225, 180, 135]

        self.canvas_size = 150
        self.canvas = FloatCanvas.FloatCanvas(self, -1,
                                              size=(self.canvas_size, self.canvas_size),
                                              ProjectionFun=None,
                                              Debug=0,
                                              BackgroundColor="White")

        # add a circle
        cir = FloatCanvas.Circle((0, 0), self.canvas_size - 10, FillColor="Black")
        # self.cir2 = FloatCanvas.Circle((0, 0), 5, FillColor="White")
        self.canvas.AddObject(cir)
        # self.canvas.AddObject(self.cir2)
        FloatCanvas.EVT_MOTION(self.canvas, self._on_move)
        FloatCanvas.EVT_LEFT_DOWN(self.canvas, self._on_left_down)
        # Circle.Bind(FC.EVT_FC_LEFT_DOWN, self.object_hit)

        for i in range(len(b_labels)):
            # print b_angles[i]
            b = wx.Button(self, wx.ID_ANY, b_labels[i])
            self.buttons.append(b)
            b.SetMinSize((80, 80))

            def on_button(event, angle=b_angles[i]):
                print angle
                self.runner(self.bot.shift_body_angle, angle)

            b.Bind(wx.EVT_BUTTON, on_button)

        grid_sizer_1 = wx.FlexGridSizer(5, 3, 1, 1)

        #TODO: delete buttons
        grid_sizer_1.Add(self.buttons[0], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[1], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[2], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[3], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.canvas, 0, 0, 0)
        grid_sizer_1.Add(self.buttons[4], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[5], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[6], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.buttons[7], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(grid_sizer_1)
        self.canvas.Draw()

    def _on_move(self, event):
        pass

    def _on_left_down(self, event):
        #TODO: change event to fire with mouse key down, not only at the moment press
        dxy = event.GetPosition()
        dc = wx.ClientDC(self.canvas)
        dc.SetPen(wx.Pen('WHITE', 1))
        self.canvas.Draw(True)
        dc.DrawLine(self.canvas_size / 2, self.canvas_size / 2, dxy[0], dxy[1])
        dc.DrawCircle(dxy[0], dxy[1], 3)

        coordinates = event.GetCoords()
        self.runner(self.bot.shift_body_angle,
                    MathTools.coordinates2angle(*coordinates),
                    MathTools.vector_length(*coordinates))
        self.runner(self.bot.sleep, 0.5)