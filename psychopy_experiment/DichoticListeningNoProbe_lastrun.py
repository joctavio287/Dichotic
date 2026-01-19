#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.2.3),
    on January 08, 2026, at 15:37
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# Run 'Before Experiment' code from code_row_selection
#import serial
#port = serial.Serial(
#    'COM3', baudrate=115200, timeout=0
#)
# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2025.2.3'
expName = 'DichoticListeningNoProbe'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = (1024, 768)
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\jocta\\repos\\Dichotic\\psychopy_experiment\\DichoticListeningNoProbe_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Espera mientras se configura el experimento...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='PsychToolbox',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "Instructions" ---
    # Run 'Begin Experiment' code from code_row_selection
    from psychopy import sound
    import pandas as pd
    import random
    
    # Define which rows to use
    NUMBER_OF_PAIRS=5
    selected_rows = random.sample(
        range(8), NUMBER_OF_PAIRS
    )
    thisExp.addData('selected_rows', selected_rows)
    
    # Read conditions, possible stimuli combinations and questionaries
    conditions = pd.read_csv(
        "conditions.csv",
        header=0,
        delimiter=','
    )
    audiobook_combinations = pd.read_csv(
        "audiobook_combinations_probes_pruebas.csv", 
        header=0, 
        delimiter=','
    )
    audiobook_questionary = pd.read_csv(
        "audiobook_questionary.csv", 
        header=0, 
        delimiter=','
    )
    
    # Store in memory audiobooks and relevant parameters
    attended_stories = []
    audio_filepaths = []
    questionaries = []
    targets = []
    audios = []
    for n_r, row in enumerate(selected_rows):
        condition_selected = conditions.iloc[row]
        targets.append(condition_selected['target'])
        
        # Define filepath and attended story
        filter_condition1 = audiobook_combinations['condition_label']==condition_selected["condition_label"]
        filter_condition2 = audiobook_combinations['ordered']==condition_selected["ordered"]
        audiobooks_possible_combinations = audiobook_combinations[filter_condition1&filter_condition2]
        
        # Get pairs, 1,2; 3,4; 5,6; ...
        n_story = (n_r+1)*2-1 # 1,3,5,7, ...
        filter_A = audiobooks_possible_combinations['story_A']==n_story
        filter_B = audiobooks_possible_combinations['story_B']==n_story
        selected_audiobook = audiobooks_possible_combinations[filter_A|filter_B]
        audio_filepath = selected_audiobook['filename'].values[0]
        audio_filepaths.append(audio_filepath)
        audios.append(
            sound.Sound(audio_filepath , hamming=True)
        )
        attended = f'story_{condition_selected["target_label"]}'
        attended_story = selected_audiobook[attended].values[0]
        attended_stories.append(attended_story)
        questionaries.append(
            audiobook_questionary.iloc[attended_story-1]
        )
    print(attended_stories)
    print(audio_filepaths)
    print(questionaries)
    print(targets)
    print(audios)
    key_instructions = keyboard.Keyboard(deviceName='defaultKeyboard')
    text_instructions = visual.TextStim(win=win, name='text_instructions',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "ConditionPrompt" ---
    text_prompt = visual.TextStim(win=win, name='text_prompt',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp_prompt = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "Bips" ---
    # set audio backend
    sound.Sound.backend = 'ptb'
    bip = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker=None,    name='bip'
    )
    bip.setVolume(1.0)
    fixation_bip = visual.ShapeStim(
        win=win, name='fixation_bip', vertices='cross',
        size=(0.1, 0.1),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    final_silence = visual.ShapeStim(
        win=win, name='final_silence', vertices='cross',
        size=(0.1, 0.1),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    
    # --- Initialize components for Routine "Listening" ---
    polygon = visual.ShapeStim(
        win=win, name='polygon', vertices='cross',
        size=(0.1, 0.1),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    
    # --- Initialize components for Routine "Bips" ---
    bip = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker=None,    name='bip'
    )
    bip.setVolume(1.0)
    fixation_bip = visual.ShapeStim(
        win=win, name='fixation_bip', vertices='cross',
        size=(0.1, 0.1),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    final_silence = visual.ShapeStim(
        win=win, name='final_silence', vertices='cross',
        size=(0.1, 0.1),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    
    # --- Initialize components for Routine "QuestionaryVariables" ---
    
    # --- Initialize components for Routine "Questionary" ---
    key_resp_questionary = keyboard.Keyboard(deviceName='defaultKeyboard')
    questionary_text = visual.TextStim(win=win, name='questionary_text',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "GoodBye" ---
    final_key = keyboard.Keyboard(deviceName='defaultKeyboard')
    final_text = visual.TextStim(win=win, name='final_text',
        text='¡Listo! Terminó el experimento. ¡Gracias por participar!\n\n\n\nApretá ESPACIO para finalizar...\n',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "Instructions" ---
    # create an object to store info about Routine Instructions
    Instructions = data.Routine(
        name='Instructions',
        components=[key_instructions, text_instructions],
    )
    Instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_row_selection
    port.write(bytes([int(25)]))
    # print(25)
    
    # create starting attributes for key_instructions
    key_instructions.keys = []
    key_instructions.rt = []
    _key_instructions_allKeys = []
    # store start times for Instructions
    Instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Instructions.tStart = globalClock.getTime(format='float')
    Instructions.status = STARTED
    thisExp.addData('Instructions.started', Instructions.tStart)
    Instructions.maxDuration = None
    # keep track of which components have finished
    InstructionsComponents = Instructions.components
    for thisComponent in Instructions.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Instructions" ---
    thisExp.currentRoutine = Instructions
    Instructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *key_instructions* updates
        waitOnFlip = False
        
        # if key_instructions is starting this frame...
        if key_instructions.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            key_instructions.frameNStart = frameN  # exact frame index
            key_instructions.tStart = t  # local t and not account for scr refresh
            key_instructions.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_instructions, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_instructions.started')
            # update status
            key_instructions.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_instructions.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_instructions.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_instructions.status == STARTED and not waitOnFlip:
            theseKeys = key_instructions.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_instructions_allKeys.extend(theseKeys)
            if len(_key_instructions_allKeys):
                key_instructions.keys = _key_instructions_allKeys[-1].name  # just the last key pressed
                key_instructions.rt = _key_instructions_allKeys[-1].rt
                key_instructions.duration = _key_instructions_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *text_instructions* updates
        
        # if text_instructions is starting this frame...
        if text_instructions.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            text_instructions.frameNStart = frameN  # exact frame index
            text_instructions.tStart = t  # local t and not account for scr refresh
            text_instructions.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_instructions, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_instructions.started')
            # update status
            text_instructions.status = STARTED
            text_instructions.setAutoDraw(True)
        
        # if text_instructions is active this frame...
        if text_instructions.status == STARTED:
            # update params
            text_instructions.setText('En cada ensayo escucharás dos historias simultáneas (una en cada oído). Tus tareas son\n\n1) Mantenerte quieto/a y mirar la cruz central.\n\n2) Prestar atención sólo a la historia indicada.\n\n3) Responder las preguntas con el teclado.\n\nPresioná ESPACIO para continuar...', log=False)
        
        # if text_instructions is stopping this frame...
        if text_instructions.status == STARTED:
            if bool(key_instructions.status == FINISHED):
                # keep track of stop time/frame for later
                text_instructions.tStop = t  # not accounting for scr refresh
                text_instructions.tStopRefresh = tThisFlipGlobal  # on global time
                text_instructions.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_instructions.stopped')
                # update status
                text_instructions.status = FINISHED
                text_instructions.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=Instructions,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            Instructions.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if Instructions.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in Instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Instructions" ---
    for thisComponent in Instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Instructions
    Instructions.tStop = globalClock.getTime(format='float')
    Instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Instructions.stopped', Instructions.tStop)
    # Run 'End Routine' code from code_row_selection
    port.write(bytes([int(30)]))
    # print(25)
    # check responses
    if key_instructions.keys in ['', [], None]:  # No response was made
        key_instructions.keys = None
    thisExp.addData('key_instructions.keys',key_instructions.keys)
    if key_instructions.keys != None:  # we had a response
        thisExp.addData('key_instructions.rt', key_instructions.rt)
        thisExp.addData('key_instructions.duration', key_instructions.duration)
    thisExp.nextEntry()
    # the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    condition_trials = data.TrialHandler2(
        name='condition_trials',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions(
        'conditions.csv', 
        selection=selected_rows
    )
    , 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(condition_trials)  # add the loop to the experiment
    thisCondition_trial = condition_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisCondition_trial.rgb)
    if thisCondition_trial != None:
        for paramName in thisCondition_trial:
            globals()[paramName] = thisCondition_trial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisCondition_trial in condition_trials:
        condition_trials.status = STARTED
        if hasattr(thisCondition_trial, 'status'):
            thisCondition_trial.status = STARTED
        currentLoop = condition_trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisCondition_trial.rgb)
        if thisCondition_trial != None:
            for paramName in thisCondition_trial:
                globals()[paramName] = thisCondition_trial[paramName]
        
        # --- Prepare to start Routine "ConditionPrompt" ---
        # create an object to store info about Routine ConditionPrompt
        ConditionPrompt = data.Routine(
            name='ConditionPrompt',
            components=[text_prompt, key_resp_prompt],
        )
        ConditionPrompt.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_prompt
        port.write(bytes([int(35)]))
        # print(35)
        
        flecha='<<<'  if target=='Left' else '>>>'
        lado='IZQUIERDO' if target=='Left' else 'DERECHO'
        
        
        text_prompt.setText(f"Presta atención a la historia del lado {lado} ({flecha}).\n\n\nApretá ESPACIO para continuar...")
        # create starting attributes for key_resp_prompt
        key_resp_prompt.keys = []
        key_resp_prompt.rt = []
        _key_resp_prompt_allKeys = []
        # store start times for ConditionPrompt
        ConditionPrompt.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        ConditionPrompt.tStart = globalClock.getTime(format='float')
        ConditionPrompt.status = STARTED
        thisExp.addData('ConditionPrompt.started', ConditionPrompt.tStart)
        ConditionPrompt.maxDuration = None
        # keep track of which components have finished
        ConditionPromptComponents = ConditionPrompt.components
        for thisComponent in ConditionPrompt.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "ConditionPrompt" ---
        thisExp.currentRoutine = ConditionPrompt
        ConditionPrompt.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisCondition_trial, 'status') and thisCondition_trial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text_prompt* updates
            
            # if text_prompt is starting this frame...
            if text_prompt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_prompt.frameNStart = frameN  # exact frame index
                text_prompt.tStart = t  # local t and not account for scr refresh
                text_prompt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_prompt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_prompt.started')
                # update status
                text_prompt.status = STARTED
                text_prompt.setAutoDraw(True)
            
            # if text_prompt is active this frame...
            if text_prompt.status == STARTED:
                # update params
                pass
            
            # if text_prompt is stopping this frame...
            if text_prompt.status == STARTED:
                if bool(key_resp_prompt.status == FINISHED):
                    # keep track of stop time/frame for later
                    text_prompt.tStop = t  # not accounting for scr refresh
                    text_prompt.tStopRefresh = tThisFlipGlobal  # on global time
                    text_prompt.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_prompt.stopped')
                    # update status
                    text_prompt.status = FINISHED
                    text_prompt.setAutoDraw(False)
            
            # *key_resp_prompt* updates
            waitOnFlip = False
            
            # if key_resp_prompt is starting this frame...
            if key_resp_prompt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp_prompt.frameNStart = frameN  # exact frame index
                key_resp_prompt.tStart = t  # local t and not account for scr refresh
                key_resp_prompt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_prompt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_prompt.started')
                # update status
                key_resp_prompt.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_prompt.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_prompt.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_prompt.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_prompt.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_prompt_allKeys.extend(theseKeys)
                if len(_key_resp_prompt_allKeys):
                    key_resp_prompt.keys = _key_resp_prompt_allKeys[-1].name  # just the last key pressed
                    key_resp_prompt.rt = _key_resp_prompt_allKeys[-1].rt
                    key_resp_prompt.duration = _key_resp_prompt_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=ConditionPrompt,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                ConditionPrompt.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if ConditionPrompt.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in ConditionPrompt.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "ConditionPrompt" ---
        for thisComponent in ConditionPrompt.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for ConditionPrompt
        ConditionPrompt.tStop = globalClock.getTime(format='float')
        ConditionPrompt.tStopRefresh = tThisFlipGlobal
        thisExp.addData('ConditionPrompt.stopped', ConditionPrompt.tStop)
        # Run 'End Routine' code from code_prompt
        port.write(bytes([int(40)])
        # print(40)
        # check responses
        if key_resp_prompt.keys in ['', [], None]:  # No response was made
            key_resp_prompt.keys = None
        condition_trials.addData('key_resp_prompt.keys',key_resp_prompt.keys)
        if key_resp_prompt.keys != None:  # we had a response
            condition_trials.addData('key_resp_prompt.rt', key_resp_prompt.rt)
            condition_trials.addData('key_resp_prompt.duration', key_resp_prompt.duration)
        # the Routine "ConditionPrompt" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        bip_trials1 = data.TrialHandler2(
            name='bip_trials1',
            nReps=10.0, 
            method='random', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
            isTrials=False, 
        )
        thisExp.addLoop(bip_trials1)  # add the loop to the experiment
        thisBip_trials1 = bip_trials1.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisBip_trials1.rgb)
        if thisBip_trials1 != None:
            for paramName in thisBip_trials1:
                globals()[paramName] = thisBip_trials1[paramName]
        
        for thisBip_trials1 in bip_trials1:
            bip_trials1.status = STARTED
            if hasattr(thisBip_trials1, 'status'):
                thisBip_trials1.status = STARTED
            currentLoop = bip_trials1
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            # abbreviate parameter names if possible (e.g. rgb = thisBip_trials1.rgb)
            if thisBip_trials1 != None:
                for paramName in thisBip_trials1:
                    globals()[paramName] = thisBip_trials1[paramName]
            
            # --- Prepare to start Routine "Bips" ---
            # create an object to store info about Routine Bips
            Bips = data.Routine(
                name='Bips',
                components=[bip, fixation_bip, final_silence],
            )
            Bips.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_bip
            if currentLoop.name == "bip_trials1":
                trigger = 45
            else:
                trigger = 150
            
            port.write(bytes([int(trigger+currentLoop.thisN*3)]))
            # print(int(trigger+currentLoop.thisN*3))
            
            # When the loop reaches the end, there will be no silence added
            if currentLoop.thisN == (currentLoop.nTotal - 1):
                final_silence.status = FINISHED
            bip.setSound('../data/processed_audios/bip.ogg', hamming=True)
            bip.setVolume(1.0, log=False)
            bip.seek(0)
            # store start times for Bips
            Bips.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Bips.tStart = globalClock.getTime(format='float')
            Bips.status = STARTED
            thisExp.addData('Bips.started', Bips.tStart)
            Bips.maxDuration = None
            # keep track of which components have finished
            BipsComponents = Bips.components
            for thisComponent in Bips.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Bips" ---
            thisExp.currentRoutine = Bips
            Bips.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisBip_trials1, 'status') and thisBip_trials1.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *bip* updates
                
                # if bip is starting this frame...
                if bip.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    bip.frameNStart = frameN  # exact frame index
                    bip.tStart = t  # local t and not account for scr refresh
                    bip.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('bip.started', tThisFlipGlobal)
                    # update status
                    bip.status = STARTED
                    bip.play(when=win)  # sync with win flip
                
                # if bip is stopping this frame...
                if bip.status == STARTED:
                    if bool(False) or bip.isFinished:
                        # keep track of stop time/frame for later
                        bip.tStop = t  # not accounting for scr refresh
                        bip.tStopRefresh = tThisFlipGlobal  # on global time
                        bip.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'bip.stopped')
                        # update status
                        bip.status = FINISHED
                        bip.stop()
                
                # *fixation_bip* updates
                
                # if fixation_bip is starting this frame...
                if fixation_bip.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    fixation_bip.frameNStart = frameN  # exact frame index
                    fixation_bip.tStart = t  # local t and not account for scr refresh
                    fixation_bip.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fixation_bip, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_bip.started')
                    # update status
                    fixation_bip.status = STARTED
                    fixation_bip.setAutoDraw(True)
                
                # if fixation_bip is active this frame...
                if fixation_bip.status == STARTED:
                    # update params
                    pass
                
                # if fixation_bip is stopping this frame...
                if fixation_bip.status == STARTED:
                    if bool(bip.status == FINISHED ):
                        # keep track of stop time/frame for later
                        fixation_bip.tStop = t  # not accounting for scr refresh
                        fixation_bip.tStopRefresh = tThisFlipGlobal  # on global time
                        fixation_bip.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'fixation_bip.stopped')
                        # update status
                        fixation_bip.status = FINISHED
                        fixation_bip.setAutoDraw(False)
                
                # *final_silence* updates
                
                # if final_silence is starting this frame...
                if final_silence.status == NOT_STARTED and bip.status==FINISHED:
                    # keep track of start time/frame for later
                    final_silence.frameNStart = frameN  # exact frame index
                    final_silence.tStart = t  # local t and not account for scr refresh
                    final_silence.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(final_silence, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'final_silence.started')
                    # update status
                    final_silence.status = STARTED
                    final_silence.setAutoDraw(True)
                
                # if final_silence is active this frame...
                if final_silence.status == STARTED:
                    # update params
                    pass
                
                # if final_silence is stopping this frame...
                if final_silence.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > final_silence.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        final_silence.tStop = t  # not accounting for scr refresh
                        final_silence.tStopRefresh = tThisFlipGlobal  # on global time
                        final_silence.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'final_silence.stopped')
                        # update status
                        final_silence.status = FINISHED
                        final_silence.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Bips,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Bips.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Bips.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Bips.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Bips" ---
            for thisComponent in Bips.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Bips
            Bips.tStop = globalClock.getTime(format='float')
            Bips.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Bips.stopped', Bips.tStop)
            # Run 'End Routine' code from code_bip
            port.write(bytes([int(trigger+currentLoop.thisN*3+1)]))
            # print(int(trigger+currentLoop.thisN*3+1))
            bip.pause()  # ensure sound has stopped at end of Routine
            # the Routine "Bips" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            # mark thisBip_trials1 as finished
            if hasattr(thisBip_trials1, 'status'):
                thisBip_trials1.status = FINISHED
            # if awaiting a pause, pause now
            if bip_trials1.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                bip_trials1.status = STARTED
        # completed 10.0 repeats of 'bip_trials1'
        bip_trials1.status = FINISHED
        
        
        # --- Prepare to start Routine "Listening" ---
        # create an object to store info about Routine Listening
        Listening = data.Routine(
            name='Listening',
            components=[polygon],
        )
        Listening.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_listening
        # Set correct audio
        audiobook = audios[condition_trials.thisN]
        port.write(bytes([int(100)]))
        # print(100)
        # t is measured since routine start
        thisExp.addData("time_audiobook_started",t)
        audiobook.play()
        
        
        
        
        
        # store start times for Listening
        Listening.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Listening.tStart = globalClock.getTime(format='float')
        Listening.status = STARTED
        thisExp.addData('Listening.started', Listening.tStart)
        Listening.maxDuration = None
        # keep track of which components have finished
        ListeningComponents = Listening.components
        for thisComponent in Listening.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Listening" ---
        thisExp.currentRoutine = Listening
        Listening.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisCondition_trial, 'status') and thisCondition_trial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from code_listening
            # When time exceed audiobook duration, end component
            # t is measured since routine start
            if t >= audiobook.duration:
                continueRoutine = False
                audiobook.stop() 
                thisExp.addData("time_audiobook_finished",t)
            
            
                
                
            
            # *polygon* updates
            
            # if polygon is starting this frame...
            if polygon.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                polygon.frameNStart = frameN  # exact frame index
                polygon.tStart = t  # local t and not account for scr refresh
                polygon.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'polygon.started')
                # update status
                polygon.status = STARTED
                polygon.setAutoDraw(True)
            
            # if polygon is active this frame...
            if polygon.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=Listening,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                Listening.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if Listening.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in Listening.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Listening" ---
        for thisComponent in Listening.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Listening
        Listening.tStop = globalClock.getTime(format='float')
        Listening.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Listening.stopped', Listening.tStop)
        # Run 'End Routine' code from code_listening
        port.write(bytes([int(105)]))
        # print(105)
        
        
        
        # the Routine "Listening" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        bip_trials2 = data.TrialHandler2(
            name='bip_trials2',
            nReps=10.0, 
            method='sequential', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
            isTrials=False, 
        )
        thisExp.addLoop(bip_trials2)  # add the loop to the experiment
        thisBip_trials2 = bip_trials2.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisBip_trials2.rgb)
        if thisBip_trials2 != None:
            for paramName in thisBip_trials2:
                globals()[paramName] = thisBip_trials2[paramName]
        
        for thisBip_trials2 in bip_trials2:
            bip_trials2.status = STARTED
            if hasattr(thisBip_trials2, 'status'):
                thisBip_trials2.status = STARTED
            currentLoop = bip_trials2
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            # abbreviate parameter names if possible (e.g. rgb = thisBip_trials2.rgb)
            if thisBip_trials2 != None:
                for paramName in thisBip_trials2:
                    globals()[paramName] = thisBip_trials2[paramName]
            
            # --- Prepare to start Routine "Bips" ---
            # create an object to store info about Routine Bips
            Bips = data.Routine(
                name='Bips',
                components=[bip, fixation_bip, final_silence],
            )
            Bips.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_bip
            if currentLoop.name == "bip_trials1":
                trigger = 45
            else:
                trigger = 150
            
            port.write(bytes([int(trigger+currentLoop.thisN*3)]))
            # print(int(trigger+currentLoop.thisN*3))
            
            # When the loop reaches the end, there will be no silence added
            if currentLoop.thisN == (currentLoop.nTotal - 1):
                final_silence.status = FINISHED
            bip.setSound('../data/processed_audios/bip.ogg', hamming=True)
            bip.setVolume(1.0, log=False)
            bip.seek(0)
            # store start times for Bips
            Bips.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Bips.tStart = globalClock.getTime(format='float')
            Bips.status = STARTED
            thisExp.addData('Bips.started', Bips.tStart)
            Bips.maxDuration = None
            # keep track of which components have finished
            BipsComponents = Bips.components
            for thisComponent in Bips.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Bips" ---
            thisExp.currentRoutine = Bips
            Bips.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisBip_trials2, 'status') and thisBip_trials2.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *bip* updates
                
                # if bip is starting this frame...
                if bip.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    bip.frameNStart = frameN  # exact frame index
                    bip.tStart = t  # local t and not account for scr refresh
                    bip.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('bip.started', tThisFlipGlobal)
                    # update status
                    bip.status = STARTED
                    bip.play(when=win)  # sync with win flip
                
                # if bip is stopping this frame...
                if bip.status == STARTED:
                    if bool(False) or bip.isFinished:
                        # keep track of stop time/frame for later
                        bip.tStop = t  # not accounting for scr refresh
                        bip.tStopRefresh = tThisFlipGlobal  # on global time
                        bip.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'bip.stopped')
                        # update status
                        bip.status = FINISHED
                        bip.stop()
                
                # *fixation_bip* updates
                
                # if fixation_bip is starting this frame...
                if fixation_bip.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    fixation_bip.frameNStart = frameN  # exact frame index
                    fixation_bip.tStart = t  # local t and not account for scr refresh
                    fixation_bip.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fixation_bip, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_bip.started')
                    # update status
                    fixation_bip.status = STARTED
                    fixation_bip.setAutoDraw(True)
                
                # if fixation_bip is active this frame...
                if fixation_bip.status == STARTED:
                    # update params
                    pass
                
                # if fixation_bip is stopping this frame...
                if fixation_bip.status == STARTED:
                    if bool(bip.status == FINISHED ):
                        # keep track of stop time/frame for later
                        fixation_bip.tStop = t  # not accounting for scr refresh
                        fixation_bip.tStopRefresh = tThisFlipGlobal  # on global time
                        fixation_bip.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'fixation_bip.stopped')
                        # update status
                        fixation_bip.status = FINISHED
                        fixation_bip.setAutoDraw(False)
                
                # *final_silence* updates
                
                # if final_silence is starting this frame...
                if final_silence.status == NOT_STARTED and bip.status==FINISHED:
                    # keep track of start time/frame for later
                    final_silence.frameNStart = frameN  # exact frame index
                    final_silence.tStart = t  # local t and not account for scr refresh
                    final_silence.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(final_silence, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'final_silence.started')
                    # update status
                    final_silence.status = STARTED
                    final_silence.setAutoDraw(True)
                
                # if final_silence is active this frame...
                if final_silence.status == STARTED:
                    # update params
                    pass
                
                # if final_silence is stopping this frame...
                if final_silence.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > final_silence.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        final_silence.tStop = t  # not accounting for scr refresh
                        final_silence.tStopRefresh = tThisFlipGlobal  # on global time
                        final_silence.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'final_silence.stopped')
                        # update status
                        final_silence.status = FINISHED
                        final_silence.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Bips,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Bips.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Bips.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Bips.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Bips" ---
            for thisComponent in Bips.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Bips
            Bips.tStop = globalClock.getTime(format='float')
            Bips.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Bips.stopped', Bips.tStop)
            # Run 'End Routine' code from code_bip
            port.write(bytes([int(trigger+currentLoop.thisN*3+1)]))
            # print(int(trigger+currentLoop.thisN*3+1))
            bip.pause()  # ensure sound has stopped at end of Routine
            # the Routine "Bips" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            # mark thisBip_trials2 as finished
            if hasattr(thisBip_trials2, 'status'):
                thisBip_trials2.status = FINISHED
            # if awaiting a pause, pause now
            if bip_trials2.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                bip_trials2.status = STARTED
        # completed 10.0 repeats of 'bip_trials2'
        bip_trials2.status = FINISHED
        
        
        # --- Prepare to start Routine "QuestionaryVariables" ---
        # create an object to store info about Routine QuestionaryVariables
        QuestionaryVariables = data.Routine(
            name='QuestionaryVariables',
            components=[],
        )
        QuestionaryVariables.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_questionary_2
        attended_story_ = attended_stories[condition_trials.thisN]
        audio_filepath_ = audio_filepaths[condition_trials.thisN]
        questionary_ = questionaries[condition_trials.thisN]
        
        # Add to log
        thisExp.addData('attended_story', attended_story_)
        thisExp.addData('audio_filepath', audio_filepath_)
        thisExp.addData('target', target)
        
        # Define new variables
        correct_answers = []
        questions = []
        answers_a = []
        answers_b = []
        answers_c = []
        for i in range(1, 4):
            correct_answer = questionary_[f'correct_answer{i}']
            question = questionary_[f'question{i}']
            answer_a = questionary_[f'answer{i}a']
            answer_b = questionary_[f'answer{i}b']
            answer_c = questionary_[f'answer{i}c']
            correct_answers.append(correct_answer)
            questions.append(question)
            answers_a.append(answer_a)
            answers_b.append(answer_b)
            answers_c.append(answer_c)  
        
            # Add to log
            thisExp.addData(f'correct_answer{i}', correct_answer)
            thisExp.addData(f'question{i}', question)
            thisExp.addData(f'answer{i}a', answer_a)
            thisExp.addData(f'answer{i}b', answer_b)
            thisExp.addData(f'answer{i}c', answer_c)
        # store start times for QuestionaryVariables
        QuestionaryVariables.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        QuestionaryVariables.tStart = globalClock.getTime(format='float')
        QuestionaryVariables.status = STARTED
        thisExp.addData('QuestionaryVariables.started', QuestionaryVariables.tStart)
        QuestionaryVariables.maxDuration = None
        # keep track of which components have finished
        QuestionaryVariablesComponents = QuestionaryVariables.components
        for thisComponent in QuestionaryVariables.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "QuestionaryVariables" ---
        thisExp.currentRoutine = QuestionaryVariables
        QuestionaryVariables.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisCondition_trial, 'status') and thisCondition_trial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=QuestionaryVariables,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                QuestionaryVariables.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if QuestionaryVariables.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in QuestionaryVariables.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "QuestionaryVariables" ---
        for thisComponent in QuestionaryVariables.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for QuestionaryVariables
        QuestionaryVariables.tStop = globalClock.getTime(format='float')
        QuestionaryVariables.tStopRefresh = tThisFlipGlobal
        thisExp.addData('QuestionaryVariables.stopped', QuestionaryVariables.tStop)
        # the Routine "QuestionaryVariables" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        questions_trial = data.TrialHandler2(
            name='questions_trial',
            nReps=3.0, 
            method='sequential', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
            isTrials=False, 
        )
        thisExp.addLoop(questions_trial)  # add the loop to the experiment
        thisQuestions_trial = questions_trial.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisQuestions_trial.rgb)
        if thisQuestions_trial != None:
            for paramName in thisQuestions_trial:
                globals()[paramName] = thisQuestions_trial[paramName]
        
        for thisQuestions_trial in questions_trial:
            questions_trial.status = STARTED
            if hasattr(thisQuestions_trial, 'status'):
                thisQuestions_trial.status = STARTED
            currentLoop = questions_trial
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            # abbreviate parameter names if possible (e.g. rgb = thisQuestions_trial.rgb)
            if thisQuestions_trial != None:
                for paramName in thisQuestions_trial:
                    globals()[paramName] = thisQuestions_trial[paramName]
            
            # --- Prepare to start Routine "Questionary" ---
            # create an object to store info about Routine Questionary
            Questionary = data.Routine(
                name='Questionary',
                components=[key_resp_questionary, questionary_text],
            )
            Questionary.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_questionary
            question = questions[questions_trial.thisRepN-1]
            correct_answer = correct_answers[questions_trial.thisRepN-1]
            answer_a = answers_a[questions_trial.thisRepN-1]
            answer_b = answers_b[questions_trial.thisRepN-1]
            answer_c = answers_c[questions_trial.thisRepN-1]
            
            port.write(bytes([int(200+currentLoop.thisN*3)]))
            # print(int(200+currentLoop.thisN*3))
            
            # create starting attributes for key_resp_questionary
            key_resp_questionary.keys = []
            key_resp_questionary.rt = []
            _key_resp_questionary_allKeys = []
            questionary_text.setText(f"{question}\n\n A: {answer_a}\n\n B: {answer_b}\n\n C: {answer_c}\n\n Presioná la opción que creas correcta (teclas A, B ó C)"
            
            
            
            )
            # store start times for Questionary
            Questionary.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Questionary.tStart = globalClock.getTime(format='float')
            Questionary.status = STARTED
            thisExp.addData('Questionary.started', Questionary.tStart)
            Questionary.maxDuration = None
            # keep track of which components have finished
            QuestionaryComponents = Questionary.components
            for thisComponent in Questionary.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Questionary" ---
            thisExp.currentRoutine = Questionary
            Questionary.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisQuestions_trial, 'status') and thisQuestions_trial.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *key_resp_questionary* updates
                waitOnFlip = False
                
                # if key_resp_questionary is starting this frame...
                if key_resp_questionary.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp_questionary.frameNStart = frameN  # exact frame index
                    key_resp_questionary.tStart = t  # local t and not account for scr refresh
                    key_resp_questionary.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp_questionary, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp_questionary.started')
                    # update status
                    key_resp_questionary.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp_questionary.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp_questionary.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp_questionary.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp_questionary.getKeys(keyList=['a', 'b', 'c'], ignoreKeys=["escape"], waitRelease=False)
                    _key_resp_questionary_allKeys.extend(theseKeys)
                    if len(_key_resp_questionary_allKeys):
                        key_resp_questionary.keys = _key_resp_questionary_allKeys[-1].name  # just the last key pressed
                        key_resp_questionary.rt = _key_resp_questionary_allKeys[-1].rt
                        key_resp_questionary.duration = _key_resp_questionary_allKeys[-1].duration
                        # a response ends the routine
                        continueRoutine = False
                
                # *questionary_text* updates
                
                # if questionary_text is starting this frame...
                if questionary_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    questionary_text.frameNStart = frameN  # exact frame index
                    questionary_text.tStart = t  # local t and not account for scr refresh
                    questionary_text.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(questionary_text, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'questionary_text.started')
                    # update status
                    questionary_text.status = STARTED
                    questionary_text.setAutoDraw(True)
                
                # if questionary_text is active this frame...
                if questionary_text.status == STARTED:
                    # update params
                    pass
                
                # if questionary_text is stopping this frame...
                if questionary_text.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > questionary_text.tStartRefresh + key_resp_questionary.status == FINISHED-frameTolerance:
                        # keep track of stop time/frame for later
                        questionary_text.tStop = t  # not accounting for scr refresh
                        questionary_text.tStopRefresh = tThisFlipGlobal  # on global time
                        questionary_text.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'questionary_text.stopped')
                        # update status
                        questionary_text.status = FINISHED
                        questionary_text.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Questionary,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Questionary.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Questionary.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Questionary.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Questionary" ---
            for thisComponent in Questionary.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Questionary
            Questionary.tStop = globalClock.getTime(format='float')
            Questionary.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Questionary.stopped', Questionary.tStop)
            # Run 'End Routine' code from code_questionary
            port.write(bytes([int(200+1+currentLoop.thisN*3)]))
            # print(int(200+1+currentLoop.thisN*3))
            # check responses
            if key_resp_questionary.keys in ['', [], None]:  # No response was made
                key_resp_questionary.keys = None
            questions_trial.addData('key_resp_questionary.keys',key_resp_questionary.keys)
            if key_resp_questionary.keys != None:  # we had a response
                questions_trial.addData('key_resp_questionary.rt', key_resp_questionary.rt)
                questions_trial.addData('key_resp_questionary.duration', key_resp_questionary.duration)
            # the Routine "Questionary" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            # mark thisQuestions_trial as finished
            if hasattr(thisQuestions_trial, 'status'):
                thisQuestions_trial.status = FINISHED
            # if awaiting a pause, pause now
            if questions_trial.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                questions_trial.status = STARTED
        # completed 3.0 repeats of 'questions_trial'
        questions_trial.status = FINISHED
        
        # mark thisCondition_trial as finished
        if hasattr(thisCondition_trial, 'status'):
            thisCondition_trial.status = FINISHED
        # if awaiting a pause, pause now
        if condition_trials.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            condition_trials.status = STARTED
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'condition_trials'
    condition_trials.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "GoodBye" ---
    # create an object to store info about Routine GoodBye
    GoodBye = data.Routine(
        name='GoodBye',
        components=[final_key, final_text],
    )
    GoodBye.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_bye
    port.write(bytes([int(230)])
    # print(230)
    # create starting attributes for final_key
    final_key.keys = []
    final_key.rt = []
    _final_key_allKeys = []
    # store start times for GoodBye
    GoodBye.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    GoodBye.tStart = globalClock.getTime(format='float')
    GoodBye.status = STARTED
    thisExp.addData('GoodBye.started', GoodBye.tStart)
    GoodBye.maxDuration = None
    # keep track of which components have finished
    GoodByeComponents = GoodBye.components
    for thisComponent in GoodBye.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "GoodBye" ---
    thisExp.currentRoutine = GoodBye
    GoodBye.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *final_key* updates
        waitOnFlip = False
        
        # if final_key is starting this frame...
        if final_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            final_key.frameNStart = frameN  # exact frame index
            final_key.tStart = t  # local t and not account for scr refresh
            final_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(final_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'final_key.started')
            # update status
            final_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(final_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(final_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if final_key.status == STARTED and not waitOnFlip:
            theseKeys = final_key.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _final_key_allKeys.extend(theseKeys)
            if len(_final_key_allKeys):
                final_key.keys = _final_key_allKeys[-1].name  # just the last key pressed
                final_key.rt = _final_key_allKeys[-1].rt
                final_key.duration = _final_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *final_text* updates
        
        # if final_text is starting this frame...
        if final_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            final_text.frameNStart = frameN  # exact frame index
            final_text.tStart = t  # local t and not account for scr refresh
            final_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(final_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'final_text.started')
            # update status
            final_text.status = STARTED
            final_text.setAutoDraw(True)
        
        # if final_text is active this frame...
        if final_text.status == STARTED:
            # update params
            pass
        
        # if final_text is stopping this frame...
        if final_text.status == STARTED:
            if bool(final_key.status == FINISHED):
                # keep track of stop time/frame for later
                final_text.tStop = t  # not accounting for scr refresh
                final_text.tStopRefresh = tThisFlipGlobal  # on global time
                final_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'final_text.stopped')
                # update status
                final_text.status = FINISHED
                final_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=GoodBye,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            GoodBye.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if GoodBye.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in GoodBye.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "GoodBye" ---
    for thisComponent in GoodBye.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for GoodBye
    GoodBye.tStop = globalClock.getTime(format='float')
    GoodBye.tStopRefresh = tThisFlipGlobal
    thisExp.addData('GoodBye.stopped', GoodBye.tStop)
    # Run 'End Routine' code from code_bye
    port.write(bytes([int(240)])
    # print(240)
    # check responses
    if final_key.keys in ['', [], None]:  # No response was made
        final_key.keys = None
    thisExp.addData('final_key.keys',final_key.keys)
    if final_key.keys != None:  # we had a response
        thisExp.addData('final_key.rt', final_key.rt)
        thisExp.addData('final_key.duration', final_key.duration)
    thisExp.nextEntry()
    # the Routine "GoodBye" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
