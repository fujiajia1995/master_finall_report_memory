mport random

switch_flag = 1 # 0 Qlearning 1 Sarsa


class Node(object):
    def __init__(self, up_status, up_price, down_status, down_price, left_status, left_price, right_status, right_price):
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
        self.up_status = [up_status, up_price]
        self.down_status = [down_status, down_price]
        self.left_status = [left_status, left_price]
        self.right_status = [right_status, right_price]

    def print(self):
        print(str(self.up)+"  ", end="")
        print(str(self.down)+" ", end="")
        print(str(self.left)+" ", end="")
        print(self.right)

    def make_max(self,switch_flag):
        if switch_flag ==0:
            return max([self.up, self.right, self.down, self.left])
        if switch_flag ==1:
            sorted_list =  sorted([self.up, self.down, self.left,self.right],reverse=True)
            r = random.randint(0,100)
            if r < 90:
                return sorted_list[0]
            else:
                r = random.randint(1, 3)
                return sorted_list[r]

    def make_choice(self):
        status_list = [self.up, self.down, self.left, self.right]
        pos_dict = {0: self.up_status, 1: self.down_status, 2: self.left_status, 3: self.right_status}
        max = -100000000
        for num in status_list:
            if num > max:
                max = num
        i = 0
        maxnum_list = []
        for num in status_list:
            if num == max:
                maxnum_list.append(i)
            i += 1
        division = len(maxnum_list)
        r = random.randint(1, 100)
        if division == 4:
            pos = random.randint(0, 3)
            return {"list": maxnum_list[pos], "NextStatus": pos_dict[maxnum_list[pos]],
                    "maximum": status_list[maxnum_list[pos]]}
        if r <= 90:
            pos = random.randint(0,division-1)
            return {"list": maxnum_list[pos],"NextStatus": pos_dict[maxnum_list[pos]], "maximum": status_list[maxnum_list[pos]]}
        else:
            pos_list = list(set(range(0, 4))-set(maxnum_list))
            pos = random.randint(0,4-division-1)
            return {"list": pos_list[pos], "NextStatus": pos_dict[pos_list[pos]], "maximum": status_list[pos_list[pos]]}


def node_update(node,ModeFlag,a,y,node_list):
    result_dict = node.make_choice()
    ModeFlag = switch_flag
    if result_dict["list"] == 0:
        node.up = node.up + a*(result_dict["NextStatus"][1] + y * (node_list[result_dict["NextStatus"][0]].make_max(switch_flag) - node.up))
        return result_dict["NextStatus"][0]
    if result_dict["list"] == 1:
        node.down = node.down + a*(result_dict["NextStatus"][1] + y * (node_list[result_dict["NextStatus"][0]].make_max(switch_flag) - node.down))
        return result_dict["NextStatus"][0]
    if result_dict["list"] == 2:
        node.left = node.left + a*(result_dict["NextStatus"][1] + y * (node_list[result_dict["NextStatus"][0]].make_max(switch_flag) - node.left))
        return result_dict["NextStatus"][0]
    if result_dict["list"] == 3:
        node.right = node.right + a*(result_dict["NextStatus"][1] + y * (node_list[result_dict["NextStatus"][0]].make_max(switch_flag) - node.right))
        return result_dict["NextStatus"][0]


def make_loop(node_list, flag):
    now_node = node_list[6]
    node_num = 6
    i = 0
    while node_num != 11 and i != 1000:
        node_num = node_update(now_node, flag, 0.1, 0.9, node_list)
        now_node = node_list[node_num]
        i += 1


def make_y_reward_sum(node_list, y, switch_flag):
    node_num = 6
    i = 0
    kekka = 0
    while node_num != 11 and i < 1000:
        result_dict = node_list[node_num].make_choice()
        node_num = result_dict["NextStatus"][0]
        kekka += y**i*(result_dict["NextStatus"][1])
        i += 1

    return kekka


def main1():
    kekka_list = [0]*3000
    for j in range(100):
        print(j)
        node0 = Node(0, -1, 6, -1, 0, -1, 1, -1)
        node1 = Node(1, -1, 7, -1, 0, -1, 2, -1)
        node2 = Node(2, -1, 8, -1, 1, -1, 3, -1)
        node3 = Node(3, -1, 9, -1, 2, -1, 4, -1)
        node4 = Node(4, -1, 10, -1, 3, -1, 5, -1)
        node5 = Node(5, -1, 11, 10, 4, -1, 5, -1)
        node6 = Node(0, -1, 6, -100, 6, -1, 7, -1)
        node7 = Node(1, -1, 7, -100, 6, -1, 8, -1)
        node8 = Node(2, -1, 8, -100, 7, -1, 9, -1)
        node9 = Node(3, -1, 9, -100, 8, -1, 10, -1)
        node10 = Node(4, -1, 10, -100, 9, -1, 11, 10)
        node11 = Node(5, -1, 11, -100, 10, -1, 11, -1)
        node_list = [node0, node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11]
        for i in range(0, 3000):
            make_loop(node_list, switch_flag)
            kekka_list[i] += make_y_reward_sum(node_list, 0.9, switch_flag)
    x = 0
    for i in kekka_list:
        print(str(x)+":"+str(i/100))
        x+=1
    for i in range(0, 12):
        node_list[i].print()
        #for i in range(0,3000):
        #    make_loop(node_list,switch_flag)
        #print(make_y_reward_sum(node_list,0.9,switch_flag))


main1()
