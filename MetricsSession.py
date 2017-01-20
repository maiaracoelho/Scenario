import json

path_json = "/home/berg/Documentos/Logs/2017/1/10/json_example"
input_file = open(path_json).read()
n_sharing = 3

def strToJson(str):
    return json.loads(str)

def averageBitrate():
    lst_chunk = strToJson(input_file)['chunkDuration']

    sum1 = sum([lst_chunk[i]['bitrate'] * (lst_chunk[i]['duration'] / 1000) for i, obj in enumerate(lst_chunk)])
    return sum1 # / tempo_sessao

def justice():
    r_obtained = averageBitrate()
    r_expected = None

    pass

def instability():
    pass

def expectedResult(averageVideosRate, n_clients):
    pass

print averageBitrate()

#lst = j["interruptions"]
#print (json.dumps(a, indent=1))
