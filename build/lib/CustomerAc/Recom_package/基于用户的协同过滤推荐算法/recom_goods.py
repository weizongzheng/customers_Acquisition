import math
# from collections import defaultdict
from operator import itemgetter


def load_data(filePath):
    f = open(filePath, "r", encoding="utf-8")
    trainSet = {}
    # len = 0
    for line in f:
        userId, goods_id, rating = line.strip().split(",")
        trainSet.setdefault(userId, {})
        trainSet[userId][goods_id] = rating
        # len = len + 1
        # if len > 10000:  # 取10000条数据
        #     break
    f.close()

    return trainSet


def calc_item_sim(dataSet):
    item_users = dict()
    for user, items in dataSet.items():
        for goods in items:
            if goods not in item_users:
                item_users[goods] = set()
            item_users[goods].add(user)
    # print("物品-用户倒排列表: ", item_users)
    return item_users


def item_similarity(userSet):
    C = dict()
    N = dict()
    for u, items in userSet.items():
        for i in items:
            N.setdefault(i, 0)
            N[i] += 1
            for j in items:
                if i == j:
                    continue
                C.setdefault(i, {})
                C[i].setdefault(j, 0)
                C[i][j] += 1
    # print("稀疏矩阵: ", C)
    W = dict()
    for i, related_items in C.items():
        for j, cij in related_items.items():
            W.setdefault(i, {})
            W[i].setdefault(j, 0)
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    # print("物品相似度: ", W)
    return W


def recommend(user, train, W, K):
    pi = 1
    rank = dict()
    interacted_items = train[user]
    for item in interacted_items:
        # print(">>>>>>>>", item)
        related_item = []
        for user, score in W[item].items():
            related_item.append((user, score))
        for j, v in sorted(related_item, key=itemgetter(1), reverse=True)[0:K]:  # 找到K个相关用户以及对应兴趣相似度
            if j in interacted_items:
                continue
            if j not in rank.keys():
                rank[j] = 0
            rank[j] += pi * v
    return rank


if __name__ == '__main__':
    file_path = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于用户的协同过滤推荐算法\\data\\协同过滤的推荐数据2.csv"
    dataSet = load_data(file_path)  # 产生数据集
    # print("\ndataSet: ", dataSet)
    userSet = calc_item_sim(dataSet)  # 对每种商品产生行为的用户列表
    # print("\nuserSet: ", userSet)
    itemSimi = item_similarity(dataSet)  # 计算物品相似度
    # print("\nuserSimi: ", itemSimi)
    lastRank = recommend("1", dataSet, itemSimi, 1)  # 目标用户id为1，数据集，物品相似度，为目标用户喜欢的每个商品分别推荐K个相关度较高的商品
    print("                                                     ")
    print("为目标用户推荐商品: ", lastRank)
    print("                                                     ")
