#!/usr/bin/env python
# coding: utf-8

from __future__ import division
from __future__ import print_function
import argparse
import numpy as np
import subprocess
import time
import sys
import matplotlib.pyplot as plt


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
        self.sequence = []
        for _  in range(self.num):
            first   = self.__random_digit(self.caled)
            secound = self.__random_digit(self.calee)
            triplet = (first, secound, self.operator(first, secound))
            self.sequence.append(triplet)
        return self.sequence

    def __call__(self):
        s = time.time()
        correct = 0
        for first, secound, answer in self.triplet():
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', default=10, type=int)
    parser.add_argument('-s', '--shape', nargs=2, default=(2, 2), type=int)
    parser.add_argument('-o', '--operator', default='add')
    parser.add_argument('-m', '--mute', default=False, type=bool)
    args = parser.parse_args()

    p = Problem(args.num, args.shape, args.operator, args.mute)

    accuracy, tpp = p()

    result_accuracy = []
    result_tpp      = []

    with open("{}_{}_{}.log".format(args.operator, args.shape[0], args.shape[1]), "a+") as f:
        f.write("{},{}\n".format(accuracy, tpp))
    with open("{}_{}_{}.log".format(args.operator, args.shape[0], args.shape[1]), "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = [float(number) for number in line.split(',')]
            result_accuracy.append(line[0])
            result_tpp.append(line[1])
    print("{} {}digit and {}digitの結果を表示しますか?[y/n]".format(args.operator, args.shape[0], args.shape[1]))
    if sys.stdin.readline().strip() == 'y':
        X = [1, 2, 3]
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        ax1.bar(X, [sum(result_tpp)/len(result_tpp), min(result_tpp), result_tpp[-1]], align='center')
        ax1.set_title('time per problem')
        ax1.set_ylabel('s')
        ax1.set_xticks(X)
        ax1.set_xticklabels(['mean', 'min', 'now'])

        score = np.array(result_accuracy)/np.array(result_tpp)
        ax2.bar(X, [np.mean(score), np.max(score), score[-1]], align='center')
        ax2.set_title('score')
        ax2.set_xticks(X)
        ax2.set_xticklabels(['mean', 'max', 'now'])
        plt.subplots_adjust(hspace=0.4)
        plt.show()






