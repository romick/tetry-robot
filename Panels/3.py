__author__ = 'roman_000'
import wx

class DemoFrame(wx.Frame):
    """ This window displays a set of buttons """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        for button_name in ["first", "second", "third"]:
            btn = wx.Button(self, label=button_name)

            def OnButton(event, button_label=button_name):
                print "In OnButton:", button_label

            btn.Bind(wx.EVT_BUTTON, OnButton)
            sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizerAndFit(sizer)


app = wx.App(False)
frame = DemoFrame(None, title="Lambda Bind Test")
frame.Show()
app.MainLoop()