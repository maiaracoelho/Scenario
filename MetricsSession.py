# coding=utf-8
import json

path_json = "/home/berg/Dropbox/Integração Note_Cel_Desktop/example_json.txt"
input_file = json.loads(open(path_json).read()) #Json
n_sharing = 3 # Number of clients

class MetricsSession():

    def __init__(self, averageBandwidthScenario, path_log):
        self.averageBandwidthScenario = long(averageBandwidthScenario)
        self.path_log = str(path_log)


    def averageBandwidth(self):
        lst_bandwidth = input_file['bandwidth']
        return sum([lst_bandwidth[i]['bandwidth'] for i, obj in enumerate(lst_bandwidth)]) / len(lst_bandwidth)

    def averageBitrate(self):
        j = input_file
        lst_chunk = j['chunk']

        sum1 = sum([lst_chunk[i]['bitrate'] * (lst_chunk[i]['duration'] / 1000) for i, obj in enumerate(lst_chunk)])
        return sum1 / (j['session_time'] / 1000)

    def justice(self):
        r_obtained = self.averageBitrate()
        r_expected = r_expected()

        sum1 = sum([r_obtained / r_expected for i in range(0, n_sharing)]) ** 2
        sum2 = sum([(r_obtained / r_expected) ** 2 for i in range(0, n_sharing)])

        return sum1 / sum2

    def instability(self):
        lst_chunk = input_file['chunk']

        sum1 = sum([abs(lst_chunk[i]['bitrate'] - lst_chunk[i-1]['bitrate'] * len(lst_chunk) - i) for i, obj in enumerate(lst_chunk)
                    if i-1 >= 0 and i < len(lst_chunk)-1])
        sum2 = sum([lst_chunk[i]['bitrate'] * len(lst_chunk) - i for i, obj in enumerate(lst_chunk[1:])])

        return float(sum1) / float(sum2)

    def r_expected(self):
        lst_qualities = input_file['qualities']
        averageQualities = sum([lst_qualities[i]['width'] for i, obj in enumerate(lst_qualities)]) / len(lst_qualities)
        return (averageQualities / n_sharing) * self.averageBandwidth()

    def averageInterruptions(self):
        lst_interruptions = input_file['interruption']

        sum1 = sum([lst_interruptions[i]['end'] - lst_interruptions[i]['start'] for i, obg in enumerate(lst_interruptions)])
        return sum1 / len(lst_interruptions)

m = MetricsSession(0, "")
print(m.r_expected())