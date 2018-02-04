'''Interactive graphs with Matplotlib have haunted me. So here I have collected a number of
tricks that should make interactive use of plots simpler. The functions below show how to

- Position figures on the screen (e.g. top left half of display)
- Pause and proceed automatically after a few sec
- Proceed on a click, or a keyboard hit
- Evaluate keyboard inputs

author: Thomas Haslwanter
date:   March-2015
ver:    1.0
license: Creative Commons Zero (almost public domain) http://scpyce.org/cc0

'''
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

t = np.arange(0,10,0.1)
c = np.cos(t)
s = np.sin(t)

def normalPlot():
    '''Just show a plot. The progam stops, and only continues when the plot is closed,
    either by hitting the "Window Close" button, or by typing "ALT+F4". '''
    
    plt.plot(t,s)
    plt.title('Normal plot: you have to close it to continue\nby clicking the "Window Close" button, or by hitting "ALT+F4"')
    plt.show()
    
def positionOnScreen():
    '''Position two plots on your screen. This uses the Tickle-backend, which I think is the default on all platforms.'''
    # Get the screen size
    root = tk.Tk()
    (screen_w, screen_h) = (root.winfo_screenwidth(), root.winfo_screenheight())
    root.destroy()
    
    # The program continues after the first plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(t,c)
    ax.set_title('Top Left: Close this one last')
    
    # Position the first graph in the top-left half of the screen
    position_topLeft = '{0}x{1}+{2}+{3}'.format(screen_w//2, screen_h//2,0,0)
    fig.canvas.manager.window.geometry(position_topLeft)
    
    # Put another graph in the top right half
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(t,s)
    # I don't completely understand why this one has to be closed first. But otherwise the program gets unstable.
    ax2.set_title('Top Right: Close this one first (e.g. with ALT+F4)')

    position_topRight = '{0}x{1}+{2}+{3}'.format(screen_w//2, screen_h//2,screen_w//2,0)
    fig2.canvas.manager.window.geometry(position_topRight)
    
    plt.show()

def showAndPause(): 
    '''Show a plot only for 2 seconds, and then proceed automatically'''
    plt.plot(t,s)
    plt.title('Don''t touch! I will proceed automatically.')
    
    plt.show(block=False)
    duration = 2    # [sec]
    plt.pause(duration)
    plt.close()
    
def waitForInput():    
    ''' This time, proceed with a click or by hitting any key '''
    plt.plot(t,c)
    plt.title('Click in that window, or hit any key to continue')
    
    plt.waitforbuttonpress()
    plt.close()

def keySelection():
    '''Wait for user intput, and proceed depending on the key entered.
    This is a bit complex. But None of the versions I tried without
    key binding were completely stable.'''
    
    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', on_key_event)
    
    # Disable default Matplotlib shortcut keys:
    keymaps = [param for param in plt.rcParams if param.find('keymap') >= 0]
    for key in keymaps:
        plt.rcParams[key] = ''
    
    ax.plot(t,c)
    ax.set_title('First, enter a vowel:')
    plt.show()
    
def on_key_event(event):
    '''Keyboard interaction'''

    #print('you pressed %s'%event.key)        
    key = event.key

    # In Python 2.x, the key gets indicated as "alt+[key]"
    # Bypass this bug:
    if key.find('alt') == 0:
        key = key.split('+')[1]

    curAxis = plt.gca()
    if key in 'aeiou':
        curAxis.set_title('Well done!')
        plt.pause(1)
        plt.close()
    else:
        curAxis.set_title(key + ' is not a vowel: try again to find a vowel ....')
        plt.draw()
    
if __name__ == '__main__':
    normalPlot()    
    positionOnScreen()    
    showAndPause()    
    waitForInput()    
    keySelection()