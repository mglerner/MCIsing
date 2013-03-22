#!/usr/bin/env python
from __future__ import division
import numpy as np
import pylab
from numpy.random import random #import only one function from somewhere
from numpy.random import randint
from numpy import mod, exp
import scipy
import matplotlib.cm as cm
from time import sleep

def initialize(size):
    """
    Initialize a random array where our spins are all up or down.
    """
    myarray = random([size,size]) # initializes with random numbers from 0 to 1.
    myarray[myarray<0.5] = -1
    myarray[myarray>=0.5] = 1
    return myarray

@profile
def deltaU(s,i,j):
    """
    Compute delta U of flipping a given dipole at i,j
    Note periodic boundary conditions, which is why we need to know the size.
    """
    size = s.shape[0]
    try:
        above = s[i+1,j]
        below = s[i-1,j]
        right = s[i,j+1]
        left =  s[i,j-1]
    except:
        above = s[mod(i+1,size),j]
        below = s[mod(i-1,size),j]
        right = s[i,mod(j+1,size)]
        left =  s[i,mod(j-1,size)]

    return 2*s[i,j]*(above+below+left+right)

def colorsquare(s,fig):
    fig.clear()
    pylab.imshow(s,interpolation='nearest',cmap=cm.Greys_r)
    fig.canvas.draw()
    #ax.set_title("Trial %s of %s"%(trial,numtrials))
    pylab.draw()


def shouldshow(iteration,size,showevery):
    if showevery is 1:
        return True
    if showevery == -1:
        return False
    if showevery is None:
        #if size <= 10:
        #    showevery = 1
        #    delay = 5
        if size < 100:
            showevery = int(size*size/2)
        else:
            showevery = size*size
        return divmod(iteration,showevery)[1] == 0

@profile
def simulate(size, T, showevery=None, graphics=True):
    """
    
    Arguments:
    - `size`: lattice length
    - `T`: in units of epsilon/k
    - `showevery`: how often to update the display. If None, a heuristic will be used.
    """
    # Some magic to set up plotting
    #pylab.ion() # You need this if running standalone

    if graphics:
        fig = pylab.figure()
        ax = fig.add_subplot(111)

    s = initialize(size)

    if graphics:
        colorsquare(s,fig)
        pylab.show()
    

    numtrials = 100*size**2
    print "numtrials",numtrials
        
    for trial in xrange(numtrials):
        i = randint(size) # choose random row
        j = randint(size) # and random column
        ediff = deltaU(s,i,j)
        if ediff <= 0: # flipping reduces the energy
            s[i,j] = -s[i,j]
        else:
            if random() < exp(-ediff/T):
                s[i,j] = -s[i,j]
        if graphics and shouldshow(trial,size,showevery):
            print "Showing iteration",trial
            colorsquare(s,fig)
    if graphics: colorsquare(s,fig)
    
if __name__ == '__main__':
    raw_input()  # you need this.
