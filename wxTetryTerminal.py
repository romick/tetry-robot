#!/usr/bin/env python_32

import inspect
import sys

import wx
import wx.aui
import wx.lib.agw.aui as aui
import Crawler
from RunnerThread import RunnerThread
from TetryQueue import TetryQueue


ID_EXIT = wx.NewId()


class MainFrame(wx.Frame):
    """Simple terminal program for wxPython"""

    def __init__(self, *args, **kwds):
        self.bot = Crawler.Controller(sender=self.sender, logger=self.dummylogger)
        self.queue = TetryQueue()
        self.total_block = False

        thread = RunnerThread(self.queue)
        thread.start()

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        #TODO: menu should be loaded from Panels
        # Menu Bar
        self.frame_terminal_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_terminal_menubar)
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_ANY, "&Block", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(ID_EXIT, "&Exit", "", wx.ITEM_NORMAL)
        self.frame_terminal_menubar.Append(wxglade_tmp_menu, "&File")

        #Bot mgmt panels & buttons
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(self)
        self.mgr.SetAutoNotebookStyle(aui.AUI_NB_TAB_EXTERNAL_MOVE |
                                      aui.AUI_NB_TAB_MOVE |
                                      aui.AUI_NB_BOTTOM |
                                      aui.AUI_NB_WINDOWLIST_BUTTON |
                                      aui.AUI_NB_CLOSE_ON_ALL_TABS |
                                      aui.AUI_NB_HIDE_ON_SINGLE_TAB |
                                      aui.AUI_NB_ORDER_BY_ACCESS |
                                      aui.AUI_NB_NO_TAB_FOCUS)
        self.mgr.SetAutoNotebookTabArt(aui.ChromeTabArt())

        #Find all panels
        self.panels_objects = {}  # placeholder for panels objects
        self.panels_classes = {}  # placeholder for panel classes
        for mod in sys.modules:
            if mod[:7] == "Panels.":
                for name, obj in inspect.getmembers(sys.modules[mod]):
                    if inspect.isclass(obj) and name[-5:] == "Panel":
                        name = name[:-5]
                        self.panels_classes[name] = obj

        #TODO: add loading from settings file
        ui_setting = [
            {'tabs': ["Moves", "Direction", "ShiftBody", "TiltBody"],
             'position': "Left",
             'size': (350,300),
             'stacked': True},
            {'tabs': ["JobList", "Logic", "Serial"],
             'position': "Bottom",
             'size': (350,300)},
            {'tabs': ["Angles", "Coordinates"],
             'position': "Right",
             'size': (450,300),
             'stacked': True},
            {'tabs': ["Virtual", ],
             'position': "Center",
             'size': (350,300)}
            ]
        default_tabs = ["Direction", "Angles"]

        for set in ui_setting:
            position_target = None
            for nm in set['tabs']:
                # self.dummmylogger(1, nm, position_target, direction)
                self.panels_objects[nm] = self.panels_classes[nm](self,
                                                                  bot=self.bot,
                                                                  menubar=self.frame_terminal_menubar,
                                                                  window=self,
                                                                  queue=self.queue,
                                                                  runner=self.runner)
                trgt = None
                position_function = None
                if 'stacked' in set.keys():
                    trgt = position_target
                if set['size'] is not None:
                    pane = aui.AuiPaneInfo().Caption(nm).Name(nm).MinSize(set['size'])
                if set['position'] == "Left":
                    position_function = pane.Left
                elif set['position'] == "Right":
                    position_function = pane.Right
                elif set['position'] == "Bottom":
                    position_function= pane.Bottom
                elif set['position'] == "Center":
                    position_function = pane.Center

                self.mgr.AddPane(self.panels_objects[nm], position_function(), target=trgt)
                if position_target is None:
                    position_target = pane

        self.mgr.Update()

        for p in self.panels_objects:
            self.dummmylogger(1, p)

        #activate tabs according to default_tabs setting
        for nb in self.mgr.GetNotebooks():
            for i in range(nb.GetPageCount()):
                if nb.GetPageText(i) in default_tabs:
                    nb.SetSelection(i)

        self.SetTitle("Robot Terminal")
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        # self.SetSize((1500, 900))
        self.Maximize()
        self.mgr.Update()

        #register events at the controls
        self.Bind(wx.EVT_MENU, self.on_exit, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_toggle_block)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        #run "on_start" hooks in all panels
        for panel in self.panels_objects.itervalues():
            for name, obj in inspect.getmembers(panel):
                if name == "on_start":
                    panel.on_start()

        self.bot.init_bot()

    def on_exit(self, event):
        """Menu point Exit"""
        self.Close()

    def on_toggle_block(self, event):
        if not self.total_block:
            self.total_block = True
            while not self.queue.empty():
                self.queue.get()
        else:
            self.total_block = False

    def on_close(self, event):
        self.mgr.UnInit()
        for (pname, panel) in self.panels_objects.iteritems():
            for name, obj in inspect.getmembers(panel):
                if name == "on_close":
                    panel.on_close()
        self.Destroy()

    def sender(self, **kwds):
        #Update GUI with new bot state
        for (pname, panel) in self.panels_objects.iteritems():
            for name, obj in inspect.getmembers(panel):
                if 'start' in kwds:
                    if name == "start":
                        panel.start()
                if 'bot_command' in kwds or 'message' in kwds:
                    if not self.total_block:
                        if name == "update":
                            bc, ms = kwds['bot_command'], kwds['message']
                            # self.dummmylogger(-1, pname, bc, ms)
                            panel.update(bot_command=bc, message=ms)
                    else:
                        if name == "stop":
                            panel.stop()
                if 'update' in kwds:
                    if name == "update":
                        panel.update()

    def runner(self, *args):
        # self.dummmylogger(1, args)
        self.queue.put(args)

    def dummylogger(level, *args, **kwds):
        """
        Placeholder for logger

        """
        if level < 0:
            print >> sys.stderr, args, kwds
        else:
            print(args, kwds)

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
