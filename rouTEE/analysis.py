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
    PATH_NAME = 'tmp_payments'
    BASE_PATH = './' + PATH_NAME
    files = os.listdir(BASE_PATH)
    try:
        files.remove('.DS_Store')
    except:
        pass
    try:
        files.remove('analysis.py')
    except:
        pass
    try:
        files.remove(PATH_NAME)
    except:
        pass
    files = sorted(files, key=int)
    # print(files)

    clipping = (0, 0)

    diffs = []
    for file_ in files:
        with open(BASE_PATH + '/' + file_, 'r') as f:
            lines = f.readlines()
            lines = lines[clipping[0]:(len(lines) - clipping[1])]

            diff = []
            remove_first_N = 7  # logs
            lines = lines[remove_first_N:]

            if len(lines) == 1:
                try:
                    num, time = lines[0].split()
                    num, time = int(num), int(time)
                except:
                    pass
                diff = [num / time]
            else:
                for idx in range(len(lines) - 1):
                    try:
                        num, time = lines[idx].split()
                        num, time = int(num), int(time)
                        next_num, next_time = lines[idx + 1].split()
                        next_num, next_time = int(next_num), int(next_time)
                    except ValueError:
                        break

                    if (next_num - num) == 0:
                        pass
                    else:
                        diff.append((next_num - num) / (next_time - time))

        diffs.append(diff)

    scale = 1000000

    # print(diffs)
    with open(BASE_PATH + '/' + PATH_NAME, 'w') as f:
        f.write('NUM\tAVG\tMED\tMIN\tMAX\t99%\t[TPS]\n')
        for file_, diff in zip(files, diffs):
            f.write(str(file_) + '\t')
            f.write(str(avg_(diff, (1, 1)) * scale) + '\t')
            f.write(str(med_(diff, (1, 1)) * scale) + '\t')
            f.write(str(min_(diff, (1, 1)) * scale) + '\t')
            f.write(str(max_(diff, (0, 0)) * scale) + '\t')
            f.write(str(nin_(diff, (0, 0)) * scale) + '\n')
