#!/usr/bin/env python_32

import wx
import inspect
import sys
import json
import threading
import time
import Queue
import Crawler
from Panels import *


ID_EXIT         = wx.NewId()

class LogicThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while 1:
            if not self.queue.empty():
                task = self.queue.get()
                print task
                task[0](*task[1:])
            else:
                time.sleep(0.1)


class MainFrame(wx.Frame):
    """Simple terminal program for wxPython"""
    
    def __init__(self, *args, **kwds):
        self.bot = Crawler.Controller(sender = self.Sender)
        self.queue = Queue.Queue()
        thread = LogicThread(self.queue)
        thread.start()

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)


        #TODO: menu should be loaded from Panels
        # Menu Bar
        self.frame_terminal_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_terminal_menubar)
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(ID_EXIT, "&Exit", "", wx.ITEM_NORMAL)
        self.frame_terminal_menubar.Append(wxglade_tmp_menu, "&File")

        #Bot mgmt panels & buttons
        self.panels = {}

        self.nbtop_left     = wx.Notebook(self, wx.ID_ANY, style=0)
        self.nbbottom_left  = wx.Notebook(self, wx.ID_ANY, style=0)
        self.nbtop_right    = wx.Notebook(self, wx.ID_ANY, style=0)
        self.nbbottom_right = wx.Notebook(self, wx.ID_ANY, style=0)

        #TODO: add loading from settings file
        lo_topleft      = ["General", "Direction", "Moves", "TiltBody"]
        lo_bottomleft   = ["Angles", "Coordinates"]
        lo_topright     = ["Serial"]
        lo_bottomright  = ["Logic"]



        #TODO: add sorting and load order
        for mod in sys.modules:
            if mod[:7] == "Panels.":
                for name, obj in inspect.getmembers(sys.modules[mod]):
                    if inspect.isclass(obj) and name[-5:] == "Panel":
                        #print name
                        name = name[:-5]
                        if name in lo_topleft:
                            nb = self.nbtop_left
                        elif name in lo_bottomleft:
                            nb = self.nbbottom_left
                        elif name in lo_topright:
                            nb = self.nbtop_right
                        else:
                            nb = self.nbbottom_right
                        self.panels[name] = obj(nb, bot=self.bot, menubar=self.frame_terminal_menubar, runner = self.runner)
                        nb.AddPage(self.panels[name], name)

        self.SetTitle("Robot Terminal")
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetSize((1500, 900))

        #Do layout
        self.nbtop_left.SetMinSize((500, 400))
        self.nbbottom_left.SetMinSize((500, 400))
        self.nbtop_right.SetMinSize((500, 400))
        self.nbbottom_right.SetMinSize((500, 400))

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_left = wx.BoxSizer(wx.VERTICAL)
        sizer_right = wx.BoxSizer(wx.VERTICAL)

        sizer_left.Add(self.nbtop_left, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND, 3)
        sizer_left.Add(self.nbbottom_left, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND, 3)

        sizer_right.Add(self.nbtop_right, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND, 3)
        sizer_right.Add(self.nbbottom_right, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND, 3)

        sizer_1.Add(sizer_left, 1, wx.ALL | wx.EXPAND, 0)
        sizer_1.Add(sizer_right, 2, wx.ALL | wx.EXPAND, 0)


        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        self.Layout()

        #register events at the controls
        self.Bind(wx.EVT_MENU, self.OnExit, id = ID_EXIT)

        for panel in self.panels.itervalues():
            for name, obj in inspect.getmembers(panel):
                    if name == "onStart":
                        panel.onStart()

        self.bot.initBot()

    def OnExit(self, event):
        """Menu point Exit"""
        self.Close()


    def Sender(self, **kwds):
        #Update GUI with new bot state

        for (pname, panel) in self.panels.iteritems():
            for name, obj in inspect.getmembers(panel):
                if 'start' in kwds:
                    if name == "start":
                        panel.start()
                if 'botcommand' in kwds or 'message' in kwds:
                    if name == "update":
                        bc, ms = kwds['botcommand'], kwds['message']
                        # print >> sys.stderr, pname, bc, ms
                        panel.update(botcommand = bc, message=ms)

    def runner(self, *args):
        # print args
        self.queue.put(args)

class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_main = MainFrame(None, -1, "")
        self.SetTopWindow(frame_main)
        frame_main.Show(1)
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
