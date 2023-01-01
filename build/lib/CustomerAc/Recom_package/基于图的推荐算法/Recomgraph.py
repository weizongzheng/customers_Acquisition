

def load_data(file_path):
    records = []
    f = open(file_path, "r", encoding="utf-8")
    for line in f:
        info = line.strip().split(",")
        records.append(info)
    f.close()
    return records


def calc_user_item(records):
    user_item = dict()
    item_user = dict()
    for user, item in records:
        user_item.setdefault(user, dict())
        user_item[user].setdefault(item, 0)
        user_item[user][item] = 1   # 用户顶点
        item_user.setdefault(item, dict())
        item_user[item].setdefault(user, 0)
        item_user[item][user] = 1   # 商品顶点
    # print("商品-用户倒排列表: ", user_item)
    return user_item, item_user


def initGraph(user_item, item_user):
    user_item_tag = dict()
    user_item_tag = dict(user_item, **item_user)
    return user_item_tag


# G: 二分图     alpha：随机游走概率     root: 初始节点     max_step: 最大游走步数
def PersonalRank(G, alpha, root, max_step):
    rank = dict()
    rank = {x: 0 for x in G.keys()}
    rank[root] = 1
    for k in range(max_step):
        tmp = {x: 0 for x in G.keys()}
        for i, ri in G.items():
            for j, wij in ri.items():
                if j not in tmp:
                    tmp[j] = 0
                tmp[j] += 0.6 * rank[i] / (1.0 * len(ri))
                if j == root:
                    tmp[j] += 1 - alpha
        # tmp[root] += 1 - alpha
        rank = tmp
    rec = sorted(rank.items(), key=lambda x: x[1], reverse=True)  # 目标用户对其余节点（包含商品和其它用户）的重要程度进行打分排名
    return rec


def Recommend(user, rank, user_item):
    rec = []
    for goods in rank:
        data = goods[0]
        rec.append(data)
    for u, v in user_item.items():
        for i in rec:
            if i == u:
                rec.remove(i)
    for u, v in user_item[user].items():
        for i in rec:
            if i == u:
                rec.remove(i)
    return rec


if __name__ == '__main__':
    file_path = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于图的推荐算法\\data\\基于图的推荐数据3.txt"
    records = load_data(file_path)
    print("                                                     ")
    print("数据集: ", records)
    print("                                                     ")
    user_item, item_user = calc_user_item(records)
    print("用户顶点: ", user_item)
    print("                                                     ")
    print("物品顶点: ", item_user)
    print("                                                     ")
    G = initGraph(user_item, item_user)
    print("G: ", G)
    print("                                                     ")
    taguser = "A"  # 设置初始节点，即用户id
    rank = PersonalRank(G, 0.85, taguser, 100)  # 以G为二分图，随机游走概率为0.85，初始节点为A，最大游走步数为100
    print("权重排名：", rank)
    rec = Recommend(taguser, rank, user_item)
    print("                                                     ")
    print("为目标用户%s推荐物品: %s" % (taguser, rec))
    print("                                                     ")
