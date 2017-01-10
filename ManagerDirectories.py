import os
from datetime import datetime
import shutil


now = datetime.now()
date_hour = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

path_logs = "/home/berg/codigos/app/log.txt"
path_file = "/home/berg/codigos/app/"
path_destiny = "/home/berg/Documentos/Logs"

class DirectoryManager():

    def __init__(self):
        pass

    def create(self, label, path):
        try:
            p = path + '/' + str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/' + label
            os.makedirs(p)
            print "Create sucessfull"
            return p
        except OSError:
            print "Error"

        return None

    def move(self, source, destiny):
        shutil.move(source, destiny)

    def renameFile(self, label):
        destiny = path_file + label + '_' + date_hour
        os.rename(path_logs, path_file + label + '_' + date_hour)
        return destiny


dir = DirectoryManager()

e = "Equipe02"
path_dir = dir.create(e, path_destiny)
path_file_rename = dir.renameFile(e)
dir.move(path_file_rename, path_dir)