import os
from copy import deepcopy


def avg_(A: list, clipping=(0, 0)):
    if len(A[clipping[0]:]) != 0:
        A = A[clipping[0]:]
    if len(A[:(len(A) - clipping[1])]) != 0:
        A = A[:(len(A) - clipping[1])]
    return sum(A) / len(A)


def med_(A: list, clipping=(0, 0)):
    if len(A[clipping[0]:]) != 0:
        A = A[clipping[0]:]
    if len(A[:(len(A) - clipping[1])]) != 0:
        A = A[:(len(A) - clipping[1])]
    len_ = len(A)
    if len_ % 2 == 0:
        tmp_A = sorted(A)
        return (tmp_A[len_ // 2 - 1] + tmp_A[len_ // 2]) / 2
    else:
        return sorted(A)[len_ // 2]


def min_(A: list, clipping=(0, 0)):
    if len(A[clipping[0]:]) != 0:
        A = A[clipping[0]:]
    if len(A[:(len(A) - clipping[1])]) != 0:
        A = A[:(len(A) - clipping[1])]
    return sorted(A)[0]


def max_(A: list, clipping=(0, 0)):
    if len(A[clipping[0]:]) != 0:
        A = A[clipping[0]:]
    if len(A[:(len(A) - clipping[1])]) != 0:
        A = A[:(len(A) - clipping[1])]
    return sorted(A, reverse=True)[0]


def nin_(A: list, clipping=(0, 0)):
    if len(A[clipping[0]:]) != 0:
        A = A[clipping[0]:]
    if len(A[:(len(A) - clipping[1])]) != 0:
        A = A[:(len(A) - clipping[1])]
    idx = int(len(A) * 0.99)
    if (idx == (len(A) - 1)) and (idx > 0):
        idx -= 1
    return sorted(A)[idx]


if __name__ == "__main__":
    BASE_PATH = './res'
    files = os.listdir(BASE_PATH)
    try:
        files.remove('.DS_Store')
    except:
        pass
    try:
        files.remove('analysis.py')
    except:
        pass
    # print(files)

    data = []
    for file_name in files:
        if "debug" in file_name:
            pass
        elif "latency" in file_name:
            pass
        else:
            data.append(file_name)
    # print(data)
    data = sorted(data)

    dict_time = {}
    for file_name in data:
        times = []
        with open(BASE_PATH + '/' + file_name, 'r') as f:
            remove_first_N = 1  # logs

            lines = f.readlines()
            lines = lines[remove_first_N:]

            clipping = (10, 10)  # first and last values
            lines = lines[clipping[0]:(len(lines) - clipping[1])]

            for idx, line in enumerate(lines):
                time = line.split()[0]
                ret = line.split()[1]
                if ret == "b''":
                    continue
                times.append(float(time))

        clipping = (2, 2)  # outliers
        times = sorted(times)[clipping[0]:(len(times) - clipping[1])]
        dict_time[file_name] = times

    # save
    with open(BASE_PATH + '/latency', 'w') as f:
        f.write('NUM\tAVG\tMED\tMIN\tMAX\t99%\t[S]\n')
        for file_name, times in dict_time.items():
            f.write(str(file_name) + '\t')
            f.write(str(avg_(times, (0, 0))) + '\t')
            f.write(str(med_(times, (0, 0))) + '\t')
            f.write(str(min_(times, (0, 0))) + '\t')
            f.write(str(max_(times, (0, 0))) + '\t')
            f.write(str(nin_(times, (0, 0))) + '\n')
