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


# temporary testing class
class TestDataGen(object):
    def __init__(self, init=50):
        self.data = self.init = init

    def next(self):
        self._recalc_data()
        return self.data

    def _recalc_data(self):
        delta = random.uniform(-0.5, 0.5)
        r = random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8:
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta


class ImplementationDialog(wx.Dialog):
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


class Graph():
    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel

        self.datagen = TestDataGen()
        self.data = [self.datagen.next()]
        self.paused = False

        self.redraw_timer = wx.Timer(self.panel)
        self.panel.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(100)

    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((7.5, 5.0), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Very important random data', size=12)

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        self.plot_data = self.axes.plot(self.data, linewidth=1, color=(1, 1, 0),)[0]

        self.canvas = FigCanvas(self.panel, -1, self.fig)

    def draw_plot(self):
        xmax = len(self.data) if len(self.data) > 50 else 50
        xmin = xmax - 50
        ymin = round(min(self.data), 0) - 1
        ymax = round(max(self.data), 0) + 1

        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)

        if self.parent.cb_grid.IsChecked():
            self.axes.grid(True, color='gray')
        else:
            self.axes.grid(False)

        pylab.setp(self.axes.get_xticklabels(), visible=self.parent.cb_xlab.IsChecked())

        self.plot_data.set_xdata(np.arange(len(self.data)))
        self.plot_data.set_ydata(np.array(self.data))

        self.canvas.draw()

    def on_pause_button(self, evt):
        self.paused = not self.paused

    def on_update_pause_button(self, evt):
        label = "Resume" if self.paused else "Pause"
        self.parent.pause_button.SetLabel(label)

    def on_cb_grid(self, evt):
        self.draw_plot()

    def on_cb_xlab(self, evt):
        self.draw_plot()

    def on_redraw_timer(self, evt):
        if not self.paused:
            self.data.append(self.datagen.next())
        self.draw_plot()


class MainFrame(wx.Frame):
    window_title = "Alekseevskii Conjecture"

    def __init__(self, manager):
        self.manager = manager
        wx.Frame.__init__(self, None, -1, title=self.window_title)

        self.sp = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.create_graph_panel()
        self.p2 = wx.Panel(self.sp, style=wx.BORDER_SUNKEN)
        self.p2.SetBackgroundColour("sky blue")
        self.sp.SplitVertically(self.graph_panel, self.p2, -200)

        self.show_startup_dialog()

    def show_startup_dialog(self):
        self.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.on_window_modal_dialog_closed)
        dlg = ImplementationDialog(self, -1, "Implementation Select Dialog", size=(350, 300),
                                   style=wx.DEFAULT_DIALOG_STYLE)
        dlg.ShowWindowModal()

    def on_implementation_choice(self, evt):
        self.manager.set_implementation(evt.GetString())

    def on_window_modal_dialog_closed(self, evt):
        dialog = evt.GetDialog()
        val = evt.GetReturnCode()
        if val == wx.ID_OK:
            self.manager.setup_blocking()
        else:
            exit()
        dialog.Destroy()

    def create_graph_panel(self):
        self.graph_panel = wx.Panel(self.sp, style=wx.BORDER_SUNKEN)
        self.graph = Graph(self, self.graph_panel)
        self.graph.init_plot()

        self.pause_button = wx.Button(self.graph_panel, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.graph.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.graph.on_update_pause_button, self.pause_button)

        self.cb_grid = wx.CheckBox(self.graph_panel, -1, "Show Grid", style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.graph.on_cb_grid, self.cb_grid)
        self.cb_grid.SetValue(True)

        self.cb_xlab = wx.CheckBox(self.graph_panel, -1, "Show X labels", style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.graph.on_cb_xlab, self.cb_xlab)
        self.cb_xlab.SetValue(True)

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.Add(self.pause_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.cb_grid, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_xlab, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.graph.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_CENTER | wx.TOP)

        self.graph_panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def on_exit(self):
        self.graph_panel.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    m = Manager()
    app.frame = MainFrame(m)
    app.frame.Show()
    app.MainLoop()
