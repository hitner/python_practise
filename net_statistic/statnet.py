# run example: python3 statnet.py 2.0 ~/Downloads/Log
# author: Liuzhuzhai
# date:2018-01-01

import sys
import os
import re
import time

kDateLen = len("2017-12-28 16:04:43.660")
kSeqRE = r"seq=[0-9]+,"
kOpRE = r"op=(0x)?[0-9a-fA-F]+"
kSeqC = re.compile(kSeqRE)
kOpC = re.compile(kOpRE)


def get_date(line: str) -> int:
    ldate_s = time.strptime(line[:kDateLen - 4], "%Y-%m-%d %H:%M:%S")
    ldate_f = time.mktime(ldate_s)
    ldate_f = ldate_f + int(line[kDateLen - 3:kDateLen]) / 1000.0
    return ldate_f


def get_seq(line)-> int:
    lists = re.findall(kSeqC, line)
    target = lists[0]
    seq = target[4:len(target) - 1]
    return int(seq)


def get_op(line):
    lists = re.search(kOpC, line)
    target = lists[0]
    return target[3:]


def parse_line(line):
    sendFlag = line.find(">>:>>>NetworkCore socket send Ok")
    type = 0
    if sendFlag == kDateLen:
        type = 1
    elif sendFlag == -1:
        recvFlag = line.find(">>:>>>NetworkCore socket received Ok")
        if recvFlag == kDateLen:
            type = 2
    if type == 0:
        return None
    ldate :str = get_date(line)
    lseq = get_seq(line)
    lop = get_op(line)
    return (type, lseq, lop, ldate, line[0:kDateLen])


def my_print(one):
    return "%s, seq:%s,\top:%s,\tdelay:%.3f" % (one['date'], one['seq'], one['op'], one['delay'])


results = []
problems = []
threshold = 1.5


def acc(send_list, recv):
    global threshold
    for send in send_list:
        if send[1] == recv[1] and send[2] == recv[2]:
            delay = recv[3] - send[3]
            one = {'date': send[4], "seq": send[1], "op": send[2], "sec": send[3], "delay": delay}
            results.append(one)
            send_list.remove(send)
            if delay > threshold:
                problems.append(one)
                print(my_print(one))
            return


def one_file(path: str) -> None:
    file_content = open(path)
    flines = file_content.readlines()
    send_list = []
    for line in flines:
        ret = parse_line(line)
        if ret:
            if ret[0] == 1:
                send_list.append(ret)
            elif ret[0] == 2:
                acc(send_list, ret)

    file_content.close()


def save_all(path):
    path: int = path.replace("txt", "md")
    f = open(path, "w")
    f.writelines("====Path:%s====\n" % (sys.argv[2]))
    for one in results:
        f.writelines(my_print(one) + '\n')
    f.close()


def statistics(min_time: float, directory: str) -> None:
    global threshold
    print("duration:%s, directory:%s" % (min_time, directory))
    threshold = float(min_time)
    for file in os.listdir(directory):
        if file.endswith("_network.txt"):
            print("===========%s=========" % (file))
            one_file(file)
            print("--------------------------")
            save_all("abc_" + file)
            results.clear()


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        statistics(sys.argv[1], sys.argv[2])
    else:
        print("not enough param!")
