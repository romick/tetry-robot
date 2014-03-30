__author__ = 'roman_000'

import wx
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# from direct.showbase import DirectObject
from pandac.PandaModules import *
loadPrcFileData("", "window-type none")

from direct.directbase import DirectStart


# class VirtualPanel(wx.Panel):
#     def __init__(self, parent, **kwds):
#         wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
#         self.bot = kwds['bot']
#         self.runner = kwds['runner']
#
#         # fig = plt.figure()
#         # ax = fig.add_subplot(111, projection='3d')

class VirtualPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
        self.runner = kwds['runner']


    def on_start(self):
        assert self.GetHandle() != 0

        wp = WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(self.ClientSize.GetWidth(), self.ClientSize.GetHeight())
        wp.setParentWindow(self.GetHandle())
        base.openDefaultWindow(props=wp, gsg=None)

        wx.EVT_SIZE(self, self.OnResize)
        loader.loadModel('models\environment').reparentTo(render)


    def OnResize(self, event):
        frame_size = event.GetSize()
        wp = WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(frame_size.GetWidth(), frame_size.GetHeight())
        base.win.requestProperties(wp)