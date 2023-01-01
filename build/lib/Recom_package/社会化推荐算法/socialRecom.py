import math
# import time, datetime
# from collections import defaultdict
# from operator import itemgetter


def load_data(friend_file, interest_file):  # 构建好友及兴趣数据集
    fri_f = open(friend_file, "r", encoding="utf-8")
    int_f = open(interest_file, "r", encoding="utf-8")
    friends_data = dict()  # 好友数据集
    for line in fri_f:
        data = line.strip().split("\t")
        friends_data[data[0]] = data[1].split(",")

    interests_data = dict()  # 兴趣数据集
    for line in int_f:
        data = line.strip().split("\t")
        interests_data[data[0]] = data[1].split(",")
    fri_f.close()
    int_f.close()
    return friends_data, interests_data


def user_friend_interest(friends_data, interests_data):  # 构建好友及兴趣倒排列表
    friends_dic = dict()  # 好友倒排列表
    for user, friends in friends_data.items():
        for friend in friends:
            if friend not in friends_dic:
                friends_dic[friend] = set()
            friends_dic[friend].add(user)

    interests_dic = dict()  # 兴趣倒排列表
    for user, interests in interests_data.items():
        for interest in interests:
            if interest not in interests_dic:
                interests_dic[interest] = set()
            interests_dic[interest].add(user)
    return friends_dic, interests_dic


def similarity(data):    # 好友熟悉度
    C = dict()
    N = dict()
    for user, friends in data.items():
        for u in friends:
            N.setdefault(u, 0)
            N[u] += 1  # 计算每个用户好友数量
            for v in friends:
                if u == v:
                    continue
                C.setdefault(u, {})
                C[u].setdefault(v, 0)
                C[u][v] += 1   # 计算共同好友数量
    # print("稀疏矩阵: ", C)  # 对于每个用户，列出其与其它用户的共同好友数
    W = dict()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W.setdefault(u, {})
            W[u].setdefault(v, 0)
            W[u][v] = cuv / math.sqrt(N[u] * N[v])

    # print("好友熟悉度: ", W)
    return W


def Recommend(user, familiarity, similarity, train):   # 假设对每个物品的喜欢程度都为1
    pw = 1
    rank = dict()
    interacted_items = train[user]  # 获取user感兴趣的物品
    rank = dict()
    for fid, fw in familiarity[user].items():
        for item in train[fid]:
            if item in interacted_items:
                continue
            rank.setdefault(item, 0)
            rank[item] = fw * pw
    for vid, sw in similarity[user].items():
        for item in train[vid]:
            if item in interacted_items:
                continue
            rank.setdefault(item, 0)
            rank[item] = sw * pw
    rank = sorted(rank.items(), key=lambda x: x[1], reverse=True)   # 按兴趣度排序
    return rank


if __name__ == '__main__':
    friend_file = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\社会化推荐算法\\data\\社交网络的推荐数据_好友.txt"
    interest_file = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\社会化推荐算法\\data\\社交网络的推荐数据_爱好.txt"
    friends_data, interests_data = load_data(friend_file, interest_file)
    print("                                                     ")
    print("好友数据集: ", friends_data)
    print("兴趣数据集: ", interests_data)
    print("                                                     ")
    friends,  interests = user_friend_interest(friends_data, interests_data)
    print("                                                     ")
    print("好友数据倒排列表: ", friends)
    print("兴趣数据倒排列表: ", interests)
    print("                                                     ")
    fam_sim = similarity(friends)
    int_sim = similarity(interests)
    print("                                                     ")
    print("用户-好友熟悉度: ", fam_sim)
    print("用户-兴趣相似度: ", int_sim)
    print("                                                     ")
    rec = Recommend("A", fam_sim, int_sim, interests_data)  # 目标用户id，熟悉度，兴趣相似度，兴趣数据集
    print("                                                     ")
    print("为用户推荐商品列表: ", rec)
    print("                                                     ")
