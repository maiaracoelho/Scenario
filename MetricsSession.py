# coding=utf-8
import json

path_json = "/home/berg/Dropbox/Integração Note_Cel_Desktop/example_json.txt"
input_file = open(path_json).read()
n_sharing = 3

class MetricsSession():

    def __init__(self, averageBandwidthScenario, path_log):
        self.averageBandwidthScenario = long(averageBandwidthScenario)
        self.path_log = str(path_log)

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

        sum1 = sum([r_obtained / r_expected for i in range(1, n_sharing+1)]) ** 2
        sum2 = [(r_obtained / r_expected) ** 2 for i in range(1, n_sharing+1)]

        return sum1 / sum2

    def instability(self):
        lst_chunk = self.strToJson(input_file)['chunk']

        sum1 = sum([abs(lst_chunk[i]['bitrate'] - lst_chunk[i-1]['bitrate'] * i+2) for i, obj in enumerate(lst_chunk)
                    if i-1 >= 0 and i < len(lst_chunk)-1])
        sum2 = sum([lst_chunk[i]['bitrate'] * i for i, obj in enumerate(lst_chunk) if i > 1])

        return sum1 / sum2

    def expectedResult(self, averageVideosRate, n_clients):
        pass

    def averageInterruptions(self):
        lst_interruptions = self.strToJson(input_file)['interruptions']

        sum1 = sum([lst_interruptions[i]['end'] - lst_interruptions[i]['start'] for i, obg in enumerate(lst_interruptions)])
        return sum1 / len(lst_interruptions)

m = MetricsSession(0, "")
print(m.instability())