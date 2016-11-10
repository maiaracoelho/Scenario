#! /usr/local/bin/python
import subprocess
import time

path_file = "/home/berg/Documentos/Cenarios/input_file.txt"
path_tc = '/home/berg/tc.bash'

file = open(path_file, "r")
flag = -1

print "Starting simulation to test"

for line in file:
    line = line.split() #Posicoes na lista: 1 = sleep; 3 = upload; 5 = delay;
    print "Sleep de " + line[1] + " seconds to reduce speed to " + line[3] + " with delay of " + line[5]
    time.sleep(int(line[1]))

    if flag == -1:
        flag = 0
        subprocess.call(['sudo', '-S', path_tc,'start', line[3], line[5]])
    else: subprocess.call(['sudo', '-S', path_tc, 'update', line[3], line[5]])

subprocess.call(['sudo', '-S', path_tc,'stop'])
print "finish...."

