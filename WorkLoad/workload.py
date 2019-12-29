workstation1 = []
workstation2 = []
workstation3 = []


def main():
    time = 0
    allJobs = []
    timeStack = []
    n = int(input())
    seq = []
    for i in range(n):
        seq.append([0, 0, 0])
    for i in range(n):
        x = input()
        splited = x.split()
        a = {'id': i, 'entrance_time': int(splited[0]), 'time1': int(splited[1]), 'time2': int(splited[2]),
             'time3': int(splited[3]),
             'lock': False}
        allJobs.append(a)
    w1 = allJobs.copy()
    w2 = allJobs.copy()
    w3 = allJobs.copy()

    # t1, index1 = min((d['time1'], d['id']) for d in w1 if d['lock'] == False and d['entrance_time'] <= time)
    # w1[index1]['lock'] = True
    # t2, index2 = min((d['time2'], d['id']) for d in w2 if d['lock'] == False and d['entrance_time'] <= time)
    # w2[index2]['lock'] = True
    # t3, index3 = min((d['time3'], d['id']) for d in w3 if d['lock'] == False and d['entrance_time'] <= time)
    # w3[index3]['lock'] = True

    # 111111111111111111111111111111
    try:
        t3, index3 = min((d['time3'], d['id']) for d in w3 if d['lock'] == False and d['entrance_time'] <= time)
        a3 = {'time': time + t3, 'index': index3, 'station': 3, 'place': 2}
        allJobs[index3]['lock'] = True
    except:
        a3 = {'time': time + 1, 'index': -1, 'station': 3, 'place': 3}
    try:
        t2, index2 = min((d['time2'], d['id']) for d in w2 if d['lock'] == False and d['entrance_time'] <= time)
        a2 = {'time': time + t2, 'index': index2, 'station': 2, 'place': 3}
        allJobs[index2]['lock'] = True
    except:
        a2 = {'time': time + 1, 'index': -1, 'station': 2, 'place': 2}
    try:
        t1, index1 = min((d['time1'], d['id']) for d in w1 if d['lock'] == False and d['entrance_time'] <= time)
        a1 = {'time': time + t1, 'index': index1, 'station': 1, 'place': 1}
        allJobs[index1]['lock'] = True
    except:
        a1 = {'time': time + 1, 'index': -1, 'station': 1, 'place': 1}



    # #1111111111111
    # timeStack.append(a1)
    # timeStack.append(a2)
    # timeStack.append(a3)
    #
    #
    # #222222222222222
    timeStack.append(a1)
    timeStack.append(a2)
    timeStack.append(a3)
    #
    # #3333333333333333
    # timeStack.append(a2)
    # timeStack.append(a1)
    # timeStack.append(a3)
    #
    # #4444444444444444
    # timeStack.append(a3)
    # timeStack.append(a1)
    # timeStack.append(a2)
    #
    # #5555555555555555
    # timeStack.append(a3)
    # timeStack.append(a2)
    # timeStack.append(a1)
    #
    # #66666666666666666
    # timeStack.append(a2)
    # timeStack.append(a3)
    # timeStack.append(a1)

    timeStack = sorted(timeStack, key=lambda i: (i['time'], i['place']))
    while w1.__len__() > 0 or w2.__len__() > 0 or w3.__len__() > 0:
        x = timeStack.pop(0)
        timeStack[0]['place'] = timeStack[0]['place'] - 1
        timeStack[1]['place'] = timeStack[1]['place'] - 1
        time = x['time']
        if x['index'] != -1:
            allJobs[x['index']]['lock'] = False
            seq[x['index']][x['station'] - 1] = time - allJobs[x['index']]['time' + str(x['station'])]
        if x['station'] == 1:
            if x['index'] != -1:
                for i in w1:
                    if i['id'] == x['index']:
                        w1.remove(i)
                        break
            try:
                t1, index1 = min((d['time1'], d['id']) for d in w1 if d['lock'] == False and d['entrance_time'] <= time)
                a1 = {'time': time + t1, 'index': index1, 'station': 1, 'place': 3}
                allJobs[index1]['lock'] = True
            except:
                a1 = {'time': time + 1, 'index': -1, 'station': 1, 'place': 3}
            timeStack.append(a1)
        if x['station'] == 2:
            if x['index'] != -1:
                for i in w2:
                    if i['id'] == x['index']:
                        w2.remove(i)
                        break
            try:
                t2, index2 = min((d['time2'], d['id']) for d in w2 if d['lock'] == False and d['entrance_time'] <= time)
                a2 = {'time': time + t2, 'index': index2, 'station': 2, 'place': 3}
                allJobs[index2]['lock'] = True
            except:
                a2 = {'time': time + 1, 'index': -1, 'station': 2, 'place': 3}
            timeStack.append(a2)
        if x['station'] == 3:
            if x['index'] != -1:
                for i in w3:
                    if i['id'] == x['index']:
                        w3.remove(i)
                        break
            try:
                t3, index3 = min((d['time3'], d['id']) for d in w3 if d['lock'] == False and d['entrance_time'] <= time)
                a3 = {'time': time + t3, 'index': index3, 'station': 3, 'place': 3}
                allJobs[index3]['lock'] = True
            except:
                a3 = {'time': time + 1, 'index': -1, 'station': 3, 'place': 3}
            timeStack.append(a3)
        timeStack = sorted(timeStack, key=lambda i: (i['time'], i['place']))
    print(time)
    for i in seq:
        print(str(i[0]) + " " + str(i[1]) + " " + str(i[2]))


if __name__ == '__main__':
    main()
