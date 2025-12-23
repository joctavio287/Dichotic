/*************************** 
 * Dichotic_Listening *
 ***************************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.2.3.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'dichotic_listening';  // from the Builder filename that created this script
let expInfo = {
    'participant': `${util.pad(Number.parseFloat(util.randint(0, 999999)).toFixed(0), 6)}`,
    'session': '001',
};
let PILOTING = util.getUrlParameters().has('__pilotToken');

// Start code blocks for 'Before Experiment'
// Run 'Before Experiment' code from audiobook_code
import * as pd from 'pandas';
audiobook_combinations = pd.read_csv("audiobook_combinations_probes.csv", {"header": 0, "delimiter": ","});
audiobook_questionary = pd.read_csv("audiobook_questionary.csv", {"header": 0, "delimiter": ","});

// init psychoJS:
const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([0,0,0]),
  units: 'height',
  waitBlanking: true,
  backgroundImage: '',
  backgroundFit: 'none',
});
// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); },flowScheduler, dialogCancelScheduler);

// flowScheduler gets run if the participants presses OK
flowScheduler.add(updateInfo); // add timeStamp
flowScheduler.add(experimentInit);
flowScheduler.add(InstructionsRoutineBegin());
flowScheduler.add(InstructionsRoutineEachFrame());
flowScheduler.add(InstructionsRoutineEnd());
const condition_trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(condition_trialsLoopBegin(condition_trialsLoopScheduler));
flowScheduler.add(condition_trialsLoopScheduler);
flowScheduler.add(condition_trialsLoopEnd);












flowScheduler.add(GoodByeRoutineBegin());
flowScheduler.add(GoodByeRoutineEachFrame());
flowScheduler.add(GoodByeRoutineEnd());
flowScheduler.add(quitPsychoJS, 'Thank you for your patience.', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, 'Thank you for your patience.', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // resources:
    {'name': 'conditions.xlsx', 'path': 'conditions.xlsx'},
    {'name': '../data/bip.wav', 'path': '../data/bip.wav'},
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.INFO);

async function updateInfo() {
  currentLoop = psychoJS.experiment;  // right now there are no loops
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2025.2.3';
  expInfo['OS'] = window.navigator.platform;


  // store frame rate of monitor if we can measure it successfully
  expInfo['frameRate'] = psychoJS.window.getActualFrameRate();
  if (typeof expInfo['frameRate'] !== 'undefined')
    frameDur = 1.0 / Math.round(expInfo['frameRate']);
  else
    frameDur = 1.0 / 60.0; // couldn't get a reliable measure so guess

  // add info from the URL:
  util.addInfoFromUrl(expInfo);
  

  
  psychoJS.experiment.dataFileName = (("." + "/") + `data/${expInfo["participant"]}_${expName}_${expInfo["date"]}`);
  psychoJS.experiment.field_separator = '\t';


  return Scheduler.Event.NEXT;
}

async function experimentInit() {
  // Initialize components for Routine "Instructions"
  InstructionsClock = new util.Clock();
  key_instructions = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  text_instructions = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_instructions',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: -2.0 
  });
  
  // Initialize components for Routine "ConditionPrompt"
  ConditionPromptClock = new util.Clock();
  text = new visual.TextStim({
    win: psychoJS.window,
    name: 'text',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: -1.0 
  });
  
  key_resp_prompt = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "Bips"
  BipsClock = new util.Clock();
  bip = new sound.Sound({
      win: psychoJS.window,
      value: 'A',
      secs: (- 1),
      });
  bip.setVolume(1.0);
  bip.isPlaying = false;
  bip.isFinished = false;
  fixation_bip = new visual.ShapeStim ({
    win: psychoJS.window, name: 'fixation_bip', 
    vertices: 'cross', size:[0.1, 0.1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -1, 
    interpolate: true, 
  });
  
  // Initialize components for Routine "Listening"
  ListeningClock = new util.Clock();
  audiobook = new sound.Sound({
      win: psychoJS.window,
      value: 'A',
      secs: (- 1),
      });
  audiobook.setVolume(1.0);
  audiobook.isPlaying = false;
  audiobook.isFinished = false;
  fixation_listening = new visual.ShapeStim ({
    win: psychoJS.window, name: 'fixation_listening', 
    vertices: 'cross', size:[0.1, 0.1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -2, 
    interpolate: true, 
  });
  
  // Initialize components for Routine "Questionary"
  QuestionaryClock = new util.Clock();
  key_resp_questionary = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  questionary_text = new visual.TextStim({
    win: psychoJS.window,
    name: 'questionary_text',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: -2.0 
  });
  
  // Initialize components for Routine "GoodBye"
  GoodByeClock = new util.Clock();
  final_key = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  final_text = new visual.TextStim({
    win: psychoJS.window,
    name: 'final_text',
    text: '¡Listo! Terminó el experimento\n\nGracias por participar\n\n\nApreta ESPACIO para finalizar...\n',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: -1.0 
  });
  
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}

function InstructionsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'Instructions' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    InstructionsClock.reset();
    routineTimer.reset();
    InstructionsMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from code_row_selection
    
            // add-on: list(s: string): string[]
            function list(s) {
                // if s is a string, we return a list of its characters
                if (typeof s === 'string')
                    return s.split('');
                else
                    // otherwise we return s:
                    return s;
            }
    
            import * as random from 'random';
    indices = list(util.range(8));
    Math.random.shuffle(indices);
    selected_rows = indices.slice(0, 7);
    psychoJS.experiment.addData("selected_rows", selected_rows);
    
    key_instructions.keys = undefined;
    key_instructions.rt = undefined;
    _key_instructions_allKeys = [];
    psychoJS.experiment.addData('Instructions.started', globalClock.getTime());
    InstructionsMaxDuration = null
    // keep track of which components have finished
    InstructionsComponents = [];
    InstructionsComponents.push(key_instructions);
    InstructionsComponents.push(text_instructions);
    
    for (const thisComponent of InstructionsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}

function InstructionsRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'Instructions' ---
    // get current time
    t = InstructionsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *key_instructions* updates
    if (t >= 2 && key_instructions.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_instructions.tStart = t;  // (not accounting for frame time here)
      key_instructions.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_instructions.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_instructions.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_instructions.clearEvents(); });
    }
    
    // if key_instructions is active this frame...
    if (key_instructions.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_instructions.getKeys({
        keyList: typeof 'space' === 'string' ? ['space'] : 'space', 
        waitRelease: false
      });
      _key_instructions_allKeys = _key_instructions_allKeys.concat(theseKeys);
      if (_key_instructions_allKeys.length > 0) {
        key_instructions.keys = _key_instructions_allKeys[_key_instructions_allKeys.length - 1].name;  // just the last key pressed
        key_instructions.rt = _key_instructions_allKeys[_key_instructions_allKeys.length - 1].rt;
        key_instructions.duration = _key_instructions_allKeys[_key_instructions_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *text_instructions* updates
    if (t >= 2 && text_instructions.status === PsychoJS.Status.NOT_STARTED) {
      // update params
      text_instructions.setText('En cada ensayo escucharás dos historias simultáneas (una en cada oído). Tus tareas son\n\n1) Mantenerte quieto/a y mirar la cruz central.\n\n2) Prestar atención solo a la historia indicada.\n\n3) Responder las preguntas con el teclado.\n\nPresioná ESPACIO para continuar...', false);
      // keep track of start time/frame for later
      text_instructions.tStart = t;  // (not accounting for frame time here)
      text_instructions.frameNStart = frameN;  // exact frame index
      
      text_instructions.setAutoDraw(true);
    }
    
    
    // if text_instructions is active this frame...
    if (text_instructions.status === PsychoJS.Status.STARTED) {
      // update params
      text_instructions.setText('En cada ensayo escucharás dos historias simultáneas (una en cada oído). Tus tareas son\n\n1) Mantenerte quieto/a y mirar la cruz central.\n\n2) Prestar atención solo a la historia indicada.\n\n3) Responder las preguntas con el teclado.\n\nPresioná ESPACIO para continuar...', false);
    }
    
    if (text_instructions.status === PsychoJS.Status.STARTED && Boolean((key_instructions.status == FINISHED))) {
      // keep track of stop time/frame for later
      text_instructions.tStop = t;  // not accounting for scr refresh
      text_instructions.frameNStop = frameN;  // exact frame index
      // update status
      text_instructions.status = PsychoJS.Status.FINISHED;
      text_instructions.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of InstructionsComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}

function InstructionsRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'Instructions' ---
    for (const thisComponent of InstructionsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('Instructions.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_instructions.corr, level);
    }
    psychoJS.experiment.addData('key_instructions.keys', key_instructions.keys);
    if (typeof key_instructions.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_instructions.rt', key_instructions.rt);
        psychoJS.experiment.addData('key_instructions.duration', key_instructions.duration);
        routineTimer.reset();
        }
    
    key_instructions.stop();
    // the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}

function condition_trialsLoopBegin(condition_trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    condition_trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 1, method: TrialHandler.Method.SEQUENTIAL,
      extraInfo: expInfo, originPath: undefined,
      trialList: TrialHandler.importConditions(psychoJS.serverManager, 'conditions.xlsx', selected_rows),
      seed: undefined, name: 'condition_trials'
    });
    psychoJS.experiment.addLoop(condition_trials); // add the loop to the experiment
    currentLoop = condition_trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisCondition_trial of condition_trials) {
      snapshot = condition_trials.getSnapshot();
      condition_trialsLoopScheduler.add(importConditions(snapshot));
      condition_trialsLoopScheduler.add(ConditionPromptRoutineBegin(snapshot));
      condition_trialsLoopScheduler.add(ConditionPromptRoutineEachFrame());
      condition_trialsLoopScheduler.add(ConditionPromptRoutineEnd(snapshot));
      const trialsLoopScheduler = new Scheduler(psychoJS);
      condition_trialsLoopScheduler.add(trialsLoopBegin(trialsLoopScheduler, snapshot));
      condition_trialsLoopScheduler.add(trialsLoopScheduler);
      condition_trialsLoopScheduler.add(trialsLoopEnd);
      condition_trialsLoopScheduler.add(ListeningRoutineBegin(snapshot));
      condition_trialsLoopScheduler.add(ListeningRoutineEachFrame());
      condition_trialsLoopScheduler.add(ListeningRoutineEnd(snapshot));
      const trials_2LoopScheduler = new Scheduler(psychoJS);
      condition_trialsLoopScheduler.add(trials_2LoopBegin(trials_2LoopScheduler, snapshot));
      condition_trialsLoopScheduler.add(trials_2LoopScheduler);
      condition_trialsLoopScheduler.add(trials_2LoopEnd);
      const questions_trialLoopScheduler = new Scheduler(psychoJS);
      condition_trialsLoopScheduler.add(questions_trialLoopBegin(questions_trialLoopScheduler, snapshot));
      condition_trialsLoopScheduler.add(questions_trialLoopScheduler);
      condition_trialsLoopScheduler.add(questions_trialLoopEnd);
      condition_trialsLoopScheduler.add(condition_trialsLoopEndIteration(condition_trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}

function trialsLoopBegin(trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 2, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: undefined,
      seed: undefined, name: 'trials'
    });
    psychoJS.experiment.addLoop(trials); // add the loop to the experiment
    currentLoop = trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial of trials) {
      snapshot = trials.getSnapshot();
      trialsLoopScheduler.add(importConditions(snapshot));
      trialsLoopScheduler.add(BipsRoutineBegin(snapshot));
      trialsLoopScheduler.add(BipsRoutineEachFrame());
      trialsLoopScheduler.add(BipsRoutineEnd(snapshot));
      trialsLoopScheduler.add(trialsLoopEndIteration(trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}

async function trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}

function trialsLoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      }
    return Scheduler.Event.NEXT;
    }
  };
}

function trials_2LoopBegin(trials_2LoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    trials_2 = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 2, method: TrialHandler.Method.SEQUENTIAL,
      extraInfo: expInfo, originPath: undefined,
      trialList: undefined,
      seed: undefined, name: 'trials_2'
    });
    psychoJS.experiment.addLoop(trials_2); // add the loop to the experiment
    currentLoop = trials_2;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial_2 of trials_2) {
      snapshot = trials_2.getSnapshot();
      trials_2LoopScheduler.add(importConditions(snapshot));
      trials_2LoopScheduler.add(BipsRoutineBegin(snapshot));
      trials_2LoopScheduler.add(BipsRoutineEachFrame());
      trials_2LoopScheduler.add(BipsRoutineEnd(snapshot));
      trials_2LoopScheduler.add(trials_2LoopEndIteration(trials_2LoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}

async function trials_2LoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(trials_2);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}

function trials_2LoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      }
    return Scheduler.Event.NEXT;
    }
  };
}

function questions_trialLoopBegin(questions_trialLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    questions_trial = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 3, method: TrialHandler.Method.SEQUENTIAL,
      extraInfo: expInfo, originPath: undefined,
      trialList: undefined,
      seed: undefined, name: 'questions_trial'
    });
    psychoJS.experiment.addLoop(questions_trial); // add the loop to the experiment
    currentLoop = questions_trial;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisQuestions_trial of questions_trial) {
      snapshot = questions_trial.getSnapshot();
      questions_trialLoopScheduler.add(importConditions(snapshot));
      questions_trialLoopScheduler.add(QuestionaryRoutineBegin(snapshot));
      questions_trialLoopScheduler.add(QuestionaryRoutineEachFrame());
      questions_trialLoopScheduler.add(QuestionaryRoutineEnd(snapshot));
      questions_trialLoopScheduler.add(questions_trialLoopEndIteration(questions_trialLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}

async function questions_trialLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(questions_trial);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}

function questions_trialLoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      }
    return Scheduler.Event.NEXT;
    }
  };
}

async function condition_trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(condition_trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}

function condition_trialsLoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      } else {
        psychoJS.experiment.nextEntry(snapshot);
      }
    return Scheduler.Event.NEXT;
    }
  };
}

function ConditionPromptRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'ConditionPrompt' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    ConditionPromptClock.reset();
    routineTimer.reset();
    ConditionPromptMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from prompt_code
    flecha = ((target === "Left") ? "<<<" : ">>>");
    lado = ((target === "Left") ? "IZQUIERDO" : "DERECHO");
    
    text.setText(f'''Presta atención a la historia del lado {lado} ({flecha}).
    
    
    Apretá ESPACIO para continuar...''');
    key_resp_prompt.keys = undefined;
    key_resp_prompt.rt = undefined;
    _key_resp_prompt_allKeys = [];
    psychoJS.experiment.addData('ConditionPrompt.started', globalClock.getTime());
    ConditionPromptMaxDuration = null
    // keep track of which components have finished
    ConditionPromptComponents = [];
    ConditionPromptComponents.push(text);
    ConditionPromptComponents.push(key_resp_prompt);
    
    for (const thisComponent of ConditionPromptComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}

function ConditionPromptRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'ConditionPrompt' ---
    // get current time
    t = ConditionPromptClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *text* updates
    if (t >= 0.0 && text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      text.tStart = t;  // (not accounting for frame time here)
      text.frameNStart = frameN;  // exact frame index
      
      text.setAutoDraw(true);
    }
    
    
    // if text is active this frame...
    if (text.status === PsychoJS.Status.STARTED) {
    }
    
    if (text.status === PsychoJS.Status.STARTED && Boolean((key_resp_prompt.status == FINISHED))) {
      // keep track of stop time/frame for later
      text.tStop = t;  // not accounting for scr refresh
      text.frameNStop = frameN;  // exact frame index
      // update status
      text.status = PsychoJS.Status.FINISHED;
      text.setAutoDraw(false);
    }
    
    
    // *key_resp_prompt* updates
    if (t >= 0.0 && key_resp_prompt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_resp_prompt.tStart = t;  // (not accounting for frame time here)
      key_resp_prompt.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_resp_prompt.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_resp_prompt.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_resp_prompt.clearEvents(); });
    }
    
    // if key_resp_prompt is active this frame...
    if (key_resp_prompt.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp_prompt.getKeys({
        keyList: typeof 'space' === 'string' ? ['space'] : 'space', 
        waitRelease: false
      });
      _key_resp_prompt_allKeys = _key_resp_prompt_allKeys.concat(theseKeys);
      if (_key_resp_prompt_allKeys.length > 0) {
        key_resp_prompt.keys = _key_resp_prompt_allKeys[_key_resp_prompt_allKeys.length - 1].name;  // just the last key pressed
        key_resp_prompt.rt = _key_resp_prompt_allKeys[_key_resp_prompt_allKeys.length - 1].rt;
        key_resp_prompt.duration = _key_resp_prompt_allKeys[_key_resp_prompt_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of ConditionPromptComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}

function ConditionPromptRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'ConditionPrompt' ---
    for (const thisComponent of ConditionPromptComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('ConditionPrompt.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_resp_prompt.corr, level);
    }
    psychoJS.experiment.addData('key_resp_prompt.keys', key_resp_prompt.keys);
    if (typeof key_resp_prompt.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp_prompt.rt', key_resp_prompt.rt);
        psychoJS.experiment.addData('key_resp_prompt.duration', key_resp_prompt.duration);
        routineTimer.reset();
        }
    
    key_resp_prompt.stop();
    // the Routine "ConditionPrompt" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}

function BipsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'Bips' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    BipsClock.reset();
    routineTimer.reset();
    BipsMaxDurationReached = false;
    // update component parameters for each repeat
    bip.isFinished = false;
    bip.setValue('../data/bip.wav');
    bip.setVolume(1.0);
    psychoJS.experiment.addData('Bips.started', globalClock.getTime());
    BipsMaxDuration = null
    // keep track of which components have finished
    BipsComponents = [];
    BipsComponents.push(bip);
    BipsComponents.push(fixation_bip);
    
    for (const thisComponent of BipsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}

function BipsRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'Bips' ---
    // get current time
    t = BipsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    if (bip.status === STARTED) {
        bip.isPlaying = true;
        if (t >= (bip.getDuration() + bip.tStart)) {
            bip.isFinished = true;
        }
    }
    // start/stop bip
    if (t >= 0.0 && bip.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      bip.tStart = t;  // (not accounting for frame time here)
      bip.frameNStart = frameN;  // exact frame index
      
      psychoJS.window.callOnFlip(function(){ bip.play(); });  // screen flip
      bip.status = PsychoJS.Status.STARTED;
    }
    if (bip.status === PsychoJS.Status.STARTED && Boolean(false) || bip.isFinished) {
      // keep track of stop time/frame for later
      bip.tStop = t;  // not accounting for scr refresh
      bip.frameNStop = frameN;  // exact frame index
      // update status
      bip.status = PsychoJS.Status.FINISHED;
      // stop playback
      bip.stop();
    }
    
    // *fixation_bip* updates
    if (t >= 0.0 && fixation_bip.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fixation_bip.tStart = t;  // (not accounting for frame time here)
      fixation_bip.frameNStart = frameN;  // exact frame index
      
      fixation_bip.setAutoDraw(true);
    }
    
    
    // if fixation_bip is active this frame...
    if (fixation_bip.status === PsychoJS.Status.STARTED) {
    }
    
    if (fixation_bip.status === PsychoJS.Status.STARTED && Boolean((bip.status == FINISHED))) {
      // keep track of stop time/frame for later
      fixation_bip.tStop = t;  // not accounting for scr refresh
      fixation_bip.frameNStop = frameN;  // exact frame index
      // update status
      fixation_bip.status = PsychoJS.Status.FINISHED;
      fixation_bip.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of BipsComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}

function BipsRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'Bips' ---
    for (const thisComponent of BipsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('Bips.stopped', globalClock.getTime());
    bip.stop();  // ensure sound has stopped at end of Routine
    // the Routine "Bips" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}

function ListeningRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'Listening' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    ListeningClock.reset();
    routineTimer.reset();
    ListeningMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from audiobook_code
    /* Syntax Error: Fix Python code */
    audiobook.isFinished = false;
    audiobook.setValue(audio_filepath);
    audiobook.setVolume(1.0);
    psychoJS.experiment.addData('Listening.started', globalClock.getTime());
    ListeningMaxDuration = null
    // keep track of which components have finished
    ListeningComponents = [];
    ListeningComponents.push(audiobook);
    ListeningComponents.push(fixation_listening);
    
    for (const thisComponent of ListeningComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}

function ListeningRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'Listening' ---
    // get current time
    t = ListeningClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    if (audiobook.status === STARTED) {
        audiobook.isPlaying = true;
        if (t >= (audiobook.getDuration() + audiobook.tStart)) {
            audiobook.isFinished = true;
        }
    }
    // start/stop audiobook
    if (t >= 0.0 && audiobook.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      audiobook.tStart = t;  // (not accounting for frame time here)
      audiobook.frameNStart = frameN;  // exact frame index
      
      psychoJS.window.callOnFlip(function(){ audiobook.play(); });  // screen flip
      audiobook.status = PsychoJS.Status.STARTED;
    }
    if (audiobook.status === PsychoJS.Status.STARTED && Boolean(false) || audiobook.isFinished) {
      // keep track of stop time/frame for later
      audiobook.tStop = t;  // not accounting for scr refresh
      audiobook.frameNStop = frameN;  // exact frame index
      // update status
      audiobook.status = PsychoJS.Status.FINISHED;
      // stop playback
      audiobook.stop();
    }
    
    // *fixation_listening* updates
    if (t >= 0.0 && fixation_listening.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fixation_listening.tStart = t;  // (not accounting for frame time here)
      fixation_listening.frameNStart = frameN;  // exact frame index
      
      fixation_listening.setAutoDraw(true);
    }
    
    
    // if fixation_listening is active this frame...
    if (fixation_listening.status === PsychoJS.Status.STARTED) {
    }
    
    if (fixation_listening.status === PsychoJS.Status.STARTED && Boolean((audiobook.status == FINISHED))) {
      // keep track of stop time/frame for later
      fixation_listening.tStop = t;  // not accounting for scr refresh
      fixation_listening.frameNStop = frameN;  // exact frame index
      // update status
      fixation_listening.status = PsychoJS.Status.FINISHED;
      fixation_listening.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of ListeningComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}

function ListeningRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'Listening' ---
    for (const thisComponent of ListeningComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('Listening.stopped', globalClock.getTime());
    audiobook.stop();  // ensure sound has stopped at end of Routine
    // the Routine "Listening" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}

function QuestionaryRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'Questionary' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    QuestionaryClock.reset();
    routineTimer.reset();
    QuestionaryMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from code
    /* Syntax Error: Fix Python code */
    key_resp_questionary.keys = undefined;
    key_resp_questionary.rt = undefined;
    _key_resp_questionary_allKeys = [];
    questionary_text.setText(f'''{question}
    
     A: {answer_a}
     B: {answer_b}
     C: {answer_c}
    
     Presioná la opción que creas correcta (teclas A, B ó C)''');
    psychoJS.experiment.addData('Questionary.started', globalClock.getTime());
    QuestionaryMaxDuration = null
    // keep track of which components have finished
    QuestionaryComponents = [];
    QuestionaryComponents.push(key_resp_questionary);
    QuestionaryComponents.push(questionary_text);
    
    for (const thisComponent of QuestionaryComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}

function QuestionaryRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'Questionary' ---
    // get current time
    t = QuestionaryClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *key_resp_questionary* updates
    if (t >= 0.0 && key_resp_questionary.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_resp_questionary.tStart = t;  // (not accounting for frame time here)
      key_resp_questionary.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_resp_questionary.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_resp_questionary.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_resp_questionary.clearEvents(); });
    }
    
    // if key_resp_questionary is active this frame...
    if (key_resp_questionary.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp_questionary.getKeys({
        keyList: typeof ['a','b','c'] === 'string' ? [['a','b','c']] : ['a','b','c'], 
        waitRelease: false
      });
      _key_resp_questionary_allKeys = _key_resp_questionary_allKeys.concat(theseKeys);
      if (_key_resp_questionary_allKeys.length > 0) {
        key_resp_questionary.keys = _key_resp_questionary_allKeys[_key_resp_questionary_allKeys.length - 1].name;  // just the last key pressed
        key_resp_questionary.rt = _key_resp_questionary_allKeys[_key_resp_questionary_allKeys.length - 1].rt;
        key_resp_questionary.duration = _key_resp_questionary_allKeys[_key_resp_questionary_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *questionary_text* updates
    if (t >= 0.0 && questionary_text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      questionary_text.tStart = t;  // (not accounting for frame time here)
      questionary_text.frameNStart = frameN;  // exact frame index
      
      questionary_text.setAutoDraw(true);
    }
    
    
    // if questionary_text is active this frame...
    if (questionary_text.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + (key_resp_questionary.status == FINISHED) - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (questionary_text.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      questionary_text.tStop = t;  // not accounting for scr refresh
      questionary_text.frameNStop = frameN;  // exact frame index
      // update status
      questionary_text.status = PsychoJS.Status.FINISHED;
      questionary_text.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of QuestionaryComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}

function QuestionaryRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'Questionary' ---
    for (const thisComponent of QuestionaryComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('Questionary.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_resp_questionary.corr, level);
    }
    psychoJS.experiment.addData('key_resp_questionary.keys', key_resp_questionary.keys);
    if (typeof key_resp_questionary.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp_questionary.rt', key_resp_questionary.rt);
        psychoJS.experiment.addData('key_resp_questionary.duration', key_resp_questionary.duration);
        routineTimer.reset();
        }
    
    key_resp_questionary.stop();
    // the Routine "Questionary" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}

function GoodByeRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'GoodBye' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    GoodByeClock.reset();
    routineTimer.reset();
    GoodByeMaxDurationReached = false;
    // update component parameters for each repeat
    final_key.keys = undefined;
    final_key.rt = undefined;
    _final_key_allKeys = [];
    psychoJS.experiment.addData('GoodBye.started', globalClock.getTime());
    GoodByeMaxDuration = null
    // keep track of which components have finished
    GoodByeComponents = [];
    GoodByeComponents.push(final_key);
    GoodByeComponents.push(final_text);
    
    for (const thisComponent of GoodByeComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}

function GoodByeRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'GoodBye' ---
    // get current time
    t = GoodByeClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *final_key* updates
    if (t >= 0.0 && final_key.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      final_key.tStart = t;  // (not accounting for frame time here)
      final_key.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { final_key.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { final_key.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { final_key.clearEvents(); });
    }
    
    // if final_key is active this frame...
    if (final_key.status === PsychoJS.Status.STARTED) {
      let theseKeys = final_key.getKeys({
        keyList: typeof 'space' === 'string' ? ['space'] : 'space', 
        waitRelease: false
      });
      _final_key_allKeys = _final_key_allKeys.concat(theseKeys);
      if (_final_key_allKeys.length > 0) {
        final_key.keys = _final_key_allKeys[_final_key_allKeys.length - 1].name;  // just the last key pressed
        final_key.rt = _final_key_allKeys[_final_key_allKeys.length - 1].rt;
        final_key.duration = _final_key_allKeys[_final_key_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *final_text* updates
    if (t >= 0.0 && final_text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      final_text.tStart = t;  // (not accounting for frame time here)
      final_text.frameNStart = frameN;  // exact frame index
      
      final_text.setAutoDraw(true);
    }
    
    
    // if final_text is active this frame...
    if (final_text.status === PsychoJS.Status.STARTED) {
    }
    
    if (final_text.status === PsychoJS.Status.STARTED && Boolean((final_key.status == FINISHED))) {
      // keep track of stop time/frame for later
      final_text.tStop = t;  // not accounting for scr refresh
      final_text.frameNStop = frameN;  // exact frame index
      // update status
      final_text.status = PsychoJS.Status.FINISHED;
      final_text.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of GoodByeComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}

function GoodByeRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'GoodBye' ---
    for (const thisComponent of GoodByeComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('GoodBye.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(final_key.corr, level);
    }
    psychoJS.experiment.addData('final_key.keys', final_key.keys);
    if (typeof final_key.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('final_key.rt', final_key.rt);
        psychoJS.experiment.addData('final_key.duration', final_key.duration);
        routineTimer.reset();
        }
    
    final_key.stop();
    // the Routine "GoodBye" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}

function importConditions(currentLoop) {
  return async function () {
    psychoJS.importAttributes(currentLoop.getCurrentTrial());
    return Scheduler.Event.NEXT;
    };
}

async function quitPsychoJS(message, isCompleted) {
  // Check for and save orphaned data
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});
  
  return Scheduler.Event.QUIT;
}
