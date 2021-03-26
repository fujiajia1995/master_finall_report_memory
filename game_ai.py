from copy import deepcopy
import time


class KomaInstance(object):
    def __init__(self):
        self.size = 10
        self.null_list = set(range(0, self.size*self.size))
        self.player1_list = set()
        self.player2_list = set()

    def print_state(self):
        assert self.null_list.isdisjoint(self.player1_list) and self.null_list.isdisjoint(self.player2_list) and self.player2_list.isdisjoint(self.player1_list)
        for i in range(0,10):
            print("\n", end="")
            for j in range(0, 10):
                num = i*10+j
                if num in self.null_list:print("囗", end="")
                elif num in self.player1_list:print("〇", end="")
                elif num in self.player2_list:print("㐅", end="")
                else: print("error")

    def change_state(self, player, pos_x, pos_y):
        pos_x -= 1
        pos_y -= 1
        pos = pos_x*10+pos_y
        assert pos <= 99 and pos in self.null_list
        assert player == 1 or player == 2
        self.null_list.remove(pos)
        if player == 1:
            self.player1_list.add(pos)
        elif player == 2:
            self.player2_list.add(pos)


class Node(object):     #nodeの設計
    def __init__(self, instance, depth, id):
        self.id = id    #nodeのId
        self.father = 0  #the father id of the node
        self.son_node_id = list()   #the list of the son node
        self.content = deepcopy(instance)  #the stat of the node
        self.depth = depth                #the depth of the node
        self.score = None                 #the score of the node

    def generate_son(self):                #the piece that near the piece on the chessboard which is most likely to lay down
        generate_set = set()
        for koma in self.content.player1_list:
            if koma+1 < 100: generate_set.add(koma+1)
            if koma-1 > 0: generate_set.add(koma-1)
            if koma+10 <100: generate_set.add(koma+10)
            if koma-10 > 0 : generate_set.add(koma-10)
            if koma+11 < 100: generate_set.add(koma+11)
            if koma-11 >0: generate_set.add(koma-11)
            if koma+9 <100:generate_set.add(koma+9)
            if koma-9 >0:generate_set.add(koma-9)
        for koma in self.content.player2_list:
            if koma+1 < 100: generate_set.add(koma+1)
            if koma-1 > 0 : generate_set.add(koma-1)
            if koma+10 <100: generate_set.add(koma+10)
            if koma-10 > 0 : generate_set.add(koma-10)
            if koma+11 < 100: generate_set.add(koma+11)
            if koma-11 >0: generate_set.add(koma-11)
            if koma+9 <100:generate_set.add(koma+9)
            if koma-9 >0:generate_set.add(koma-9)
        generate_set = generate_set.difference(self.content.player2_list)
        generate_set = generate_set.difference(self.content.player1_list)
        return generate_set


class Tree(object):              #the design of the tree
    def __init__(self, node=0, count=4):      # generate the tree using the Breadth-First Search
        self.open_list = list()
        self.close_list = list()
        if node != 0:
            self.start_node = Node(deepcopy(node), 1, 1)
        else:                                  # test mode
            a = KomaInstance()
            a.change_state(2, 5, 5)
            a.change_state(1, 6, 6)
            a.change_state(2, 4, 3)
            self.start_node = Node(a, 1, 1)
        self.open_list.append(self.start_node)
        id_count = 1
        while len(self.open_list) != 0:
            generate_set = self.open_list[0].generate_son()
            temp_node_1 = self.open_list.pop(0)
            self.close_list.append(temp_node_1)
            for item in generate_set:
                id_count += 1
                temp = deepcopy(self.close_list[len(self.close_list)-1])
                temp_stat = temp.content
                temp_depth = temp.depth+1
                if temp_depth-2*(temp_depth//2) == 0: player = 1
                else: player = 2
                pos_x = item//10+1
                pos_y = item - 10*(item//10)+1
                temp_stat.change_state(player, pos_x, pos_y)
                temp_id = id_count
                temp_father = temp.id
                self.close_list[len(self.close_list)-1].son_node_id.append(temp_id)
                temp_node_2 = Node(temp_stat, temp_depth, temp_id)
                temp_node_2.father = temp_father
                self.open_list.append(deepcopy(temp_node_2))
                if temp_depth == count + 1:
                    self.close_list.extend(self.open_list)
                    self.open_list.clear()
                    return None

    def return_depth_node(self, depth=1):       #return the node whose depth is equal with the input depth
        kekka_list = list()
        if depth == 1:
            for item in self.close_list:
                if item.depth == 1:
                    kekka_list.append(item)
        if depth == 2:
            for item in self.close_list:
                if item.depth == 2:
                    kekka_list.append(item)
        if depth == 3:
            for item in self.close_list:
                if item.depth == 3:
                    kekka_list.append(item)
        if depth == 4:
            for item in self.close_list:
                if item.depth == 4:
                    kekka_list.append(item)
        if depth == 5:
            for item in self.close_list:
                if item.depth == 5:
                    kekka_list.append(item)
        return kekka_list


def get_score(input_set1, input_set2):          #the design of the score ,
    kekka_dict = {"2": 0, "3": 0, "4": 0,"5":0}
    komaset_dict = {"1": deepcopy(input_set1),
                    "10": deepcopy(input_set1),
                    "9": deepcopy(input_set1),
                    "11": deepcopy(input_set1)}
    for i in [1,10,9,11]:                       #自分の駒の二# 連の数*0.1+三連の数*0.8+四連の数*1.5+五連の数*1000
        while len(komaset_dict[str(i)]) != 0:
            temp_node = komaset_dict[str(i)].pop()
            temp_count = 1
            for j in range(1, 5):
                if temp_node-i*j in komaset_dict[str(i)]:
                    komaset_dict[str(i)].remove(temp_node-i*j)
                    temp_count += 1
                else:
                    break
            for j in range(1, 5):
                if temp_node+i*j in komaset_dict[str(i)]:
                    komaset_dict[str(i)].remove(temp_node+i*j)
                    temp_count += 1
                else:
                    break
            if temp_count in set([2,3,4,5]):
                kekka_dict[str(temp_count)] += 1
    score = kekka_dict["2"]*0.1+kekka_dict["3"]*0.8+kekka_dict["4"]*1.5+kekka_dict["5"]*1000

    input_set1_2 = deepcopy(input_set1)  #相手を止めるための設計、自分の駒一個と相手の駒４連の数掛ける４０プラス５連の数掛ける７０
    input_set2_2 = deepcopy(input_set2)
    stop_dict = {"4": 0, "5": 0}
    for koma in input_set1_2:
        for i in [1, 10, 11, 9]:
            stop_count = 1
            flag = 1
            while flag:
                for j in range(1, 5):
                    if koma + i * j in input_set2_2:
                        stop_count += 1
                    else:
                        break
                for j in range(1, 5):
                    if koma - i * j in input_set2_2:
                        stop_count += 1
                    else:
                        break
                flag = 0

                if stop_count in set([4, 5]):
                    stop_dict[str(stop_count)] += 1
    stop_score = stop_dict["4"] * 40 + stop_dict["5"] * 70
    score += stop_score

    return score


def get_result(input_set):                 #５連が取るかどうかの判断
    kekka_dict = {"2": 0, "3": 0, "4": 0, "5": 0}
    komaset_dict = {"1": deepcopy(input_set),
                    "10": deepcopy(input_set),
                    "9": deepcopy(input_set),
                    "11": deepcopy(input_set)}
    for i in [1, 10, 9, 11]:
        while len(komaset_dict[str(i)]) != 0:
            temp_node = komaset_dict[str(i)].pop()
            temp_count = 1
            for j in range(1, 5):
                if temp_node-i*j in komaset_dict[str(i)]:
                    komaset_dict[str(i)].remove(temp_node-i*j)
                    temp_count += 1
                else:
                    break
            for j in range(1, 5):
                if temp_node+i*j in komaset_dict[str(i)]:
                    komaset_dict[str(i)].remove(temp_node+i*j)
                    temp_count += 1
                else:
                    break
            if temp_count in set([2,3,4,5]):
                kekka_dict[str(temp_count)] += 1
    if kekka_dict["5"] != 0:
        return True
    return False


def make_decision(tree=0): #mini-maxの設計
    if tree != 0:
       temp_tree = deepcopy(tree)
    else:
        b = Tree()
        temp_tree = b
    for item in temp_tree.return_depth_node(4):
        player1_score = get_score(item.content.player1_list,item.content.player2_list)
        player2_score = get_score(item.content.player2_list,item.content.player1_list)
        score = player1_score-player2_score
        item.score = score
    for item_1 in temp_tree.return_depth_node(3):
        temp_score_1 = 100
        for item_2 in temp_tree.return_depth_node(4):
            if item_2.father == item_1.id:
                if item_2.score < temp_score_1:
                    temp_score_1 = item_2.score
        item_1.score = temp_score_1
    for item_1 in temp_tree.return_depth_node(2):
        temp_score_1 = -100
        for item_2 in temp_tree.return_depth_node(3):
            if item_2.father == item_1.id:
                if item_2.score > temp_score_1:
                    temp_score_1 = item_2.score
        item_1.score = temp_score_1
    temp = -100
    temp_instance = 0
    for item in temp_tree.return_depth_node(2):
        if item.score > temp:
            temp = item.score
            temp_instance = item
    return temp_instance.content


def main():                  #ユーザーとの交流の部分の設計
    a = KomaInstance()
    a.change_state(1, 5, 5)
    print("今の状態：")
    a.print_state()
    input_location=input("input pattern;pos_x,pos_y;")
    while input_location:
        temp_input = list(input_location)
        if temp_input[1] != ",":
            continue
        pos_x = int(temp_input[0])
        pos_y = int(temp_input[2])
        a.change_state(2, pos_x, pos_y)
        b = Tree(a)
        a = make_decision(b)
        print("今の状態：")
        a.print_state()
        if get_result(a.player1_list):
            print("player1 win")
            time.sleep(3)
            return
        elif get_result(a.player2_list):
            print("player2 win")
            time.sleep(3)
            return
        else:
            input_location = input("input pattern;pos_x,pos_y;")


main()
