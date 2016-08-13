# coding: utf-8

from __future__ import division
from __future__ import print_function
import argparse
import numpy as np
import subprocess
import time
import sys
#import matplotlib.pyplot as plt


class Problem(object):
    def __init__(self, num, shape, operator, mute=True):
        self.num      = num
        self.caled    = shape[0]
        self.calee    = shape[1]
        self.operator = eval("int.__{}__".format(operator))
        self.mute     = mute
        if operator == "add":
            self.voice = "たす"
        elif operator == "mul":
            self.voice = "かける"
        elif operator == "sub":
            self.voice = "ひく"
        self.sequence = self.triplet()

    def question(self, first, secound):
        if self.mute:
            sys.stdout.write("\r{} {} {}".format(first, self.voice, secound))
            sys.stdout.flush()
            time.sleep(1.5)
            sys.stdout.write("\r答えは?{} ".format((self.calee+self.caled)*' '))
            sys.stdout.flush()
        else:
            subprocess.call("echo '{} {} {}' | say".format(first, self.voice, secound), shell=True)

    def __random_digit(self, length):
        return np.random.randint(pow(10, length-1), pow(10, length))

    def triplet(self):
        sequence = []
        for _  in range(self.num):
            first   = self.__random_digit(self.caled)
            secound = self.__random_digit(self.calee)
            triplet = (first, secound, self.operator(first, secound))
            sequence.append(triplet)
        return sequence

    def __call__(self):
        s = time.time()
        correct = 0
        for first, secound, answer in self.sequence():
            self.question(first, secound)
            inference = sys.stdin.readline().strip()
            while 'onemore' == inference or not inference.isdigit():
                if 'onemore' == inference:
                    self.question(first, secound)
                elif not inference.isdigit():
                    print("打ち間違い. もっかい!")
                inference = sys.stdin.readline().strip()
            if answer == int(inference):
                print("正解!")
                subprocess.call("echo ピンポーん | say", shell=True)
                correct += 1
            else:
                print("ばーか.答えは{}だよ".format(answer))
                subprocess.call("echo ぶっぶー | say", shell=True)
        accuracy = correct/self.num*100
        tpp      = round((time.time()-s)/self.num, 3)
        print("正解率{}%, 一問あたりにかかった時間{}sec".format(accuracy, tpp))
        return accuracy, tpp


