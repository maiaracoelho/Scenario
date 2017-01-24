import os
from datetime import datetime
import shutil
import os.path

now = datetime.now()
date_hour = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

path_logs = "/home/berg/codigos/app/log.txt"
path_file = "/home/berg/codigos/app/"
path_destiny = "/var/www/html/public/log"

class DirectoryManager():

    def __init__(self):
        pass

    def create(self, label, path):
        try:
            p = path + '/' + label+ '/' + str(now.year) + '/' + str(now.month) + '/' + str(now.day)
            os.makedirs(p)
            print ("Create sucessfull")
        except OSError:
            print("Error")

        return p

    def createAllLogs(self, p, label, value):
        text = []
        if os.path.isfile(p +"/" + label):
            file = open(p +"/" + label, 'r')
            text = file.readlines()
            text.append("\n" + value)
        else: text.append(value)
        arq = open(p + "/" + label, "w")
        arq.write(''.join(text))
        arq.close()

    def move(self, source, destiny):
        shutil.move(source, destiny)
        return destiny

    def renameFile(self, label, path_dir):
        destiny = path_file + label + '_' + date_hour
        os.rename(path_logs, destiny)
        self.move(destiny, path_dir)
        self.createAllLogs(path_dir, "list_log.txt", label + '_' + date_hour)


dir = DirectoryManager()  # New Object DirectoryManager
path_dir = dir.create("Equipe01", path_destiny)  # new folder or directory
print(path_dir)
dir.renameFile("Equipe01", path_dir)  # rename log file and return you path

