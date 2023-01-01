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


def calc_user_sim(dataSet):  # 建立物品-用户的倒排列表
    item_users = dict()
    for user, items in dataSet.items():
        for goods in items:
            if goods not in item_users:
                item_users[goods] = set()
            item_users[goods].add(user)
    # print("物品-用户倒排列表: ", item_users)
    return item_users


def user_similarity(userSet):
    C = dict()
    N = dict()
    for goods, users in userSet.items():
        for u in users:
            N.setdefault(u, 0)
            N[u] += 1  # 每个商品下用户出现一次就加一次，就是计算每个用户一共购买的商品个数。
            for v in users:
                if u == v:
                    continue
                C.setdefault(u, {})
                C[u].setdefault(v, 0)
                C[u][v] += 1
    # print("稀疏矩阵: ", C)
    W = dict()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W.setdefault(u, {})
            W[u].setdefault(v, 0)
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    # print("用户相似度: ", W)
    return W


def user_similarity_update(userSet):
    C = dict()
    N = dict()
    for goods, users in userSet.items():
        for u in users:
            N.setdefault(u, 0)
            N[u] += 1  # 每个商品下用户出现一次就加一次，就是计算每个用户一共购买的商品个数。
            for v in users:
                if u == v:
                    continue
                C.setdefault(u, {})
                C[u].setdefault(v, 0)
                C[u][v] += 1 / math.log(1 + len(users))
    # print("稀疏矩阵: ", C)
    W = dict()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W.setdefault(u, {})
            W[u].setdefault(v, 0)
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    # print("用户相似度: ", W)
    return W


def recommend(user, train, W, K):
    rvi = 1
    rank = dict()
    related_user = []
    interacted_items = train[user]

    for co_user, item in W.items():
        if co_user == user:
            for user, score in item.items():
                related_user.append((user, score))
            break
    # print("与user用户相似度: ", related_user)
    for v, wuv in sorted(related_user, key=itemgetter(1), reverse=True)[0:K]:
        for i in train[v]:
            if i in interacted_items:  # 如果用户已经喜欢或购买过，则不需要推荐
                continue
            if i not in rank.keys():
                rank[i] = 0
            rank[i] += wuv * rvi
    # print(rank)
    return rank


if __name__ == '__main__':
    filePath = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于用户的协同过滤推荐算法\\data\\协同过滤的推荐数据2.csv"
    dataSet = load_data(filePath)  # 产生数据集
    # print("\ndataSet: ", dataSet)
    userSet = calc_user_sim(dataSet)  # 对每种商品产生行为的用户列表
    # print("\nuserSet: ", userSet)
    userSimi = user_similarity(userSet)  # 计算用户相似度
    # print("\nuserSimi: ", userSimi)
    lastRank = recommend("22", dataSet, userSimi, 3)  # 目标用户id，数据集，用户相似度，与目标用户相似的K个用户（为目标用户推荐其未曾购买过的商品）
    print("                                                     ")
    print("为目标用户推荐的商品为: ", lastRank)
    print("                                                     ")
