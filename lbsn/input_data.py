from lbsn_config import dataset_path, how_many_lines
from classes import User, POI, Activity
from data import datas

import os
import json

def change_to_inner_id(s):
    return int(s, 16)
def return_to_input_id(num):
    return str(hex(num))[2:]

# read & parse
def read_n_parse(datas=datas, dataset_pat=dataset_path, how_many_lines=how_many_lines):
    uiter = 0
    viter = 0
    users = {}
    pois = {}
    acts = []
    user_dict = {}
    poi_dict = {}

    path = os.path.realpath('__file__')
    #dir = path[:path.rfind('\\')+1]
    dir = path[:path.rfind('\\')+1] + 'lbsn\\'
    #with open(dir + "model\\parameters.json", "r") as file:
    with open(u"C:\\Users\\lmq\\Desktop\\biyesheji\\lbsn\\flasky\\lbsn\\model\\parameters.json") as file:
        d = json.load(file)
        datas['alpha'] = float(d.get('alpha', 0.2))
    
    i = 0
    with open(dataset_path, "rb") as file:
        while 1:
            
            i += 1
            
            if i > how_many_lines:
                break

            l = file.readline()
            if not l:
                break
            try:
                [a, b, c, d, e, f, g, h] = l.decode().split('\t')
            except:
                continue
                       
            uid = user_dict.get(a, uiter)
            if a not in user_dict:
                user_dict[a] = uid
                users[uid] = User(a)
                uiter += 1            
            vid = poi_dict.get(b, viter)
            if b not in poi_dict:
                poi_dict[b] = vid
                pois[vid] = POI(b, c, d, float(e), float(f), g)
                viter += 1            
            acts.append(Activity(uid, vid, h)) 
            
    datas["users"] = users
    datas["pois"] = pois
    datas["acts"] = acts
    datas["user_dict"] = user_dict
    datas["poi_dict"] = poi_dict
    return datas
    
def split_data(datas, i, n=5):
    if not datas['original_acts']:
        datas['original_acts'] = datas['acts']
    
    i = int(i)
    all_acts = datas['original_acts']
    step = int(len(all_acts) / n)
    # print("len(all_acts)=", len(all_acts), "step=", step)
    e_acts = all_acts[(i*step): ((i+1)*step)]
    acts = list(set(all_acts).difference(set(e_acts)))

    datas['acts'] = acts
    datas['e_acts'] = e_acts
    return datas
    
def rollback_data(datas=datas):
    if datas['original_acts']:
        datas['acts'] = datas['original_acts']
        datas['original_acts'] = None
        datas['e_acts'] = None
    return datas
    
if __name__ == '__main__':

    from data import datas
    datas = read_n_parse(datas)
    datas = split_data(datas, 1)
    print(len(datas['acts']), len(datas['e_acts']))
    datas = rollback_data(datas)
    print(len(datas['acts']))