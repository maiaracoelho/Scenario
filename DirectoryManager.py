import os
from datetime import datetime
import shutil
import os.path
import json

now = datetime.now()
date_hour = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

path_logs = "/home/berg/codigos/app/log.txt"
path_file = "/home/berg/codigos/app/Logs/"
path_destiny = "/var/www/html/public/log"

class DirectoryManager():

    def __init__(self):
        pass

    def create(self, path):
        lst = self.getAllFiles()
        print (lst)

        for obj in lst:
            j = json.loads(open(path_file+str(obj)).read())
            try:
                date = self.formatDate(str(j['date']))
                print (date)
                p = path + '/' + j['team'] + '/' + date[0] + '/' + date[1] + '/' + date[2]
                os.makedirs(p)
                print ("Create sucessfull")
                self.renameFile(j['team'], p, str(obj))
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

    def renameFile(self, labelTeam, path_dir, fileName):
        destiny = path_file + labelTeam + '_' + date_hour
        os.rename(path_file + fileName, destiny)
        self.move(destiny, path_dir)
        self.createAllLogs(path_dir, "list_log.txt", labelTeam + '_' + date_hour)

    def getAllFiles(self):
        l = []
        for _, _, arquivo in os.walk(path_file):
            l = arquivo
        return l


    def moveAllFiles(self, path_dir):
        lst = self.getAllFiles()
        for i in lst:
            json = json.loads(open(path_file+i).read())
            self.renameFile(json['team'], path_dir, str(i))

    def formatDate(self, date):
        date  = date.split('-')
        return date

dir = DirectoryManager()  # New Object DirectoryManager
dir.create(path_destiny)
# dir.getAllFiles()
# path_dir = dir.create("Equipe01", path_destiny)  # new folder or directory
# print(path_dir)
# dir.renameFile("Equipe01", path_dir)  # rename log file and return you path

