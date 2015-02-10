__author__ = 'roman_000'

import wx
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


class VirtualPanel(wx.Panel):
    def __init__(self, parent, **kwds):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.bot = kwds['bot']
        self.runner = kwds['runner']

        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')