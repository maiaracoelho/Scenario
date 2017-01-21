# coding=utf-8
import json

path_json = "/home/berg/Dropbox/Integração Note_Cel_Desktop/example_json.txt"
input_file = open(path_json).read()
n_sharing = 3

class MetricsSession():

    def __init__(self, averageBandwidthScenario, path_json):
        self.averageBandwidthScenario = long(averageBandwidthScenario)
        self.path_json = str(path_json)

    def strToJson(self, str):
        return json.loads(str)

    def averageBitrate(self):
        j = self.strToJson(input_file)
        lst_chunk = j['chunk']

        sum1 = sum([lst_chunk[i]['bitrate'] * (lst_chunk[i]['duration'] / 1000) for i, obj in enumerate(lst_chunk)])
        return sum1 / j['session_time']

    def justice(self):
        r_obtained = self.averageBitrate()
        r_expected = None

    def instability(self):
        pass

    def expectedResult(self, averageVideosRate, n_clients):
        pass

    def averageInterruptions(self):
        lst_interruptions = self.strToJson(input_file)['interruptions']

        sum1 = sum(
            [lst_interruptions[i]['end'] - lst_interruptions[i]['start'] for i, obg in enumerate(lst_interruptions)])
        return sum1 / len(lst_interruptions)

