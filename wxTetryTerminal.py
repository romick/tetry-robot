#!/usr/bin/env python_32

import wx
import sys
import wxConfigDialog
import serial
import threading
import Tetry
#import legIK
import cPickle

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

class RedirectText:
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string) #supporting class to redirect stdout to textcontrol


class TerminalFrame(wx.Frame):
    """Simple terminal program for wxPython"""
    
    def __init__(self, *args, **kwds):
        self.bot = Tetry.Robot(sender = self.Sender)
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

        #redirect stdout to text_ctrl_log
        self.text_ctrl_log = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        sys.stdout = RedirectText(self.text_ctrl_log)
        
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

        #Bot mgmt buttons
        self.button_3 = wx.Button(self, wx.ID_ANY, ("forward"))
        self.button_2 = wx.Button(self, wx.ID_ANY, ("left"))
        self.button_4 = wx.Button(self, wx.ID_ANY, ("right"))
        self.button_5 = wx.Button(self, wx.ID_ANY, ("backward"))
        self.button_6 = wx.Button(self, wx.ID_ANY, ("reset all servos"))
        self.button_7 = wx.Button(self, wx.ID_ANY, ("Start robot"))

        #clean log buttons
        self.button_clear_1 = wx.Button(self, wx.ID_ANY, ("clear log"), style= wx.BU_EXACTFIT)
        self.button_clear_2 = wx.Button(self, wx.ID_ANY, ("clear log"), style= wx.BU_EXACTFIT)

        self.sliders=[]
        for i in range(self.bot.servo_number):
            self.sliders.append(wx.Slider(self, wx.ID_ANY, 1500, 500, 2500, style=wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_TOP, name="servo%i" % i))


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

        self.button_3.SetMinSize((140, 140))
        self.button_2.SetMinSize((140, 140))
        self.button_4.SetMinSize((140, 140))
        self.button_5.SetMinSize((140, 140))
        
        for i in range(self.bot.servo_number):
            self.sliders[i].SetMinSize((150, -1))


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        grid_sizer_1 = wx.FlexGridSizer(8, 3, 2, 2)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((150, 150), 0, 0, 0)
        grid_sizer_1.Add(self.button_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_5, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((60, 60), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        for i in range(self.bot.servo_number):
            grid_sizer_1.Add(self.sliders[i], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_7, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_2.Add(grid_sizer_1, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        sizer_1.Add(sizer_2, 1, wx.ALL | wx.EXPAND, 0)

        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        self.Layout()

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)



        sizer_3.Add(self.text_ctrl_output, 1, wx.EXPAND, 0)
        sizer_4.Add(self.button_clear_1, 1,  wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        sizer_3.Add(sizer_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 1)

        sizer_3.Add(self.text_ctrl_log, 1, wx.EXPAND, 0)
        sizer_5.Add(self.button_clear_2, 1,  wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        sizer_3.Add(sizer_5, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 1)

        sizer_1.Add(sizer_3, 1,  wx.ALL | wx.EXPAND, 0)


    def __attach_events(self):
        #register events at the controls
        self.Bind(wx.EVT_MENU, self.OnClear, id = ID_CLEAR)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id = ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnExit, id = ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onSettings, id = ID_SETTINGS)
        self.text_ctrl_output.Bind(wx.EVT_CHAR, self.OnKey)
        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Bind(wx.EVT_BUTTON, self.forward_button_pressed, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.left_button_pressed, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.right_button_pressed, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.back_button_pressed, self.button_5)
        self.Bind(wx.EVT_BUTTON, self.reset_button_pressed, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.OnStartRobot, self.button_7)

        self.Bind(wx.EVT_BUTTON, self.clean_terminal, self.button_clear_1)
        self.Bind(wx.EVT_BUTTON, self.clean_log, self.button_clear_2)

        for i in range(self.bot.servo_number):
            self.Bind(wx.EVT_SCROLL_CHANGED , self.servo_move, self.sliders[i])

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

    def forward_button_pressed(self, event):  
                    self.bot.makeStep(0)

    def left_button_pressed(self, event):  
                    self.bot.makeStep(270)

    def right_button_pressed(self, event): 
                    self.bot.makeStep(90)

    def back_button_pressed(self, event):  
                    self.bot.makeStep(180)

    def reset_button_pressed(self, event): 
                self.bot.initBot()

    def servo_move(self, event):  
                command = []
                for s in range(self.bot.servo_number):
                    command.append(dict(servo=s, position=self.sliders[s].GetValue()))
                self.bot._send(command)


    def clean_terminal(self, event):
            self.text_ctrl_output.Clear()
            pass

    def clean_log(self, event):
            self.text_ctrl_log.Clear()
            pass
    
    def Sender(self, message):
                print "Sending message:%s" % message
                if self.settings.echo:          #do echo if needed
                    self.text_ctrl_output.WriteText(message + '\n')
                self.serial.write(message)         #send the charcater

            
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
