import matplotlib.pyplot as plt 
import numpy as np 
import re 

from .rep import REP 

def from_grace_to_tex(string):
    rep = dict((re.escape(k), v) for k, v in REP.items())
    pattern = re.compile("|".join(rep.keys()))
    new_string = pattern.sub(lambda m: rep[re.escape(m.group(0))], string)
    return r'{}'.format(new_string)

class GraceReader:
    def __init__(self, xvg_path, label):
        self.xvg_file = open(xvg_path, 'r')
        self.label = label 

        self.x, self.y, self.dx, self.dy = None, None, None, None 

    def read(self):
        x, y, dx, dy = [], [], [], []
        for line in self.xvg_file:
            buff = line.strip().split()
            if buff[0] != '#':
                if buff[0].startswith('@'):
                    if buff[1] == 'title':
                        self.title = from_grace_to_tex(' '.join(buff[2:]))
                    if buff[1] == 'xaxis':
                        if buff[2] == 'label':
                            self.xlabel = from_grace_to_tex(' '.join(buff[3:]))
                    if buff[1] == 'yaxis':
                        if buff[2] == 'label':
                            self.ylabel = from_grace_to_tex(' '.join(buff[3:]))
                    if buff[0].endswith('TYPE'):
                        self.type = buff[1]
                else:
                    x.append(float(buff[0]))
                    y.append(float(buff[1]))
                    if self.type == 'xydx':
                        dx.append(float(buff[2]))
                    if self.type == 'xydy':
                        dy.append(float(buff[2]))
        self.x, self.y = x, y 
        if self.type == 'xydx':
            self.dx = dx 
        if self.type == 'xydy':
            self.dy = dy 
    
    def clean(self, tol=25.):
        if self.type == 'xydy':
            x = np.array(self.x)
            y = np.array(self.y)
            dy = np.array(self.dy)
            idx = np.argwhere(dy > tol)
            x = np.array([xi for i, xi in enumerate(x) if i not in idx])
            y = np.array([yi for i, yi in enumerate(y) if i not in idx])
            dy = np.array([dyi for i, dyi in enumerate(dy) if i not in idx])
            self.x, self.y, self.dy = x, y, dy 
    
    def plot(self):
        if self.type == 'xydy':
            plt.errorbar(self.x, self.y, yerr=self.dy, label=self.label)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        plt.plot()

