#coding: utf-8

from __future__ import division

import wx
from problem import Problem

class MessageBox(wx.Frame):
    def __init__(self, parent, message, id=wx.ID_ANY):
        super(MessageBox, self).__init__(parent, id, title='hoggg', size=[200, 200])

        panel = wx.Panel(self)
        button = wx.Button(panel, label='OK', pos=[100, 50], size=[50, 50])
        text = wx.StaticText(panel, wx.ID_ANY, message, pos=[100, 10], size=[30, 30])
        self.Bind(wx.EVT_BUTTON, self.close, button)
    def close(self, event):
        self.Destroy()

class CalFrame(wx.Frame):
    def __init__(self, parent, seq, operator, id=wx.ID_ANY):
        super(CalFrame, self).__init__(parent, id, title='hogege', size=[500, 500])

        panel = wx.Panel(self)
        self.correct = 0
        self.operator = operator
        self.seq = seq
        self.gen = self.seq_y()
        self.triple = self.gen.next()
        self.question = wx.StaticText(panel,
                wx.ID_ANY,
                self.q_text(self.triple),
                pos=[200, 50],
                size=[100, 100])

        self.input = wx.TextCtrl(panel, wx.ID_ANY, pos=[200, 300], size=[100, 100])
        self.button = wx.Button(panel, label='入力', pos=[200, 400], size=[100, 100])

        self.Bind(wx.EVT_BUTTON, self.input_answer, self.button)

    def input_answer(self, event):
        if isinstance(self.triple, str):
            self.Destroy()

        inval = self.input.GetValue()
        if int(inval) == self.triple[2]:
            self.correct += 1
            message = '正解!'
        else:
            message = '不正解! 正解は{}だよ'.format(self.triple[2])

        mes = MessageBox(parent=self, message=message)
        mes.Show()
        self.triple = self.gen.next()
        self.question.SetLabel(self.q_text(self.triple))

    def seq_y(self):
        for f in self.seq:
            yield f
        yield 'finish'

    def q_text(self, triple):
        if isinstance(triple, str):
            return self.result()
        return "{}{}{}".format(triple[0], self.operator, triple[1])

    def result(self):
        return "正解率: {}%".format(100*self.correct/len(self.seq))

class MainFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY):
        super(MainFrame, self).__init__(parent, id, title='hoge', size=[500, 500])

        panel = wx.Panel(self)
        add = wx.Button(panel, label='足し算', pos=[250, 30], size=[100, 100])
        #mul = wx.Button(panel, label='掛け算', pos=[250, 150], size=[100, 100])
        #sub = wx.Button(panel, label='ひき算', pos=[250, 270], size=[100, 100])

        self.Bind(wx.EVT_BUTTON, self.start_add, add)
        #self.Bind(wx.EVT_BUTTON, self.start_mul, mul)
        #self.Bind(wx.EVT_BUTTON, self.start_sub, sub)

    def start_add(self, event):
        p = Problem(20, (2, 2), 'add')
        cal_farme = CalFrame(parent=self, seq=p.sequence, operator=p.voice)
        cal_farme.Show()





if __name__ == '__main__':
    app = wx.App()

    frame = MainFrame(None)
    frame.Show()

    app.MainLoop()
