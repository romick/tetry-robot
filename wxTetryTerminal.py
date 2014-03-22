#!/usr/bin/env python_32

import wx
import wx.aui
import wx.lib.agw.aui as aui
import inspect
import sys
# import json
import threading
import time
import Crawler
from Panels import *


ID_EXIT = wx.NewId()


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


import Queue


class IndexQueue(Queue.Queue):
    def __getitem__(self, index):
        with self.mutex:
            return self.queue[index]


class MainFrame(wx.Frame):
    """Simple terminal program for wxPython"""

    def __init__(self, *args, **kwds):
        self.bot = Crawler.Controller(sender=self.sender)
        self.queue = IndexQueue()
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
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(self)

        self.panels = {}

        #TODO: add loading from settings file
        lo_commands = ["Direction", "General", "Moves", "TiltBody"]
        lo_state = ["Angles", "Coordinates", "JobList"]
        lo_logs = ["Serial", "Logic"]

        left_nb = None
        center_nb = None
        for mod in sys.modules:
            if mod[:7] == "Panels.":
                for name, obj in inspect.getmembers(sys.modules[mod]):
                    if inspect.isclass(obj) and name[-5:] == "Panel":
                        name = name[:-5]
                        self.panels[name] = obj(self,
                                                bot=self.bot,
                                                menubar=self.frame_terminal_menubar,
                                                window=self,
                                                queue=self.queue,
                                                runner=self.runner)
                        pane = aui.AuiPaneInfo().Caption(name).MinSize(350, 300)
                        if name in  lo_commands:
                            self.mgr.AddPane(self.panels[name], pane.Left(), target=left_nb)
                            if left_nb is None:
                                left_nb = pane
                        if name in  lo_logs:
                            self.mgr.AddPane(self.panels[name], pane.Bottom())
                        if name in  lo_state:
                            self.mgr.AddPane(self.panels[name], pane.Center(), target=center_nb)
                            if center_nb is None:
                                center_nb = pane

        self.SetTitle("Robot Terminal")
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetSize((1500, 900))
        self.Maximize()

        self.mgr.Update()



        #register events at the controls
        self.Bind(wx.EVT_MENU, self.on_exit, id=ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        for panel in self.panels.itervalues():
            for name, obj in inspect.getmembers(panel):
                if name == "on_start":
                    panel.on_start()

        self.bot.init_bot()

    def on_exit(self, event):
        """Menu point Exit"""
        self.mgr.UnInit()
        self.Close()

    def on_close(self, event):
        for (pname, panel) in self.panels.iteritems():
            for name, obj in inspect.getmembers(panel):
                if name == "on_close":
                    panel.on_close()
        self.Destroy()

    def sender(self, **kwds):
        #Update GUI with new bot state

        for (pname, panel) in self.panels.iteritems():
            for name, obj in inspect.getmembers(panel):
                if 'start' in kwds:
                    if name == "start":
                        panel.start()
                if 'bot_command' in kwds or 'message' in kwds:
                    if name == "update":
                        bc, ms = kwds['bot_command'], kwds['message']
                        # print >> sys.stderr, pname, bc, ms
                        panel.update(bot_command=bc, message=ms)

    def runner(self, *args):
        # print args
        self.queue.put(args)


class MyApp(wx.App):
    def OnInit(self):
        # wx.InitAllImageHandlers()
        frame_main = MainFrame(None, -1, "")
        self.SetTopWindow(frame_main)
        frame_main.Show(1)
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
