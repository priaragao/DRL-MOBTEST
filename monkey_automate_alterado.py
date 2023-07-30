#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 23:31:39 2020

@author: indtusuario
"""
from uiautomator import Device
import numpy as np
import time
import timeit
import urllib3

import torchvision.transforms as T
from PIL import Image
from scipy import misc

import pandas as pd

import torch

from collections import namedtuple

import sys
import os
os.environ['LD_LIBRARY_PATH']='/usr/local/lib' #changed by Equipe2
import math
import random
import numpy as np
from collections import namedtuple
from itertools import count
from copy import deepcopy
from PIL import Image
from matplotlib.pyplot import imread

import string
import time
import shutil
import torch
import torch.nn as nn
import torch.optim as optim
import torch.autograd as autograd
import torch.nn.functional as F
import torchvision.transforms as T
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter()

import subprocess
from subprocess import Popen, PIPE
from subprocess import call
from collections import deque

from torch.autograd import Variable
import logging

FNULL = open(os.devnull, 'w')
PROJECT_ROOT = "/home/iartes/monkey_script" #changed by Equipe2
APP_UNDER_TEST_ROOT = "/home/iartes/monkey_script/Experiments/wallpaper/" #changed by Equipe2
http_client = urllib3.PoolManager()

#compile_reporter = "javac -cp lib/org.jacoco.ant-0.8.5-nodeps.jar:. ReportGenerator.java"
#logging.basicConfig(filename='tmp.log',
 #                   format='%(levelname)s %(asctime)s :: %(message)s',
  #                  level=logging.DEBUG)
app_package = "com.google.android.wallpaper" #changed by Equipe2
d = Device()

call(f"ng ng-cp {PROJECT_ROOT}lib/org.jacoco.ant-0.8.5-nodeps.jar", shell=True, stdout=FNULL)
call(f"ng ng-cp {PROJECT_ROOT}", shell=True, stdout=FNULL)
call(f"adb forward tcp:8981 tcp:8981", shell=True, stdout=FNULL)

def reset():
    call(f"adb  shell am force-stop {app_package}", shell=True, stdout=FNULL)
    call(f"adb shell pm clear {app_package}", shell=True, stdout=FNULL)
    call(f"adb shell monkey -p {app_package} 1", shell=True, stdout=FNULL)  

def get_screen():
        d.screenshot("state.png")
        timestr = time.strftime("%Y%m%d-%H%M%S")
        shutil.copy("state.png","states/state_"+timestr+".png")
       # img = imread("state.png")
    
def run():
    cont = 1
    line =0
    while cont <100000:
        previous_line = get_lines()
        call(f"adb shell monkey -p {app_package} --pct-touch 95 -v {cont} > log.txt", shell=True, stdout=FNULL)
        get_screen()
        get_crash()
        line = get_lines()
        #coverage = get_coverage()
        #print("Coverage: ",coverage)
        if previous_line <line:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            #shutil.copy("coverage/coverage.exec","coverage_"+timestr+".exec")
            #shutil.copy("report.csv","report_"+timestr+".csv")
            reset()
        previous_line = line
        #coverage, crash =_get_current_coverage()
 #       if crash == True:
#            reset()
        cont = cont + 1
#        print("Coverage: ",coverage)
#        logging.debug("coverage:")
#        logging.debug(coverage)
    
def _get_current_coverage():
    start_time = timeit.default_timer()
    try:
        with http_client.request("GET", "http://192.168.0.6:8981", preload_content=False) as r, open('coverage.exec', "wb") as coverage_file:
            coverage_file.write(r.read())
        generate_report_cmd = f'java -cp lib/org.jacoco.ant-0.8.5-nodeps.jar:. ReportGenerator "{APP_UNDER_TEST_ROOT}"'
        call(generate_report_cmd, shell=True, stdout=FNULL)
        crash = False
    except:
        print("Not connected")
        crash = True
        timestr = time.strftime("%Y%m%d-%H%M%S")
        shutil.copy("coverage.exec","coverage_"+timestr+".exec")
    df = pd.read_csv("report.csv")
    missed, covered = df[['LINE_MISSED', 'LINE_COVERED']].sum()
    print(f"Complete in {timeit.default_timer() - start_time} seconds")
    logging.debug(f"Complete in {timeit.default_timer() - start_time} seconds")
    return covered / (missed + covered), crash


def get_coverage():
    start_time = timeit.default_timer()
    call(f"adb pull /sdcard/coverage /home/indtusuario/Experiments/monkey/", shell=True, stdout=FNULL)  
    generate_report_cmd = f'java -cp lib/org.jacoco.ant-0.8.5-nodeps.jar:. ReportGenerator "{APP_UNDER_TEST_ROOT}"'
    call(generate_report_cmd, shell=True, stdout=FNULL)
    df = pd.read_csv("report.csv")
    missed, covered = df[['LINE_MISSED', 'LINE_COVERED']].sum()
    print(f"Complete in {timeit.default_timer() - start_time} seconds")
    logging.debug(f"Complete in {timeit.default_timer() - start_time} seconds")
    return covered / (missed + covered)

def get_crash():
    #comand ="adb shell logcat | grep 'Unable to start activity ComponentInfo{protect.budgetwatch/protect.budgetwatch.MainActivity}'> std.txt"
    try:
        call(f"adb shell logcat -d | grep 'Unable to start activity ComponentInfo'> std.txt", shell=True, stdout=FNULL)  
    except:
        print("Not copied")
    
    
def get_lines():
    with open('std.txt') as f:
        line_count = 0
        for line in f:
            line_count += 1
        
    return line_count

run()


