#!/usr/bin/env python
# generated by wxGlade 0.3.1 on Thu Oct 02 23:25:44 2003

import wx
import serial
import os
import re

SHOW_BAUDRATE = 1 << 0
SHOW_FORMAT = 1 << 1
SHOW_FLOW = 1 << 2
SHOW_TIMEOUT = 1 << 3
SHOW_ALL = SHOW_BAUDRATE | SHOW_FORMAT | SHOW_FLOW | SHOW_TIMEOUT

try:
    enumerate
except NameError:
    def enumerate(sequence):
        return zip(range(len(sequence)), sequence)


class SerialConfigDialog(wx.Dialog):
    """Serial Port confiuration dialog, to be used with pyserial 2.0+
       When instantiating a class of this dialog, then the "serial" keyword
       argument is mandatory. It is a reference to a serial.Serial instance.
       the optional "show" keyword argument can be used to show/hide different
       settings. The default is SHOW_ALL which coresponds to 
       SHOW_BAUDRATE|SHOW_FORMAT|SHOW_FLOW|SHOW_TIMEOUT. All constants can be
       found in ths module (not the class)."""

    def __init__(self, *args, **kwds):
        #grab the serial keyword and remove it from the dict
        self.serial = kwds['serial']
        del kwds['serial']

        self.show = SHOW_ALL
        if 'show' in kwds:
            self.show = kwds['show']
            del kwds['show']

        self.settings = kwds['settings']
        del kwds['settings']

        self.bot = kwds['bot']
        #self.creator = kwds['creator']
        #print 1
        del kwds['bot']

        # begin wxGlade: SerialConfigDialog.__init__
        # end wxGlade
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)

        self.sizer_main = wx.BoxSizer(wx.VERTICAL)
        #For some strange reason MacOSX require it to be defined before controls, which would added to it.
        #Otherwise they are simply disabled.
        self.sizer_basics = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Basics"), wx.VERTICAL)
        self.sizer_4 = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Input/Output"), wx.VERTICAL)
        self.sizer_nb = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Legs"), wx.VERTICAL)
        self.sizer_timeout = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Timeout"), wx.HORIZONTAL)
        self.sizer_flow = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Flow Control"), wx.HORIZONTAL)
        self.sizer_format = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Data Format"), wx.VERTICAL)
        self.sizer_9 = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Bot"), wx.VERTICAL)

        self.label_2 = wx.StaticText(self, -1, "Port")
        self.combo_box_port = wx.ComboBox(self, -1, choices=["dummy1",
                                                             "dummy2",
                                                             "dummy3",
                                                             "dummy4",
                                                             "dummy5"],
                                          style=wx.CB_DROPDOWN)
        if self.show & SHOW_BAUDRATE:
            self.label_1 = wx.StaticText(self, -1, "Baudrate")
            self.choice_baudrate = wx.Choice(self, -1, choices=["choice 1"])
        if self.show & SHOW_FORMAT:
            self.label_3 = wx.StaticText(self, -1, "Data Bits")
            self.choice_databits = wx.Choice(self, -1, choices=["choice 1"])
            self.label_4 = wx.StaticText(self, -1, "Stop Bits")
            self.choice_stopbits = wx.Choice(self, -1, choices=["choice 1"])
            self.label_5 = wx.StaticText(self, -1, "Parity")
            self.choice_parity = wx.Choice(self, -1, choices=["choice 1"])
        if self.show & SHOW_TIMEOUT:
            self.checkbox_timeout = wx.CheckBox(self, -1, "Use Timeout")
            self.text_ctrl_timeout = wx.TextCtrl(self, -1, "")
            self.label_6 = wx.StaticText(self, -1, "seconds")
        if self.show & SHOW_FLOW:
            self.checkbox_rtscts = wx.CheckBox(self, -1, "RTS/CTS")
            self.checkbox_xonxoff = wx.CheckBox(self, -1, "Xon/Xoff")
        self.button_ok = wx.Button(self, -1, "OK")
        self.button_cancel = wx.Button(self, -1, "Cancel")

        #Terminal settings
        self.checkbox_echo = wx.CheckBox(self, -1, "Local Echo")
        self.checkbox_unprintable = wx.CheckBox(self, -1, "Show unprintable characters")
        self.radio_box_newline = wx.RadioBox(self, -1, "Newline Handling", choices=["CR only", "LF only", "CR+LF"],
                                             majorDimension=0, style=wx.RA_SPECIFY_ROWS)

        #set Bot settings
        self.radio_box_protocol = wx.RadioBox(self, -1, "Protocol", choices=self.bot.protocols, majorDimension=0,
                                              style=wx.RA_SPECIFY_ROWS)
        self.nb = wx.Notebook(self, wx.ID_ANY, style=0)
        self.leg_pages = []

        #TODO: read initial settings from file
        self.robots = []
        for file_name in os.listdir('Robots'):
            if os.path.splitext(file_name)[1] == '.json':
                file_name = os.path.splitext(file_name)[0]
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', file_name)
                self.robots.append(s1)
        self.choice_robots = wx.Choice(self, -1, choices=self.robots)

        self.__set_properties()
        self.__do_layout()
        #fill in ports and select current setting
        index = 0
        self.combo_box_port.Clear()
        for n in range(4):
            portname = serial.device(n)
            self.combo_box_port.Append(portname)
            if self.serial.portstr == portname:
                index = n
        if self.serial.portstr is not None:
            self.combo_box_port.SetValue(str(self.serial.portstr))
        else:
            #self.combo_box_port.SetSelection(index)
            self.combo_box_port.SetSelection(2)
        if self.show & SHOW_BAUDRATE:
            #fill in badrates and select current setting
            self.choice_baudrate.Clear()
            for n, baudrate in enumerate(self.serial.BAUDRATES):
                self.choice_baudrate.Append(str(baudrate))
                if self.serial.baudrate == baudrate:
                    index = n
                    #self.choice_baudrate.SetSelection(index)
            self.choice_baudrate.SetSelection(len(self.serial.BAUDRATES) - 1)
        if self.show & SHOW_FORMAT:
            #fill in databits and select current setting
            self.choice_databits.Clear()
            for n, bytesize in enumerate(self.serial.BYTESIZES):
                self.choice_databits.Append(str(bytesize))
                if self.serial.bytesize == bytesize:
                    index = n
            self.choice_databits.SetSelection(index)
            #fill in stopbits and select current setting
            self.choice_stopbits.Clear()
            for n, stopbits in enumerate(self.serial.STOPBITS):
                self.choice_stopbits.Append(str(stopbits))
                if self.serial.stopbits == stopbits:
                    index = n
            self.choice_stopbits.SetSelection(index)
            #fill in parities and select current setting
            self.choice_parity.Clear()
            for n, parity in enumerate(self.serial.PARITIES):
                self.choice_parity.Append(str(serial.PARITY_NAMES[parity]))
                if self.serial.parity == parity:
                    index = n
            self.choice_parity.SetSelection(index)
        if self.show & SHOW_TIMEOUT:
            #set the timeout mode and value
            if self.serial.timeout is None:
                self.checkbox_timeout.SetValue(False)
                self.text_ctrl_timeout.Enable(False)
            else:
                self.checkbox_timeout.SetValue(True)
                self.text_ctrl_timeout.Enable(True)
                self.text_ctrl_timeout.SetValue(str(self.serial.timeout))
        if self.show & SHOW_FLOW:
            #set the rtscts mode
            self.checkbox_rtscts.SetValue(self.serial.rtscts)
            #set the rtscts mode
            self.checkbox_xonxoff.SetValue(self.serial.xonxoff)

        #Terminal settings
        self.checkbox_echo.SetValue(self.settings.echo)
        self.checkbox_unprintable.SetValue(self.settings.unprintable)
        self.radio_box_newline.SetSelection(self.settings.newline)

        #Bot settings
        self.radio_box_protocol.SetSelection(self.bot.protocols.index(self.bot.current_protocol))

        #attach the event handlers
        self.__attach_events()

        self.choice_robots.SetSelection(0)

    def __set_properties(self):
        # begin wxGlade: SerialConfigDialog.__set_properties
        # end wxGlade
        self.SetTitle("Robot Terminal Configuration")
        if self.show & SHOW_TIMEOUT:
            self.text_ctrl_timeout.Enable(0)
        self.button_ok.SetDefault()
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.radio_box_newline.SetSelection(0)

    def __do_layout(self):
        # begin wxGlade: SerialConfigDialog.__do_layout
        # end wxGlade

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.label_2, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_5.Add(self.combo_box_port, 1, 0, 0)
        self.sizer_basics.Add(sizer_5, 0, wx.RIGHT | wx.EXPAND, 0)
        if self.show & SHOW_BAUDRATE:
            sizer_baudrate = wx.BoxSizer(wx.HORIZONTAL)
            sizer_baudrate.Add(self.label_1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_baudrate.Add(self.choice_baudrate, 1, wx.ALIGN_RIGHT, 0)
            self.sizer_basics.Add(sizer_baudrate, 0, wx.EXPAND, 0)
        sizer_2.Add(self.sizer_basics, 0, wx.EXPAND, 0)
        if self.show & SHOW_FORMAT:
            sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_6.Add(self.label_3, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_6.Add(self.choice_databits, 1, wx.ALIGN_RIGHT, 0)
            self.sizer_format.Add(sizer_6, 0, wx.EXPAND, 0)
            sizer_7.Add(self.label_4, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_7.Add(self.choice_stopbits, 1, wx.ALIGN_RIGHT, 0)
            self.sizer_format.Add(sizer_7, 0, wx.EXPAND, 0)
            sizer_8.Add(self.label_5, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_8.Add(self.choice_parity, 1, wx.ALIGN_RIGHT, 0)
            self.sizer_format.Add(sizer_8, 0, wx.EXPAND, 0)
            sizer_2.Add(self.sizer_format, 0, wx.EXPAND, 0)
        if self.show & SHOW_TIMEOUT:
            self.sizer_timeout.Add(self.checkbox_timeout, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            self.sizer_timeout.Add(self.text_ctrl_timeout, 0, 0, 0)
            self.sizer_timeout.Add(self.label_6, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_2.Add(self.sizer_timeout, 0, 0, 0)
        if self.show & SHOW_FLOW:
            self.sizer_flow.Add(self.checkbox_rtscts, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            self.sizer_flow.Add(self.checkbox_xonxoff, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            self.sizer_flow.Add((10, 10), 1, wx.EXPAND, 0)
            sizer_2.Add(self.sizer_flow, 0, wx.EXPAND, 0)

        sizer_3.Add(self.button_ok, 0, 0, 0)
        sizer_3.Add(self.button_cancel, 0, 0, 0)
        sizer_1.Add(sizer_2, 0, wx.ALL | wx.ALIGN_RIGHT, 4)

        #Terminal settings layout
        self.sizer_4.Add(self.checkbox_echo, 0, wx.ALL, 4)
        self.sizer_4.Add(self.checkbox_unprintable, 0, wx.ALL, 4)
        self.sizer_4.Add(self.radio_box_newline, 0, 0, 0)
        sizer_1.Add(self.sizer_4, 0, wx.ALL | wx.EXPAND, 4)

        #Bot setting layout
        self.sizer_9.Add(self.radio_box_protocol, 0, 0, 0)
        sizer_1.Add(self.sizer_9, 0, wx.ALL | wx.EXPAND, 4)

        self.sizer_nb.Add(self.choice_robots, 0, wx.ALL | wx.EXPAND, 4)
        self.sizer_nb.Add(self.nb, 0, wx.ALL | wx.EXPAND, 4)
        #self.panel.SetAutoLayout(1)
        #self.panel.SetSizer(self.sizer_nb)
        #self.panel.Layout()

        self.sizer_main.Add(sizer_1, 0, wx.ALL, 4)
        self.sizer_main.Add(self.sizer_nb, 0, wx.ALL | wx.EXPAND, 4)
        self.sizer_main.Add(sizer_3, 0, wx.ALL | wx.ALIGN_RIGHT, 4)

        self.SetAutoLayout(1)
        self.SetSizer(self.sizer_main)
        self.sizer_main.Fit(self)
        self.sizer_main.SetSizeHints(self)
        self.Layout()

        self.choice_robots.SetSelection(0)
        self.on_robot_choice()

    def __attach_events(self):
        wx.EVT_BUTTON(self, self.button_ok.GetId(), self.on_ok)
        wx.EVT_BUTTON(self, self.button_cancel.GetId(), self.on_cancel)
        wx.EVT_CHOICE(self, self.choice_robots.GetId(), self.on_robot_choice)
        if self.show & SHOW_TIMEOUT:
            wx.EVT_CHECKBOX(self, self.checkbox_timeout.GetId(), self.on_timeout)

    def on_ok(self, events):
        success = True
        self.serial.port = str(self.combo_box_port.GetValue())
        if self.show & SHOW_BAUDRATE:
            self.serial.baudrate = self.serial.BAUDRATES[self.choice_baudrate.GetSelection()]
        if self.show & SHOW_FORMAT:
            self.serial.bytesize = self.serial.BYTESIZES[self.choice_databits.GetSelection()]
            self.serial.stopbits = self.serial.STOPBITS[self.choice_stopbits.GetSelection()]
            self.serial.parity = self.serial.PARITIES[self.choice_parity.GetSelection()]
        if self.show & SHOW_FLOW:
            self.serial.rtscts = self.checkbox_rtscts.GetValue()
            self.serial.xonxoff = self.checkbox_xonxoff.GetValue()
        if self.show & SHOW_TIMEOUT:
            if self.checkbox_timeout.GetValue():
                try:
                    self.serial.timeout = float(self.text_ctrl_timeout.GetValue())
                except ValueError:
                    dlg = wx.MessageDialog(self, 'Timeout must be a numeric value',
                                           'Value Error', wx.OK | wx.ICON_ERROR)
                    dlg.ShowModal()
                    dlg.Destroy()
                    success = False
            else:
                self.serial.timeout = None

        #Save terminal settings
        self.settings.echo = self.checkbox_echo.GetValue()
        self.settings.unprintable = self.checkbox_unprintable.GetValue()
        self.settings.newline = self.radio_box_newline.GetSelection()

        #save bot settings
        self.bot.protocol = self.bot.protocols[self.radio_box_protocol.GetSelection()]
        for lp in self.leg_pages:
            lp.leg.name = lp.text_ctrl_16.GetValue()
            lp.leg.leg_offset[0] = int(lp.text_ctrl_8.GetValue())
            lp.leg.leg_offset[1] = int(lp.text_ctrl_9.GetValue())
            lp.leg.coxa_length = int(lp.text_ctrl_10.GetValue())
            lp.leg.temur_length = int(lp.text_ctrl_11.GetValue())
            lp.leg.coxa_length = int(lp.text_ctrl_12.GetValue())
            lp.leg.servos = [int(lp.text_ctrl_13.GetValue()),
                             int(lp.text_ctrl_14.GetValue()),
                             int(lp.text_ctrl_15.GetValue())]
            lp.leg.debug = lp.checkbox_1.GetValue()

        self.bot.dump_settings()

        if success:
            self.EndModal(wx.ID_OK)

    def on_cancel(self, events):
        self.EndModal(wx.ID_CANCEL)

    def on_robot_choice(self, events=None):
        sel = self.choice_robots.GetCurrentSelection()
        self.bot.load_settings('./Robots/' + self.robots[sel] + '.json')

        self.nb.DeleteAllPages()
        self.leg_pages = []
        for l in self.bot.legs:
            cp = LegPanel(self.nb, leg=l)
            self.leg_pages.append(cp)
            self.nb.AddPage(cp, l.name)
        self.Layout()
        self.sizer_main.Fit(self)

    def on_timeout(self, events):
        if self.checkbox_timeout.GetValue():
            self.text_ctrl_timeout.Enable(True)
        else:
            self.text_ctrl_timeout.Enable(False)


# end of class SerialConfigDialog


class LegPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.leg = kwds['leg']

        self.label_13 = wx.StaticText(self, wx.ID_ANY, "Name:")
        self.text_ctrl_16 = wx.TextCtrl(self, wx.ID_ANY, str(self.leg.name))
        self.label_5 = wx.StaticText(self, wx.ID_ANY, "Offset X:")
        self.text_ctrl_8 = wx.TextCtrl(self, wx.ID_ANY, str(self.leg.leg_offset[0]))
        self.label_6 = wx.StaticText(self, wx.ID_ANY, "Offset Y:")
        self.text_ctrl_9 = wx.TextCtrl(self, wx.ID_ANY, str(self.leg.leg_offset[1]))
        self.label_7 = wx.StaticText(self, wx.ID_ANY, "Coxa length:")
        self.text_ctrl_10 = wx.TextCtrl(self, wx.ID_ANY, str(self.leg.coxa_length))
        self.label_10 = wx.StaticText(self, wx.ID_ANY, "Coxa servo:")
        self.text_ctrl_13 = wx.TextCtrl(self, wx.ID_ANY, str(self.leg.servos[0]))
        self.label_8 = wx.StaticText(self, wx.ID_ANY, "Temur length:")
        self.text_ctrl_11 = wx.TextCtrl(self, wx.ID_ANY, str(self.leg.temur_length))
        self.label_11 = wx.StaticText(self, wx.ID_ANY, "Temur servo:")
        self.text_ctrl_14 = wx.TextCtrl(self, wx.ID_ANY, str(self.leg.servos[1]))
        self.label_9 = wx.StaticText(self, wx.ID_ANY, "Tibia length:")
        self.text_ctrl_12 = wx.TextCtrl(self, wx.ID_ANY, str(self.leg.tibia_length))
        self.label_12 = wx.StaticText(self, wx.ID_ANY, "Tibia servo:")
        self.text_ctrl_15 = wx.TextCtrl(self, wx.ID_ANY, str(self.leg.servos[2]))
        self.label_14 = wx.StaticText(self, wx.ID_ANY, "Verbose?:")
        self.checkbox_1 = wx.CheckBox(self, wx.ID_ANY, "")
        self.checkbox_1.SetValue(self.leg.debug)

        grid_sizer_1 = wx.FlexGridSizer(8, 4, 1, 1)
        grid_sizer_1.Add(self.label_13, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.text_ctrl_16, 0, wx.ALL, 4)
        grid_sizer_1.Add((1, 1), 0, wx.ALL, 4)
        grid_sizer_1.Add((1, 1), 0, wx.ALL, 4)
        grid_sizer_1.Add(self.label_5, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.text_ctrl_8, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.label_6, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.text_ctrl_9, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.label_7, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.text_ctrl_10, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.label_10, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.text_ctrl_13, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.label_8, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.text_ctrl_11, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.label_11, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.text_ctrl_14, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.label_9, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.text_ctrl_12, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.label_12, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.text_ctrl_15, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.label_14, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.checkbox_1, 0, wx.ALL, 4)

        self.SetSizer(grid_sizer_1)


class MyApp(wx.App):
    """Test code"""

    def OnInit(self):
        wx.InitAllImageHandlers()

        ser = serial.Serial()
        print ser
        #loop until cancel is pressed, old values are used as start for the next run
        #show the different views, one after the other
        #value are kept.
        for flags in (SHOW_BAUDRATE, SHOW_FLOW, SHOW_FORMAT, SHOW_TIMEOUT, SHOW_ALL):
            dialog_serial_cfg = SerialConfigDialog(None, -1, "", serial=ser, show=flags)
            self.SetTopWindow(dialog_serial_cfg)
            result = dialog_serial_cfg.ShowModal()
            print ser
            if result != wx.ID_OK:
                break
        #the user can play around with the values, CANCEL aborts the loop
        while 1:
            dialog_serial_cfg = SerialConfigDialog(None, -1, "", serial=ser)
            self.SetTopWindow(dialog_serial_cfg)
            result = dialog_serial_cfg.ShowModal()
            print ser
            if result != wx.ID_OK:
                break
        return 0

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
