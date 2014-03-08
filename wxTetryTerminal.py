#!/usr/bin/env python_32

import wx
import inspect
import wxConfigDialog
import serial
import threading
import Crawler
import Panels

#----------------------------------------------------------------------
# Create an own event type, so that GUI updates can be delegated
# this is required as on some platforms only the main thread can
# access the GUI without crashing. wxMutexGuiEnter/wxMutexGuiLeave
# could be used too, but an event is more elegant.

SERIALRX = wx.NewEventType()
# bind to serial data receive events
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)

class SerialRxEvent(wx.PyCommandEvent):
    eventType = SERIALRX
    def __init__(self, windowID, data):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)

#----------------------------------------------------------------------

ID_CLEAR        = wx.NewId()
ID_SAVEAS       = wx.NewId()
ID_SETTINGS     = wx.NewId()
ID_TERM         = wx.NewId()
ID_EXIT         = wx.NewId()
ID_BOT          = wx.NewId()

NEWLINE_CR      = 0
NEWLINE_LF      = 1
NEWLINE_CRLF    = 2
NEWLINE         ='\n'

#PROTOCOL_CUSTOM     = 0
#PROTOCOL_COMPACT    = 1
#PROTOCOL_POLOLU     = 2
#PROTOCOL_MINISSC    = 3


#SERVO_NUMBER = 12

class TerminalSetup:
    """Placeholder for various terminal settings. Used to pass the
       options to the TerminalSettingsDialog."""
    def __init__(self):
        self.echo = False
        self.unprintable = False
        self.newline = NEWLINE_CRLF



class TerminalFrame(wx.Frame):
    """Simple terminal program for wxPython"""
    
    def __init__(self, *args, **kwds):
        self.bot = Crawler.Controller(sender = self.Sender, settings = './tetry.json')
        #bot_settings_file = open('./tetry.ini',mode='w+')
        #cPickle.dump(self.bot,bot_settings_file)

        self.serial = serial.Serial()
        self.serial.timeout = 0.5   #make sure that the alive event can be checked from time to time
        self.settings = TerminalSetup() #placeholder for the settings
        self.thread = None
        self.alive = threading.Event()               
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.text_ctrl_output = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)


        # Menu Bar
        self.frame_terminal_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_terminal_menubar)
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(ID_CLEAR, "&Clear", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(ID_SAVEAS, "&Save Text As...", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(ID_SETTINGS, "&Settings...", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(ID_EXIT, "&Exit", "", wx.ITEM_NORMAL)
        self.frame_terminal_menubar.Append(wxglade_tmp_menu, "&File")

        #Bot mgmt panels & buttons
        self.panels = {}

        self.nbtop_left = wx.Notebook(self, wx.ID_ANY, style=0)
        self.nbbottom_left = wx.Notebook(self, wx.ID_ANY, style=0)
        self.nbtop_right = wx.Notebook(self, wx.ID_ANY, style=0)
        self.nbbottom_right = wx.Notebook(self, wx.ID_ANY, style=0)

        for name, obj in inspect.getmembers(Panels):
            if inspect.isclass(obj) and "Panel" in name:
                #print name
                self.panels[name] = obj(self.nbtop_left, bot=self.bot)
                self.nbtop_left.AddPage(self.panels[name], name)


        self.button_6 = wx.Button(self, wx.ID_ANY, ("reset all servos"))
        self.button_7 = wx.Button(self, wx.ID_ANY, ("Start robot"))

        #clean log buttons
        self.button_clear_1 = wx.Button(self, wx.ID_ANY, ("clear log"), style= wx.BU_EXACTFIT)


        self.__set_properties()
        self.__do_layout()
        self.__attach_events()          #register events



        self.onSettings(None)       #call setup dialog on startup, opens port
        if not self.alive.isSet():
            self.Close()





    def StartThread(self):
        """Start the receiver thread"""        
        self.thread = threading.Thread(target=self.ComPortThread)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def StopThread(self):
        """Stop the receiver thread, wait util it's finished."""
        if self.thread is not None:
            self.alive.clear()          #clear alive event for thread
            self.thread.join()          #wait until thread has finished
            self.thread = None
        
    def __set_properties(self):
        self.SetTitle("Robot Terminal")
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetSize((1000, 800))

        

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_left = wx.BoxSizer(wx.VERTICAL)
        sizer_right = wx.BoxSizer(wx.VERTICAL)

        sizer_left.Add(self.nbtop_left, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        sizer_left.Add(self.nbbottom_left, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        sizer_left.Add(self.button_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_left.Add(self.button_7, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_right.Add(self.nbtop_right, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        sizer_right.Add(self.nbbottom_right, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)

        sizer_1.Add(sizer_left, 1, wx.ALL | wx.EXPAND, 0)
        sizer_1.Add(sizer_right, 1, wx.ALL | wx.EXPAND, 0)

        sizer_right.Add(self.text_ctrl_output, 1, wx.EXPAND, 0)
        sizer_right.Add(self.button_clear_1, 1,  wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)

        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        self.Layout()




    def __attach_events(self):
        #register events at the controls
        self.Bind(wx.EVT_MENU, self.OnClear, id = ID_CLEAR)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id = ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnExit, id = ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onSettings, id = ID_SETTINGS)
        self.text_ctrl_output.Bind(wx.EVT_CHAR, self.OnKey)
        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Bind(wx.EVT_BUTTON, self.reset_button_pressed, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.OnStartRobot, self.button_7)

        self.Bind(wx.EVT_BUTTON, self.clean_terminal, self.button_clear_1)


    def OnExit(self, event):
        """Menu point Exit"""
        self.Close()

    def OnClose(self, event):
        """Called on application shutdown."""
        self.StopThread()               #stop reader thread
        self.serial.close()             #cleanup
        self.Destroy()                  #close windows, exit app

    def OnSaveAs(self, event):
        """Save contents of output window."""
        filename = None
        dlg = wx.FileDialog(None, "Save Text As...", ".", "", "Text File|*.txt|All Files|*",  wx.SAVE)
        if dlg.ShowModal() ==  wx.ID_OK:
            filename = dlg.GetPath()
        dlg.Destroy()
        
        if filename is not None:
            f = file(filename, 'w')
            text = self.text_ctrl_output.GetValue()
            if type(text) == unicode:
                text = text.encode("latin1")    #hm, is that a good asumption?
            f.write(text)
            f.close()
    
    def OnClear(self, event):
        """Clear contents of output window."""
        self.text_ctrl_output.Clear()
    
    def onSettings(self, event=None):
        """Show the portsettings dialog. The reader thread is stopped for the
           settings change."""
        if event is not None:           #will be none when called on startup
            self.StopThread()
            self.serial.close()
        ok = False
        while not ok:
            dialog_serial_cfg = wxConfigDialog.SerialConfigDialog(None, -1, "",
                show=wxConfigDialog.SHOW_BAUDRATE|wxConfigDialog.SHOW_FORMAT|wxConfigDialog.SHOW_FLOW,
                serial=self.serial,
                settings=self.settings,
                bot=self.bot
            )
            result = dialog_serial_cfg.ShowModal()
            dialog_serial_cfg.Destroy()
            #open port if not called on startup, open it on startup and OK too
            if result == wx.ID_OK or event is not None:
                try:
                    self.serial.open()
                except serial.SerialException, e:
                    dlg = wx.MessageDialog(None, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)
                    dlg.ShowModal()
                    dlg.Destroy()
                else:
                    self.StartThread()
                    self.SetTitle("Robot Terminal on %s [%s, %s%s%s%s%s]" % (
                        self.serial.portstr,
                        self.serial.baudrate,
                        self.serial.bytesize,
                        self.serial.parity,
                        self.serial.stopbits,
                        self.serial.rtscts and ' RTS/CTS' or '',
                        self.serial.xonxoff and ' Xon/Xoff' or '',
                        )
                    )
                    ok = True
            else:
                #on startup, dialog aborted
                self.alive.clear()
                ok = True

    def OnKey(self, event):
        """Key event handler. if the key is in the ASCII range, write it to the serial port.
           Newline handling and local echo is also done here."""
        code = event.GetKeyCode()
        if code < 256:                          #is it printable?
            if code == 13:                      #is it a newline? (check for CR which is the RETURN key)
                if self.settings.echo:          #do echo if needed
                    self.text_ctrl_output.AppendText('\n')
                if self.settings.newline == NEWLINE_CR:
                    self.serial.write('\r')     #send CR
                elif self.settings.newline == NEWLINE_LF:
                    self.serial.write('\n')     #send LF
                elif self.settings.newline == NEWLINE_CRLF:
                    self.serial.write('\r\n')   #send CR+LF
            else:
                char = chr(code)
                if self.settings.echo:          #do echo if needed
                    self.text_ctrl_output.WriteText(char)
                self.serial.write(char)         #send the charcater
        else:
            print "Extra Key:", code

    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        text = event.data
        if self.settings.unprintable:
            text = ''.join([(c >= ' ') and c or '<%d>' % ord(c)  for c in text])
        self.text_ctrl_output.AppendText(text)

    def ComPortThread(self):
        """Thread that handles the incomming traffic. Does the basic input
           transformation (newlines) and generates an SerialRxEvent"""
        while self.alive.isSet():               #loop while alive event is true
            text = self.serial.read(1)          #read one, with timout
            if text:                            #check if not timeout
                n = self.serial.inWaiting()     #look if there is more to read
                if n:
                    text = text + self.serial.read(n) #get it
                #newline transformation
                if self.settings.newline == NEWLINE_CR:
                    text = text.replace('\r', '\n')
                elif self.settings.newline == NEWLINE_LF:
                    pass
                elif self.settings.newline == NEWLINE_CRLF:
                    text = text.replace('\r\n', '\n')
                event = SerialRxEvent(self.GetId(), text)
                self.GetEventHandler().AddPendingEvent(event)
                #~ self.OnSerialRead(text)         #output text in window

    def OnStartRobot(self, event):
        self.bot.initBot()

    def reset_button_pressed(self, event):
                    self.bot.initBot()



    def clean_terminal(self, event):
            self.text_ctrl_output.Clear()
            pass


    def Sender(self, message, bc):
                print "Sending message:%s" % message
                if self.settings.echo:          #do echo if needed
                    self.text_ctrl_output.WriteText(message + '\n')
                self.serial.write(message)         #send the charcater
                
                #Update GUI with new bot state
                for obj in self.panels.itervalues():
                    obj.update(botcommand = bc)

            
# end of class TerminalFrame





class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_terminal = TerminalFrame(None, -1, "")
        self.SetTopWindow(frame_terminal)
        frame_terminal.Show(1)
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
