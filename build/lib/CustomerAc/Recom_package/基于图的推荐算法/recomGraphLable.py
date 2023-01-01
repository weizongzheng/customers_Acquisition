

def load_data(file_path):
    records = []
    f = open(file_path, "r", encoding="utf-8")
    for line in f:
        info = line.strip().split(",")
        records.append(info)
    f.close()
    return records


def user_vertex_cal(records):  # 建立商品-用户的倒排列表
    user_tag = dict()
    tag_user = dict()
    tag_goods = dict()
    goods_tag = dict()
    for user, goods, tag in records:
        user_tag.setdefault(user, dict())
        user_tag[user].setdefault(tag, 0)
        user_tag[user][tag] = 1  # 用户顶点
        tag_user.setdefault(tag, dict())
        tag_user[tag].setdefault(user, 0)
        tag_user[tag][user] = 1  # 标签顶点
        tag_goods.setdefault(tag, dict())
        tag_goods[tag].setdefault(goods, 0)
        tag_goods[tag][goods] = 1  # 标签顶点
        goods_tag.setdefault(goods, dict())
        goods_tag[goods].setdefault(tag, 0)
        goods_tag[goods][tag] = 1  # 商品顶点
    return user_tag, tag_user, tag_goods, goods_tag


def initGraph(user_tag, tag_user, tag_goods, goods_tag):
    tag_G = dict()
    goods_G = dict()
    tag_G = dict(user_tag, **tag_user)
    goods_G = dict(tag_goods, **goods_tag)
    return tag_G, goods_G


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

        rank = tmp
    rec = sorted(rank.items(), key=lambda x: x[1], reverse=True)  # 目标用户对其余节点（包含商品种类和其它用户）的重要程度进行打分排名
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
    file_path = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于图的推荐算法\\data\\基于图标签的推荐数据2.txt"
    records = load_data(file_path)
    # print(records)
    user_tag, tag_user, tag_goods, goods_tag = user_vertex_cal(records)
    print("                                                     ")
    print("                                                     ")
    print("用户-标签顶点: ", user_tag)
    print("                                                     ")
    print("标签-用户顶点: ", tag_user)
    print("                                                     ")
    print("标签-商品顶点: ", tag_goods)
    print("                                                     ")
    print("商品-标签顶点: ", goods_tag)
    print("                                                     ")
    print("                                                     ")
    tag_G, goods_G = initGraph(user_tag, tag_user, tag_goods, goods_tag)
    print("                                                     ")
    print("tag_G: ", tag_G)
    print("                                                     ")
    print("goods_G: ", goods_G)
    print("                                                     ")
    print("                                                     ")
    taguser = "D"  # 设置初始节点，即用户id
    rank = PersonalRank(tag_G, 0.85, taguser, 100)  # 以tag_G为二分图，随机游走概率为0.85，初始节点为A，最大游走步数为100
    print("权重排名：", rank)
    print("                                                     ")
    rec = Recommend(taguser, rank, user_tag)
    print("为目标用户%s推荐的商品种类:%s " % (taguser, rec))  # 推荐的商品种类中会去除之前和目标用户有过行为的商品种类
    print("                                                     ")
