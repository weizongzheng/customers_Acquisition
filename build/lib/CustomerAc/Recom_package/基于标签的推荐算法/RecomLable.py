# 基于标签的商品推荐系统

from math import log
# from collections import defaultdict


def load_data(file_path):
    records = []
    f = open(file_path, "r", encoding="utf-8")
    for line in f:
        info = line.strip().split(",")  # 分割
        records.append(info)
    f.close()
    return records


def InitStat_update_2(records):
    user_tags = dict()  # 用户打过标签的次数，代表用户对不同类型商品的偏好
    tag_items = dict()  # 商品按种类被打过标签的次数，代表商品流行度
    tag_user = dict()  # 标签被用户使用次数，按商品种类分类，查看不同用户的偏好
    item_user = dict()  # 商品被不同用户标记次数，按具体商品分类，查看不同用户的偏好

    for user, item, tag in records:
        user_tags.setdefault(user, dict())
        user_tags[user].setdefault(tag, 0)
        user_tags[user][tag] += 1

        tag_items.setdefault(tag, dict())
        tag_items[tag].setdefault(item, 0)
        tag_items[tag][item] += 1

        tag_user.setdefault(tag, dict())
        tag_user[tag].setdefault(user, 0)
        tag_user[tag][user] += 1

        item_user.setdefault(item, dict())
        item_user[item].setdefault(user, 0)
        item_user[item][user] += 1

    return user_tags, tag_items, tag_user, item_user


def Recommend_update_2(user, K):
    recommend_items = dict()
    for tag, wut in user_tags[user].items():
        for item, wti in tag_items[tag].items():
            if item not in recommend_items:
                recommend_items[item] = (wut / log(1 + len(tag_user[tag]))) * (
                            wti / log(1 + len(item_user[item])))  # 计算用户对商品兴趣度
            else:
                recommend_items[item] += (wut / log(1 + len(tag_user[tag]))) * (wti / log(1 + len(item_user[item])))

    rec = sorted(recommend_items.items(), key=lambda x: x[1], reverse=True)  # 将推荐商品按兴趣度排名
    print("推荐商品按兴趣度排名：\n", rec)
    goods = []
    for i in range(K):
        goods.append(rec[i][0])

    goods = "/".join(goods)

    return goods


if __name__ == '__main__':
    file_path = u"data/标签的推荐数据2.txt"
    records = load_data(file_path)
    # print(records)
    user_tags, tag_items, tag_user, item_user = InitStat_update_2(records)
    print("-----------------------------------------------------")
    print("                                                     ")
    print("用户打过标签的次数: \n", user_tags)
    print("                                                     ")
    print("商品按种类被打过标签的次数: \n", tag_items)
    print("                                                     ")
    print("标签被用户使用次数: \n", tag_user)
    print("                                                     ")
    print("商品被用户标记次数: \n", item_user)
    print("                                                     ")
    print("-----------------------------------------------------")
    print("                                                     ")
    rec = Recommend_update_2("A", 3)  # 向目标用户A推荐top3商品
    print("                                                     ")
    print("推荐商品: \n", rec)
    print("                                                     ")
