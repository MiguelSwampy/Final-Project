from psychopy import visual, monitors, core, event, gui
import csv
import os
import random

expInfo = {'SubjectNumber': 0, 'Age':0, 'Gender': ('male','female','other')}
myDlg = gui.DlgFromDict(dictionary=expInfo)
filename = (str(expInfo['SubjectNumber']) +'_' + (str(expInfo['Age'])) + '_' +(expInfo['Gender']) + '.csv')

main_dir = os.getcwd()
data_dir = os.path.join(main_dir, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
fullAddress = os.path.join(data_dir, filename)

def stimColor(stim):
    RTstim.color=colorsLst[block][trial] 
    RTstim.draw()

nBlocks = 2
nTrials = 6

reactionTime = [[0] * nTrials]*nBlocks
fixTime = [[0] * nTrials]*nBlocks
colorData = [[0] * nTrials]*nBlocks
blocks = [[0,0,0,0,0,0], [1,1,1,1,1,1]]
trials = [[0,1,2,3,4,5], [0,1,2,3,4,5]]

mon = monitors.Monitor('myMonitor', width=35.56, distance=60)
mon.setSizePix([1920, 1080])
win = visual.Window(monitor=mon, size=(800,800), units = 'pix', fullscr = True)

instText = visual.TextStim(win, text = 'A square will appear on the screen, press the spacebar the moment you see it. Press the spacebar to continue.')
fixStim = visual.TextStim(win, text = '+')
RTstim = visual.Rect(win, size = (300, 300), units = 'pix')
colorsLst = [['red', 'green', 'blue', 'red', 'green', 'blue'],['red', 'green', 'blue', 'red', 'green', 'blue']]


instText.draw()
win.flip()
event.waitKeys(keyList = ['space', 'escape'])

RTclock = core.Clock()

for block in range(nBlocks):
    instText.text = 'Press the spacebar to start block' + str(block+1)
    instText.draw()
    win.flip()
    event.waitKeys(keyList = ['space'])
    
    random.shuffle(colorsLst[1])
    
    for trial in range(nTrials):
        event.clearEvents(eventType = 'keyboard')
        fixDur = random.randint(1,3)
        fixTime[block][trial] = fixDur
   
        fixStim.draw()
        win.flip()
        core.wait(fixDur)
    
        stimColor(RTstim)
        colorData = colorsLst
        win.flip()
        RTclock.reset() 
        
        keys = event.waitKeys(keyList = ['space', 'escape']) 
        
        if keys:
            if 'escape' in keys:
                win.close()
            else:
                reactionTime[block][trial] = RTclock.getTime()

instText.text = 'The expirement has concluded, thank you.'
instText.draw()
win.flip()
core.wait(2)

with open(fullAddress, 'w') as sub_data:
    fieldnames = ['Block', 'Trial', 'Reaction Time','Fixation Duration', 'Stimulus Color']
    data_writer = csv.DictWriter(sub_data, fieldnames=fieldnames)
    data_writer.writeheader()
    
    for block in range(nBlocks):
        data_as_dict = []
        for a,b,c,d,e in zip(blocks[block], trials[block], reactionTime[block], fixTime[block], colorData[block]):
            data_as_dict.append({'Block':a, 'Trial':b, 'Reaction Time': c, 'Fixation Duration': d, 'Stimulus Color': e})

        for iTrial in range(nTrials):
            data_writer.writerow(data_as_dict[iTrial])

win.close()
