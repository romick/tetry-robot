__author__ = 'roman_000'

import wx
import serial
import threading
import wxConfigDialog


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

    def __init__(self, window_id, data):
        wx.PyCommandEvent.__init__(self, self.eventType, window_id)
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)


#----------------------------------------------------------------------


class TerminalSetup:
    """Placeholder for various terminal settings. Used to pass the
       options to the TerminalSettingsDialog."""

    def __init__(self):
        self.echo = False
        self.unprintable = False
        self.newline = NEWLINE_CRLF


ID_CLEAR = wx.NewId()
ID_SAVEAS = wx.NewId()
ID_SETTINGS = wx.NewId()
ID_TERM = wx.NewId()
ID_BOT = wx.NewId()

NEWLINE_CR = 0
NEWLINE_LF = 1
NEWLINE_CRLF = 2
NEWLINE = '\n'


class SerialPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
        self.menu = kwds['menubar']
        self.window = kwds['window']

        self.serial = serial.Serial()
        self.serial.timeout = 0.5  # make sure that the alive event can be checked from time to time
        self.settings = TerminalSetup()  # placeholder for the settings
        self.thread = None
        self.alive = threading.Event()

        self.text_ctrl_output = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.button_clear_1 = wx.Button(self, wx.ID_ANY, "clear log", style=wx.BU_EXACTFIT)
        self.button_clear_1.SetSize((20, 50))

        #do layout
        sizer_right = wx.BoxSizer(wx.VERTICAL)
        sizer_right.Add(self.text_ctrl_output, 10, wx.EXPAND, 0)
        sizer_right.Add(self.button_clear_1, 1, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        self.SetSizer(sizer_right)

        #Add menu
        panels_menu = wx.Menu()
        panels_menu.Append(ID_CLEAR, "&Clear", "", wx.ITEM_NORMAL)
        panels_menu.Append(ID_SAVEAS, "&Save Text As...", "", wx.ITEM_NORMAL)
        panels_menu.AppendSeparator()
        panels_menu.Append(ID_SETTINGS, "&Settings...", "", wx.ITEM_NORMAL)
        self.menu.Append(panels_menu, "&Serial")

        #Add events
        self.text_ctrl_output.Bind(wx.EVT_CHAR, self.on_key)
        self.Bind(EVT_SERIALRX, self.on_serial_read)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_BUTTON, self.clean_terminal, self.button_clear_1)
        #TODO: fix menus
        self.Bind(wx.EVT_MENU, self.on_clear, id=ID_CLEAR)
        self.window.Bind(wx.EVT_MENU, self.on_save_as, id=ID_SAVEAS)
        self.window.Bind(wx.EVT_MENU, self.on_settings, id=ID_SETTINGS)

    def start_thread(self):
        """Start the receiver thread"""
        self.thread = threading.Thread(target=self.com_port_thread)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def stop_thread(self):
        """Stop the receiver thread, wait util it's finished."""
        if self.thread is not None:
            self.alive.clear()  # clear alive event for thread
            self.thread.join()  # wait until thread has finished
            self.thread = None

    def update(self, **kwds):
        message = kwds['message']
        print "Sending message:%s" % message
        if self.settings.echo:  # do echo if needed
            self.text_ctrl_output.WriteText(message + '\n')
        self.serial.write(message)  # send the character
        pass

    def on_start(self):
        self.on_settings(None)  # call setup dialog on startup, opens port
        if not self.alive.isSet():
            self.Close()

    def on_settings(self, event=None):
        """Show the port_settings dialog. The reader thread is stopped for the
           settings change."""
        if event is not None:  # will be none when called on startup
            self.stop_thread()
            self.serial.close()
        ok = False
        while not ok:
            dialog_serial_cfg = \
                wxConfigDialog.SerialConfigDialog(None, -1, "",
                                                  show=wxConfigDialog.SHOW_BAUDRATE |
                                                       wxConfigDialog.SHOW_FORMAT |
                                                       wxConfigDialog.SHOW_FLOW,
                                                  serial=self.serial,
                                                  settings=self.settings,
                                                  bot=self.bot)
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
                    self.start_thread()
                    ok = True
            else:
                #on startup, dialog aborted
                self.alive.clear()
                ok = True

    def on_close(self, event=None):
        """Called on application shutdown."""
        self.stop_thread()  # stop reader thread
        self.serial.close()  # cleanup
        self.Destroy()  # close windows, exit app

    def on_clear(self, event):
        """Clear contents of output window."""
        print "Clear!!!"
        self.text_ctrl_output.Clear()

    def on_save_as(self, event):
        """Save contents of output window."""
        filename = None
        dlg = wx.FileDialog(None, "Save Text As...", ".", "", "Text File|*.txt|All Files|*", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
        dlg.Destroy()

        if filename is not None:
            f = file(filename, 'w')
            text = self.text_ctrl_output.GetValue()
            if type(text) == unicode:
                text = text.encode("latin1")  # hm, is that a good assumption?
            f.write(text)
            f.close()

    def on_key(self, event):
        """Key event handler. if the key is in the ASCII range, write it to the serial port.
           Newline handling and local echo is also done here."""
        code = event.GetKeyCode()
        if code < 256:  # is it printable?
            if code == 13:  # is it a newline? (check for CR which is the RETURN key)
                if self.settings.echo:  # do echo if needed
                    self.text_ctrl_output.AppendText('\n')
                if self.settings.newline == NEWLINE_CR:
                    self.serial.write('\r')  # send CR
                elif self.settings.newline == NEWLINE_LF:
                    self.serial.write('\n')  # send LF
                elif self.settings.newline == NEWLINE_CRLF:
                    self.serial.write('\r\n')  # send CR+LF
            else:
                char = chr(code)
                if self.settings.echo:  # do echo if needed
                    self.text_ctrl_output.WriteText(char)
                self.serial.write(char)  # send the character
        else:
            print "Extra Key:", code

    def on_serial_read(self, event):
        """Handle input from the serial port."""
        text = event.data
        if self.settings.unprintable:
            text = ''.join([(c >= ' ') and c or '<%d>' % ord(c) for c in text])
        self.text_ctrl_output.AppendText(text)

    def com_port_thread(self):
        """Thread that handles the incoming traffic. Does the basic input
           transformation (newlines) and generates an SerialRxEvent"""
        while self.alive.isSet():  # loop while alive event is true
            text = self.serial.read(1)  # read one, with timeout
            if text:  # check if not timeout
                n = self.serial.inWaiting()  # look if there is more to read
                if n:
                    text = text + self.serial.read(n)  # get it
                #newline transformation
                if self.settings.newline == NEWLINE_CR:
                    text = text.replace('\r', '\n')
                elif self.settings.newline == NEWLINE_LF:
                    pass
                elif self.settings.newline == NEWLINE_CRLF:
                    text = text.replace('\r\n', '\n')
                event = SerialRxEvent(self.GetId(), text)
                self.GetEventHandler().AddPendingEvent(event)
                #~ self.on_serial_read(text)         #output text in window

    def clean_terminal(self, event):
        self.text_ctrl_output.Clear()
        pass
