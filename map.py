import matplotlib.pyplot as plt
import numpy as np
import csv

plt.figure(figsize=(20, 20))
dot_dict = dict()


def make_dot_dict(item):
    dot_dict[int(item[2:6])] = [int(item[8:13]), int(item[13:18])]


def make_line(item, dot_dict):
    line_x_list = []
    line_y_list = []
    line_x_list.append(int(dot_dict[int(item[2:6])][0]))
    line_y_list.append(int(dot_dict[int(item[2:6])][1]))
    for i in range(0, min(int(item[88:91]), 16)):
            print(item)
            print(item[88:91])
            print(repr(item[(91+i*10):(96+i*10)]))
            print(repr(item[(96+i*10):(101+i*10)]))
            line_x_list.append(int(item[(91+i*10):(96+i*10)]))
            line_y_list.append(int(item[(96+i*10):(101+i*10)]))
    line_x_list.append(int(dot_dict[int(item[6:10])][0]))
    line_y_list.append(int(dot_dict[int(item[6:10])][1]))
    return line_x_list, line_y_list


def make_datalist():
    result_x_list = []
    result_y_list = []
    x_list = []
    y_list = []
    count = 0
    with open("./533421.txt", "r", encoding="utf_8") as f:
        for sentence in f:
            item = sentence
            if item[0:2] == "21":
                x_list.append(int(item[8:13]))
                y_list.append(int(item[13:18]))
                make_dot_dict(item)
                count += 1
            if item[0:2] == "22":
                line_x_list, line_y_list = make_line(item, dot_dict)
                print(line_y_list, line_x_list)
                result_x_list.append(line_x_list)
                result_y_list.append(line_y_list)
            if item[0:2] == "46":
                pass
    print(count)
    return x_list, y_list, dot_dict, result_x_list, result_y_list


def make_time_list():
    time_x_list = []
    time_y_list = []
    label_list = []
    with open("./tableview.csv","r",encoding="utf_8") as f:
        reader = csv.reader(f)
        for row in reader:
           time_y_list.append((float(row[3])-0.003148714-35.5)*12*10000)
           time_x_list.append((float(row[2])+0.002714486-134.125)*8*10000)
           label_list.append(row[1])
    return time_x_list, time_y_list, label_list




x_list, y_list,dot_dict,result_x_list, result_y_list = make_datalist()
x_list = np.array(x_list)
y_list = np.array(y_list)
#print(dot_dict)
#print(x_list.shape[0])
plt.subplot(x_list.shape[0])
plt.scatter(x_list, y_list, c="r", s=1)

for i in range(0, len(result_x_list)):
    plt.plot(result_x_list[i], result_y_list[i])

time_x_list, time_y_list, label_list =make_time_list()


plt.scatter(time_x_list, time_y_list, c="black", s=15, marker="x")

for i in range(0, 50):
    plt.annotate(label_list[i], (time_x_list[i], time_y_list[i]), size=2)

plt.rcParams["figure.figsize"] = [60, 60]
plt.rcParams["figure.dpi"] = 100000000
plt.xlim((0, 10000))
plt.ylim((0, 10000))
my_x_ticks = np.arange(0, 10000, 2000)
my_y_ticks = np.arange(0, 10000, 1000)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
plt.savefig("./data.png", dpi=500)

