#! /usr/local/bin/python
import subprocess
import time

path_file = "/home/berg/PycharmProjects/Scripts/bw_fluctuation_claro_mao_evening_AVBW.txt"
path_tc = '/home/berg/PycharmProjects/Scripts/tc.bash'

file = open(path_file, "r")
flag = -1
linePrevious = file.readline().split()

print "Starting simulation to test"

for line in file:
    line = line.split()

    if flag == -1:
        flag = 0
        subprocess.call(['sudo', '-S', path_tc, 'start', 'UP:' + linePrevious[2] + "kbit"])
    else:
        subprocess.call(['sudo', '-S', path_tc, 'update', 'UP:' + linePrevious[2] + "kbit"])

    sleep_time = long(line[1]) - long(linePrevious[1])
    linePrevious = line
    #if linePrevious[1] >= 900: break # secao de 15 minutos

    print "Sleep of", sleep_time, "seconds to speed of", linePrevious[2], "UP kbit"
    time.sleep(sleep_time)


subprocess.call(['sudo', '-S', path_tc,'stop'])
subprocess.call(['sudo', '-S', path_tc,'show'])

print "finish..."