#! /usr/local/bin/python
from __future__ import print_function
import subprocess
import time
import sys


#from DirectoryManager import DirectoryManager
#from MetricsSession import MetricsSession

path_log = open(sys.argv[1], "w")
path_file = "/home/dash/git/Scenario/scen/bw_fluctation_tim_rio_meanBw.txt"
path_tc = '/home/dash/git/Scenario/tc.bash'
file = open(path_file, "r")
section_in_seconds = 900

def run(index):
    scenario_lst = Scenario(file)

    for i, obj in enumerate(scenario_lst.lst[index:]):

	time1 = time.time()
	path_log.write(str(time1) + " " + str(obj.rate) + "\n")
        if not scenario_lst.run:

            subprocess.call(['sudo', '-S', path_tc, 'start', 'UP:' + obj.rate + "kbit"])
            scenario_lst.run = True
        else:

            subprocess.call(['sudo', '-S', path_tc, 'update', 'UP:' + obj.rate + "kbit"])

        sleep = obj.seconds - obj.seconds_prev
        time.sleep(sleep)
        print("Sleep of " + str(sleep) + " seconds of " + str(i+1) + " to speed of " + obj.rate + " UP kbit")
        sys.stdout.flush()
    path_log.close()
    subprocess.call(['sudo', '-S', path_tc, 'stop'])
    subprocess.call(['sudo', '-S', path_tc, 'show'])

    print("Finish...")


#def processingAfterEnd(scenario_lst):
 #   dir = DirectoryManager()  # New Object DirectoryManager
  #  path_dir = dir.create(team_name, dir.path_destiny)  # new folder or directory
  #  path_file_rename = dir.renameFile(team_name)  # rename log file and return you path
  #  return dir.move(path_file_rename, path_dir)  # move log file to folder path and return you new path

class Data():

    def __init__(self, hour, seconds, rate, seconds_prev):
        self.hour = str(hour)
        self.seconds = long(seconds)
        self.rate = str(rate)
        self.seconds_prev = long(seconds_prev)

    def printData(self):
        print(str(self.hour) + ' ' + str(self.seconds) + ' ' + str(self.rate))

    def split(self):
        return [self.hour, self.seconds, self.rate]

class Scenario():
    lst = []

    def __init__(self, file):
        self.read(file)
        self.run = False

    def read(self, file):
        prev = -1
        for line in file:
            line = line.strip().split()
            self.lst.append(Data(line[0], line[1], line[2], prev))
            prev = line[1]

index = raw_input("Insira inicio: ")
run(long(index))
