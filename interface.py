__author__ = 'Lucas Schuermann'

import wxversion
wxversion.ensureMinimal('2.8')

import os
import random
import wx

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas
import numpy as np
import pylab

from manager import Manager


class StartupDialog(wx.Dialog):
    def __init__(self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)
        self.PostCreate(pre)
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Select an implementation:")
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        self.ch = wx.Choice(self, -1, (100, 50), choices=Manager.implementation_choices)
        self.Bind(wx.EVT_CHOICE, parent.on_implementation_choice, self.ch)

        box.Add(self.ch, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


class MainFrame(wx.Frame):
    def __init__(self, manager):
        self.manager = manager

        self.window_title = "Alekseevskii Conjecture"
        self.window_width = 800
        self.window_height = 600
        wx.Frame.__init__(self, None, title=self.window_title, size=(self.window_width, self.window_height))
        self.sp = wx.SplitterWindow(self)
        self.p1 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        self.p2 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        self.sp.SplitVertically(self.p1, self.p2, self.window_width/2.)

        self.show_startup_dialog()

    def show_startup_dialog(self):
        self.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.on_window_modal_dialog_closed)
        dlg = StartupDialog(self, -1, "Implementation Select Dialog", size=(350, 300), style=wx.DEFAULT_DIALOG_STYLE)
        dlg.ShowWindowModal()

    def on_implementation_choice(self, evt):
        print evt.GetString()

    def on_window_modal_dialog_closed(self, evt):
        dialog = evt.GetDialog()
        val = evt.GetReturnCode()
        if val == wx.ID_OK:
            print "You pressed ok"
        else:
            exit()
        dialog.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    app.frame = MainFrame(Manager())
    app.frame.Show()
    app.MainLoop()
