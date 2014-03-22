__author__ = 'roman_000'

import wx
# import os


class JobListPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
        self.jobs = kwds['queue']
        self.text_ctrl_output = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.button_clear_1 = wx.Button(self, wx.ID_ANY, "clear log", style=wx.BU_EXACTFIT)
        self.button_clear_1.SetSize((20, 50))

        #do layout
        sizer_right = wx.BoxSizer(wx.VERTICAL)
        sizer_right.Add(self.text_ctrl_output, 10, wx.EXPAND, 0)
        sizer_right.Add(self.button_clear_1, 1, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        self.SetSizer(sizer_right)

    def  update(self, **kwds):
            self.text_ctrl_output.Clear()
            for job in self.jobs:
                self.text_ctrl_output.WriteText(str(job[0].__name__) + ": " + str(job[1:]) + '\n')
