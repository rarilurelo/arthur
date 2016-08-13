#coding: utf-8

from __future__ import division

import wx
from problem import Problem

class MessageBox(wx.Frame):
    def __init__(self, parent, message, id=wx.ID_ANY):
        super(MessageBox, self).__init__(parent, id, title='正答', size=[500, 500])

        panel = wx.Panel(self)
        button = wx.Button(panel, label='OK', pos=[200, 400], size=[100, 100])
        text = wx.StaticText(panel, wx.ID_ANY, message, pos=[200, 150], size=[100, 100])
        self.font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        button.SetFont(self.font)
        text.SetFont(self.font)

        self.Bind(wx.EVT_BUTTON, self.close, button)


    def close(self, event):
        self.Destroy()

class CalFrame(wx.Frame):
    def __init__(self, parent, seq, operator, id=wx.ID_ANY):
        super(CalFrame, self).__init__(parent, id, title='問題', size=[500, 500])

        panel = wx.Panel(self)
        self.correct = 0
        self.operator = operator
        self.seq = seq
        self.gen = self.seq_y()
        self.triple = self.gen.next()
        self.font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.question = wx.StaticText(panel,
                wx.ID_ANY,
                self.q_text(self.triple),
                pos=[200, 150],
                size=[100, 100])
        self.question.SetFont(self.font)

        self.input = wx.TextCtrl(panel, wx.ID_ANY, pos=[200, 300], size=[100, 100])
        self.button = wx.Button(panel, label='入力', pos=[200, 400], size=[100, 100])

        self.input.SetFont(self.font)
        self.button.SetFont(self.font)

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
        self.input.SelectAll()

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
        super(MainFrame, self).__init__(parent, id, title='計算', size=[500, 500])

        panel = wx.Panel(self)
        add = wx.Button(panel, label='足し算', pos=[200, 50], size=[100, 100])
        mul = wx.Button(panel, label='掛け算', pos=[200, 250], size=[100, 100])
        #sub = wx.Button(panel, label='ひき算', pos=[250, 270], size=[100, 100])
        self.font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        add.SetFont(self.font)
        mul.SetFont(self.font)

        self.Bind(wx.EVT_BUTTON, self.start_add, add)
        self.Bind(wx.EVT_BUTTON, self.start_mul, mul)
        #self.Bind(wx.EVT_BUTTON, self.start_sub, sub)

    def start_add(self, event):
        p = Problem(20, (2, 2), 'add')
        cal_farme = CalFrame(parent=self, seq=p.sequence, operator=p.voice)
        cal_farme.Show()

    def start_mul(self, event):
        p = Problem(20, (2, 1), 'mul')
        cal_farme = CalFrame(parent=self, seq=p.sequence, operator=p.voice)
        cal_farme.Show()





if __name__ == '__main__':
    app = wx.App()

    frame = MainFrame(None)
    frame.Show()

    app.MainLoop()
