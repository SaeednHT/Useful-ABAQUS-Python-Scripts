# ==============================================================================================
# **********************************************************************************************
# ************************                   INA                        ************************
# ************************            Useful Python Scripts             ************************
# ************************                By: SaeednHT                  ************************
# **********************************************************************************************

import os, sys
import subprocess
import time
import glob
from itertools import cycle
import win32api

# Check if .lck file exists (other jobs are running)
while glob.glob('*.lck'):
    print >> sys.__stdout__, '****'
    # for i in cycle(["|", "/", "-", "\\ ", ".", " . ", "  .", " . ",".  ", " . ", "  .","    "]):
    for i in cycle(["*      ",">*     ", ">>*    ", ">>>*   ", ">>>>*  ", ">>>>>* ","     *", "    *<", "   *<<", "  *<<<", " *<<<<", "*<<<<<","*      "]):
        if glob.glob('*.lck'):
            print ('Previous jobs are runnig. Please wait.  ',i,end='\r') # '\r' clears the previous output
            time.sleep(0.9)
        else:
            break
    print >> sys.__stdout__, '\n'
    print >> sys.__stdout__, '****'

# **********************************************************************************************
# Submit inputfiles (.inp)
timeout = 12 * 60 * 60 # 12 hour(s) time is given to be completed, otherwise it stops the job forcefully
def run_command(cmd, timeout):
    start_time = time.time()
    df = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while timeout and df.poll() == None:
        if time.time()-start_time >= timeout:
            df.terminate()
            try:
                subprocess.Popen('TASKKILL /F /IM standard.exe')
            except:
                pass
            try:
                subprocess.Popen('TASKKILL /F /IM pre.exe', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except:
                pass

# Submit Jobs (job1-name, job2-name) in queue
try:
    Job = 'job1-name'
    strCommandLine = 'abaqus' + ' job=' + Job + ' input=' + Job + '.inp' + ' interactive cpus=7 gpus=1'
    print >> sys.__stdout__, '--------------------------------------------------- ' + Job + ' ---------------------------------------------------'
    try:
        run_command(strCommandLine, timeout)
    except:
        pass

    # Check system inactivity and move mouse if it has been inactive for more than 20 minutes.
    last_active = win32api.GetLastInputInfo()
    now = win32api.GetTickCount()
    elapsed_milliseconds = (now - last_active)
    elapsed_minutes = (float(elapsed_milliseconds)/1000)/60
    print >> sys.__stdout__, 'Minutes of inactivity = ',elapsed_minutes
    if (elapsed_minutes-20) > 1e-3:
        print >> sys.__stdout__, 'Moving Mouse'
        strCommandLine = 'call mouse_control moveBy 200x200'
        subprocess.call(strCommandLine, shell=True)
    
    Job = 'job2-name'
    strCommandLine = 'abaqus' + ' job=' + Job + ' input=' + Job + '.inp' + ' interactive cpus=7 gpus=1'
    print >> sys.__stdout__, '--------------------------------------------------- ' + Job + ' ---------------------------------------------------'
    try:
        run_command(strCommandLine, timeout)
    except:
        pass
except:
    pass


# **********************************************************************************************
# Check if a job is completed successfully
def check_complete(name):
    try:
        # read sta file
        sta_file = os.getcwd()+'\\'+name+'.sta'
        
        with open(sta_file, 'r') as file:
            data = file.readlines()
        
        if 'HAS COMPLETED SUCCESSFULLY' in data[-1]:
            complete = 'True :)'  
        else:
            complete = 'False!'
    except:
        complete = 'False (Job does not contain status file!)'
        pass
    return complete

# **********************************************************************************************
# Check if a job contains NaN
def check_NaN(name):
    try:
        # read msg file
        msg_file = os.getcwd()+'\\'+name+'.msg'
        with open(msg_file, 'r') as file:
            data = file.read()
        if 'NaN' in data:
            NaN_output = 'Job Contains NaN. Find the problem!'
        else:
            NaN_output = 'No NaN found. Perfect :)'
    except:
        NaN_output = 'Job does not contain massage file!'
    return NaN_output

# **********************************************************************************************
# Shut down windows
os.system('shutdown -s')