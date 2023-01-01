def testsdk():
    print("test sdk successfully")
from CustomerAc.Recom_package.UserCF商品推荐.main import *
def algorithm_1(file_path,cust): # 基于用户协同过滤的商品算法一
    ubcf = UserBasedCF(file_path)
    ubcf.readData()  # 读取数据
    ubcf.preprocessData()  # 预处理数据
    ubcf.userSimilarity()  # 计算用户相似度矩阵
    # ------ 为用户 i 产生推荐 ------ #
    i = cust
    topN = ubcf.recommend(i, k=3, N=10)  # 输出格式：商品的id和评分
    topN_list = list(topN.keys())  # 只取对应的商品的id
    print("                                                     ")
    print("------ i ------")
    print(i)
    print("                                                     ")
    print("------ topN_list ------")
    print(topN_list)
    print("                                                     ")

    # ------ 为全部用户产生推荐 ------ #
    # topN_list = {} # 存储为每一个用户推荐的列表
    # for each_user in ubcf.trainData:
    #     topN = ubcf.recommend(each_user, k=3, N=10) # 商品的id和评分
    #     topN_list[each_user] = list(topN.keys()) # 只取对应的商品的id
    #
    #     print("------ topN_list[each_user] ------")
    #     print(topN_list[each_user])
    # print(topN_list)
from CustomerAc.Recom_package.基于关联规则的推荐算法.Apriori_update import *
import CustomerAc.Recom_package.基于关联规则的推荐算法.Apriori_update
def algorithm_3(file_path): #基于关联规则的推荐算法
    #file_path = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于关联规则的推荐算法\\data\\关联规则推荐数据2.txt"  # 别问 就改成“r”+绝对路径完事
    dataSet = CustomerAc.Recom_package.基于关联规则的推荐算法.Apriori_update.load_data(file_path)  # 计数
    print("                                                     ")
    print("用户-商品倒排列表: ", dataSet)
    data_count = first_num_count(dataSet)
    print("                                                     ")
    print("第1次剪枝前拓展项计数: ", data_count)
    data_num = len(dataSet)
    data, data_cut = cut_tree(data_count, data_num, 0.1)  # 剪枝 最小支持度0.X可更改
    print("第1次剪枝后拓展项计数: ", data)
    print("                                    ")
    K = 2
    while True:  # while K <= 3:
        data = move_cut(data, data_cut, K)
        print("第%d次拓展初始集合: %s" % (K, data))
        data_count = num_count(dataSet, data)  # 子集计数
        print("第%d次剪枝前拓展项计数: %s" % (K, data_count))
        if len(data_count) == 0:  # 如果无法拓展，表示已经完成，data为最后的拓展项集
            print("\n\t拓展结束")
            break
        data, data_cut = cut_tree(data_count, data_num, 0.1)  # 剪枝 最小支持度0.X可更改
        print("第%d次剪枝后拓展项计数: %s" % (K, data))
        # if len(data) == 0:  # 加一个break条件
        #     print("\n\t拓展结束")
        #     break
        print("                                    ")
        # print("第%d次被剪枝数据: %s" % (K, data_cut))
        K += 1

    goods = []
    for key, value in data.items():
        goods = key.split("、")
        num = value
    # 获取列表的非空子集
    print("                                                     ")
    print("强关联商品集合: ", goods)
    data_num = []
    for i in range(1, len(goods)):
        data_num += Combinations(goods, i)
    print("                                                     ")
    print("强关联商品的非空子集:", data_num)
    print("                                                     ")
    # 置信度计算
    for i in data_num:
        count = 0
        for u, v in dataSet.items():
            if set(i).issubset(list(v)):
                count += 1
        print(i, "置信度: ", float(num)/count)
    print("                                                     ")
from CustomerAc.Recom_package.社会化推荐算法.socialRecom import *
import CustomerAc.Recom_package.社会化推荐算法.socialRecom
def algorithm_10(friend_file,interest_file,userID):#社会化推荐算法
    #friend_file = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\社会化推荐算法\\data\\社交网络的推荐数据_好友.txt"
    #interest_file = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\社会化推荐算法\\data\\社交网络的推荐数据_爱好.txt"
    friends_data, interests_data = CustomerAc.Recom_package.社会化推荐算法.socialRecom.load_data(friend_file, interest_file)
    print("                                                     ")
    print("好友数据集: ", friends_data)
    print("兴趣数据集: ", interests_data)
    print("                                                     ")
    friends, interests = user_friend_interest(friends_data, interests_data)
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
from CustomerAc.Recom_package.基于图的推荐算法.Recomgraph import *
import CustomerAc.Recom_package.基于图的推荐算法.Recomgraph
def algorithm_7(file_path,UserID):#图推荐算法
    #file_path = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于图的推荐算法\\data\\基于图的推荐数据3.txt"
    records = CustomerAc.Recom_package.基于图的推荐算法.Recomgraph.load_data(file_path)
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
    taguser = UserID  # 设置初始节点，即用户id
    rank = PersonalRank(G, 0.85, taguser, 100)  # 以G为二分图，随机游走概率为0.85，初始节点为A，最大游走步数为100
    print("权重排名：", rank)
    rec = Recommend(taguser, rank, user_item)
    print("                                                     ")
    print("为目标用户%s推荐物品: %s" % (taguser, rec))
    print("                                                     ")
from CustomerAc.Recom_package.基于图的推荐算法.recomGraphLable import *
import CustomerAc.Recom_package.基于图的推荐算法.recomGraphLable
def algorithm_6(file_path,UserID):#图标签推荐算法
    #file_path = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于图的推荐算法\\data\\基于图标签的推荐数据2.txt"
    records = CustomerAc.Recom_package.基于图的推荐算法.recomGraphLable.load_data(file_path)
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
    taguser = UserID  # 设置初始节点，即用户id
    rank = PersonalRank(tag_G, 0.85, taguser, 100)  # 以tag_G为二分图，随机游走概率为0.85，初始节点为A，最大游走步数为100
    print("权重排名：", rank)
    print("                                                     ")
    rec = Recommend(taguser, rank, user_tag)
    print("为目标用户%s推荐的商品种类:%s " % (taguser, rec))  # 推荐的商品种类中会去除之前和目标用户有过行为的商品种类
    print("                                                     ")
from CustomerAc.Recom_package.基于时间上下文的推荐算法.recomItemCF import *
import CustomerAc.Recom_package.基于时间上下文的推荐算法.recomItemCF
def algorithm_4(file_path,UserID,TopNo,t1):#时间上下文推荐算法ItemCF
    #file_path = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于时间上下文的推荐算法\\data\\基于时间的推荐数据2.txt"
    dataSet = CustomerAc.Recom_package.基于时间上下文的推荐算法.recomItemCF.load_data(file_path)
    # print("数据集: ", dataSet)
    # print("----------------------------------------------------------------------------------------------------------")
    W = ItemSimilarity(dataSet, 0.85)  # 计算商品相似度
    # print("商品相似度: ", W)
    # print("----------------------------------------------------------------------------------------------------------")
    t = "2022-04-20 16:43:54"
    t = t1
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    t0 = int(time.mktime(timeArray))  # 将日期转为时间戳
    lastRank = Recommend(dataSet, UserID, W, TopNo, t0)  # 数据集，目标用户id，物品相似度，每种商品寻找K个相似的商品（剔除目标用户购买过的商品），t时间
    print("为目标用户推荐商品列表: ", list(lastRank.keys()))
    print("----------------------------------------------------------------------------------------------------------")
from CustomerAc.Recom_package.基于时间上下文的推荐算法.recomUserCF import *
import CustomerAc.Recom_package.基于时间上下文的推荐算法.recomUserCF
def algorithm_5(file_path,UserID,TopNo,t1):#时间上下文推荐算法UserCF
    #file_path = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于时间上下文的推荐算法\\data\\基于时间的推荐数据2.txt"
    dataSet = CustomerAc.Recom_package.基于时间上下文的推荐算法.recomUserCF.load_data(file_path)
    # print("数据集: ", dataSet)  # 注释
    # print("----------------------------------------------------------------------------------------------------------")  # 注释
    W = UserSimilarity(dataSet)  # 计算物品相似度
    # print("用户相似度: ", W)  # 注释
    # print("----------------------------------------------------------------------------------------------------------")  # 注释
    t = "2022-11-20 13:41:46"
    t=t1
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    t0 = int(time.mktime(timeArray))  # 将日期转为时间戳
    lastRank = Recommend(dataSet, UserID, W, TopNo, t0)  # 数据集，目标用户id，用户相似度，前K个相似用户，t时间
    print("                                                     ")
    print("为目标用户推荐商品列表: ", list(lastRank.keys()))
    print("                                                     ")
from CustomerAc.Recom_package.基于标签的推荐算法.RecomLable import *
import CustomerAc.Recom_package.基于标签的推荐算法.RecomLable
def algorithm_2(file_path,userID,topnum):#基于标签的推荐算法
    #file_path = u"./data/标签的推荐数据2.txt"
    records = CustomerAc.Recom_package.基于标签的推荐算法.RecomLable.load_data(file_path)
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
    rec = Recommend_update_2(userID, topnum)  # 向目标用户A推荐top3商品
    print("                                                     ")
    print("推荐商品: \n", rec)
    print("                                                     ")
from CustomerAc.Recom_package.基于用户的协同过滤推荐算法.recom_goods import *
import CustomerAc.Recom_package.基于用户的协同过滤推荐算法.recom_goods
def algorithm_8(file_path,UserID,topNum):#基于物品协同过滤
    #file_path = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于用户的协同过滤推荐算法\\data\\协同过滤的推荐数据2.csv"
    dataSet = CustomerAc.Recom_package.基于用户的协同过滤推荐算法.recom_goods.load_data(file_path)  # 产生数据集
    # print("\ndataSet: ", dataSet)
    userSet = calc_item_sim(dataSet)  # 对每种商品产生行为的用户列表
    # print("\nuserSet: ", userSet)
    itemSimi = item_similarity(dataSet)  # 计算物品相似度
    # print("\nuserSimi: ", itemSimi)
    lastRank = recommend(UserID, dataSet, itemSimi, topNum)  # 目标用户id为1，数据集，物品相似度，为目标用户喜欢的每个商品分别推荐K个相关度较高的商品
    print("                                                     ")
    print("为目标用户推荐商品: ", lastRank)
    print("                                                     ")
from CustomerAc.Recom_package.基于用户的协同过滤推荐算法.recom_users import *
import CustomerAc.Recom_package.基于用户的协同过滤推荐算法.recom_users
def algorithm_9(filePath,UserID,topNum):#基于用户协同过滤
    #filePath = r"C:\\Users\\jiaoj\\Desktop\\多种推荐算法\\Recommendation-System-master\\基于用户的协同过滤推荐算法\\data\\协同过滤的推荐数据2.csv"
    dataSet = CustomerAc.Recom_package.基于用户的协同过滤推荐算法.recom_users.load_data(filePath)  # 产生数据集
    # print("\ndataSet: ", dataSet)
    userSet = calc_user_sim(dataSet)  # 对每种商品产生行为的用户列表
    # print("\nuserSet: ", userSet)
    userSimi = user_similarity(userSet)  # 计算用户相似度
    # print("\nuserSimi: ", userSimi)
    lastRank = recommend(UserID, dataSet, userSimi, topNum)  # 目标用户id，数据集，用户相似度，与目标用户相似的K个用户（为目标用户推荐其未曾购买过的商品）
    print("                                                     ")
    print("为目标用户推荐的商品为: ", lastRank)
    print("                                                     ")