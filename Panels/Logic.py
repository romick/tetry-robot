__author__ = 'roman_000'

import wx
import sys


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
        pass
