 # -*- coding:utf-8 -*-  
from input_data import read_n_parse
from data import datas

import seaborn as sns
import pandas as pd
import os
'''
数据集整体分析：
	1.用户访问位置数的分布：<10, 10~20, .. (柱状图)
	2.位置的被访问频次的分布：<10, 10~100 ....(柱状图)

局部查询：
	用户id：访问了的位置id，位置的被访问次数
	'''
def draw_all_distribution(datas=datas, ufpath=None, pfpath=None):
# users-pois pois-users
    datas = read_n_parse(datas)
    u = [0] * len(datas["users"])
    p = [0] * len(datas["pois"])
    for act in datas["acts"]:
        u[act.uid] += 1
        p[act.vid] += 1

    '''
    users_graph = sns.jointplot(x="weizhishu",#"用户访问不同位置数", \
                                y="geshu",#用户个数", \
                                data=pd.DataFrame(u))
    '''
    path = os.path.realpath('__file__')
    dir = path[:path.rfind('\\')+1]

    u = pd.Series(u, name=u"user visited places")
    users_graph = sns.distplot(u)
    users_graph.get_figure().savefig(dir + "graphs\\users_distribution.png")
    #users_graph.get_figure().savefig(dir + "lbsn\\graphs\\users_distribution.png")


    p = pd.Series(p, name=u"places being visited")
    pois_graph = sns.distplot(p)    
    pois_graph.get_figure().savefig(dir + "graphs\\pois_distribution.png")    
    #pois_graph.get_figure().savefig(dir + "lbsn\\graphs\\pois_distribution.png")    
    
    
    # after draw two pictures
    # return [absolute] path
    path = os.path.realpath('__file__')
    dir = path[:path.rfind('\\')+1]
    '''
    return (dir + "graphs\\users_distribution.png",
            dir + "graphs\\pois_distribution.png")
    '''
    return (dir + "lbsn\\graphs\\users_distribution.png",
            dir + "lbsn\\graphs\\pois_distribution.png")
    
    
def draw_user_distribution(datas=datas, user_id=10, fpath=None):   
    datas = read_n_parse(datas)     
    ud = {}
    for act in datas["acts"]:
        if act.uid == user_id:
            ud[act.vid] = ud.get(act.vid, 0) + 1
    vids, times = [], []
    for v, t in ud.items():
        vids.append(v)
        times.append(t)
    vids = pd.Series(vids)
    times = pd.Series(times)
    ud = pd.DataFrame({"vids": vids, "times": times})

    ax = sns.barplot(x='vids', y='times', data=ud)        
    ax.get_figure().savefig("graphs\\user_" + str(user_id) + "_distribution.png")

    path = os.path.realpath('__file__')
    dir = path[:path.rfind('\\')+1]
    return dir + "graphs\\user_" + str(user_id) + "_distribution.png"
    
    '''
    datas = read_n_parse(datas) 
    ud = {'user_id':{}}
    for act in datas["acts"]:
        if act.uid == user_id:
            ud['user_id']['u'+str(act.vid)] = ud['user_id'].get('u'+str(act.vid), 0) + 1
    
    df_data = pd.DataFrame(ud).sort_values('user_id', ascending=False)
    print(df_data)
    sns.set_color_codes("muted")
    ax = sns.barplot(x='user_id', y=df_data.index, data=df_data, label='user_id')
    ax.get_figure().savefig("graphs\\user_" + str(user_id) + "_distribution.png")

    path = os.path.realpath('__file__')
    dir = path[:path.rfind('\\')+1]
    return dir + "graphs\\user_" + str(user_id) + "_distribution.png"
    '''

    
def draw_poi_distribution(datas=datas, poi_id=10, fpath=None):    
    datas = read_n_parse(datas)    
    ud = {}
    for act in datas["acts"]:
        if act.vid == poi_id:
            ud[act.uid] = ud.get(act.uid, 0) + 1
    uids, times = [], []
    for u, t in ud.items():
        uids.append(u)
        times.append(t)
    uids = pd.Series(uids)
    times = pd.Series(times)
    ud = pd.DataFrame({"uids": uids, "times": times})

    ax = sns.barplot(x='uids', y='times', data=ud)        
    ax.get_figure().savefig("graphs\\poi_" + str(poi_id) + "_distribution.png")

    path = os.path.realpath('__file__')
    dir = path[:path.rfind('\\')+1]
    return dir + "graphs\\poi_" + str(poi_id) + "_distribution.png"


if __name__ == "__main__":
    draw_all_distribution()
    draw_user_distribution()
    draw_poi_distribution()