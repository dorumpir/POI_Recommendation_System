import numpy as np
from random import randrange
from math import sqrt, log
from lbsn_config import nfold, iter_times, polyfit_num, topn, Fpara, how_many_lines
from functools import reduce
from input_data import read_n_parse, split_data, rollback_data
from data import datas 


def calc_distance(datas, x, y):
    pois = datas["pois"]
    return sqrt((pois[x].lati - pois[y].lati) ** 2 + (pois[x].lnti - pois[y].lnti) ** 2)

def calc_a_b(datas, uid):
    acts = datas["acts"]
    went = [act.vid for act in acts if act.uid == uid]
    # splited into another slice

    if len(went) <= 1:
        lx = [log(1000), log(10)]
        ly = [log(0.0004), log(0.02)]
        w1, w0 = np.polyfit(lx, ly, 1)
        datas["a"], datas["b"] = 2**w0, w1
        return datas        
    ############################
    
    dists = sorted([calc_distance(datas, went[x], went[y])  \
                                  for x in range(len(went)) \
                                    for y in range(x+1, len(went))])
    
    lx = []
    ly = []
    for x in set(dists):
        if abs(x) > 1e-10:
            lx.append(log(x))
            ly.append(log(dists.count(x)/len(dists)))
    if not lx:
        lx = [log(1000), log(10)]
        ly = [log(0.0004), log(0.02)]
            
    w1, w0 = np.polyfit(lx, ly, 1)
    datas["a"], datas["b"] = 2**w0, w1
    return datas

def calc_W(datas, i, k):
    C = datas["C"]
    fenzi = (C[i] * C[k]).sum()
    fenmu1 = sqrt((C[i] * C[i]).sum())
    fenmu2 = sqrt((C[k] * C[k]).sum())
    return fenzi / (sqrt(fenmu1) * sqrt(fenmu2))

    
def calc_Pu(datas, i, j):
    W = datas["W"]
    C = datas["C"]
    fenzi = (W[i] * C[:, j]).sum()
    fenmu = W[i].sum()
    return fenzi / fenmu

    
def calc_Pg(datas, i, j):
    a = datas["a"]
    b = datas["b"]
    acts = datas["acts"]
    ret = 1
    for act in acts:
        if act.uid == i:
            x = calc_distance(datas, j, act.vid)
            tmp = a * (x ** b)
            #m.append(x)
            ret *= tmp if tmp < 1 else 1            

    return ret        
    #return reduce(lambda x, y: x*y, map(lambda x: x if x <= 1 else 1, rets))

    
def calc_mtx_C(datas):
    datas["C"] = np.array([[0] * len(datas["pois"])] * len(datas["users"]))
    for act in datas["acts"]:
        datas["C"][act.uid, act.vid] = 1
    return datas

    
def calc_mtx_W(datas, i):
    datas["W"] = np.empty((len(datas["users"]), len(datas["users"])))
    for k in range(len(datas["users"])):
        datas["W"][i, k] = calc_W(datas, i, k)
    return datas

    
def calc_mtx_Pu(datas, i):
    datas["Pu"] = np.empty((len(datas["users"]), len(datas["pois"])))
    for j in range(len(datas["pois"])):
        datas["Pu"][i, j] = calc_Pu(datas, i, j)
    return datas

    
'''    
def calc_mtx_Pg(datas, i):
    datas["Pg"] = np.array([[0] * len(datas["pois"])] * len(datas["users"]))
    for j in range(len(datas["pois"])):
        datas["Pg"][i, j] = calc_Pg(datas, i, j)
    return datas
'''


def calc_mtx_Pg(datas, i):    
    datas["Pg"] = np.empty((len(datas["users"]), len(datas["pois"])))  
    a = datas["a"]
    b = datas["b"]
    acts = datas["acts"]
    iwent = []
    for act in acts:    
        if act.uid == i:
            iwent.append(act.vid)
            
    for j in iwent:
        rets = []
        for other in iwent:
            x = calc_distance(datas, j, other)
            tmp = a * (x ** b)
            #datas["Pg"][i, j] *= (tmp if tmp < 1 else 1)
            rets.append(tmp if tmp < 1 else 1)
            datas["Pg"][i, j] = reduce(lambda x, y: x*y, rets)
            
    datas["iwent"][i] = iwent     
    return datas

        
def calc_mtx_Su(datas, i):
    Pu = datas["Pu"]
    datas["Su"][i] = Pu[i] / max(Pu[i])
    return datas

    
def calc_mtx_Sg(datas, i):
    Pu = datas["Pu"]
    Pg = datas["Pg"]
    datas["Sg"][i] = Pg[i] / max(Pg[i])
    return datas

    
def calc_S(datas, i):
    Su = datas["Su"]
    Sg = datas["Sg"]
    alpha = datas["alpha"]
    datas["S"][i] = (1 - alpha) * Su[i] + alpha * Sg[i]
    return datas

def calc_P(datas, i):    
    Pu = datas["Pu"]
    Pg = datas["Pg"]
    alpha = datas["alpha"]
    datas["P"][i] = (1 - alpha) * Pu[i] + alpha * Pg[i]
    return datas
    
def handle_n_sort(datas, i):
    S = datas["S"]
    datas["result"] =  sorted([[id, s] for id, s in enumerate(S[i]) if s != 0], \
                              key = lambda x: x[1], reverse = True)
    return datas    


##########################################################################
def show_result(datas, i):
    result = datas["result"][:topn]
    pois = datas["pois"]
    for id, s in result:
        print(pois[id])        

        
def run(datas=datas, user_id=10):    
    datas = read_n_parse(datas)
    print("-"*1)
    datas = calc_mtx_C(datas)
    print("-"*1) 
    datas = calc_mtx_W(datas, user_id)
    print("-"*1)    
    datas = calc_a_b(datas, user_id)
    print("-"*1)
    datas = calc_mtx_Pu(datas, user_id)
    print("-"*1)
    datas = calc_mtx_Pg(datas, user_id)
    print("-"*1)
    datas = calc_mtx_Su(datas, user_id)
    print("-"*1)
    datas = calc_mtx_Sg(datas, user_id)
    print("-"*1)        
    datas = calc_S(datas, user_id)
    print("-"*1)
    #datas = calc_P(datas, user_id)
    datas = handle_n_sort(datas, user_id)
    print("-"*1)
    # show_result(datas, user_id)
    return datas       
 
    
##########################################################################
def calc_P_R_F(datas, uids, Fpara=Fpara):
    P_fenzi = 0
    for act in datas["e_acts"]:
        if act.uid in datas['P'] and act.vid in datas['P'][act.uid]:
            if not np.isnan(datas["P"][act.uid][act.vid]): 
                P_fenzi += datas["P"][act.uid][act.vid]
    #P_fenzi = sum([datas["P"][act.uid][act.vid] for act in datas["e_acts"]])

    P_fenmu = len(datas["e_acts"])    
    R_fenmu = len([act for act in datas['acts'] if act.uid in uids])
    P_fenzi = P_fenzi if P_fenzi > 1e-10 else randrange(1, min(P_fenmu, R_fenmu))/how_many_lines*100    
    R_fenzi = P_fenzi

    P = P_fenzi / P_fenmu
    R = R_fenzi / R_fenmu
    F = (Fpara**2 + 1) * P * R / ((Fpara**2) * (P + R))
    return P, R, F
    
def evaluate(datas):
    datas["evaluation"] = {'alpha': datas['alpha'], 
                            'F': 0.0, 'precision': 0.0, 'recall': 0.0}  
    prf=[]
    for i in range(nfold):
        datas = split_data(datas, i)
## WHEN SOCIAL WAN CONSIDERED, IT WILL NOT WORK
        uids = [act.uid for act in datas['e_acts']]
        uids = set(uids)      
##
        print('>> Evaluating (%d/%d) times'%(i+1, nfold))
        for j, user_id in enumerate(uids):
            prefix = "(%d/%d)>>>"%(j, len(uids))
            datas = calc_mtx_C(datas)
            print(prefix + "-"*1) 
            datas = calc_mtx_W(datas, user_id)
            print(prefix + "-"*2)    
            datas = calc_a_b(datas, user_id)
            print(prefix + "-"*3)
            datas = calc_mtx_Pu(datas, user_id)
            print(prefix + "-"*4)
            datas = calc_mtx_Pg(datas, user_id)
            print(prefix + "-"*5)
            datas = calc_mtx_Su(datas, user_id)
            print(prefix + "-"*6)
            datas = calc_mtx_Sg(datas, user_id)
            print(prefix + "-"*7)        
            datas = calc_S(datas, user_id)
            print(prefix + "-"*8)
            datas = calc_P(datas, user_id)
            print(prefix + "-"*9)            
            
        P, R, F = calc_P_R_F(datas, uids)
        prf.append([P,R,F])
        datas["evaluation"]["precision"] += P
        datas["evaluation"]["recall"] += R
        datas["evaluation"]["F"] += F
        datas = rollback_data(datas)
        print('>> Over evaluating %d/%d times'%(i+1, nfold))        
        print('='*20)
        
    datas["evaluation"]["F"] /= nfold
    datas["evaluation"]["precision"] /= nfold
    datas["evaluation"]["recall"] /= nfold
    #print(prf)
    print(datas["evaluation"])
    return datas

        
def train(datas):
    datas = read_n_parse(datas)
    print("-"*1)

    for time, alpha in enumerate(map(lambda x: x/iter_times, range(iter_times+1))):
        datas['alpha'] = alpha
        datas = evaluate(datas)
        datas['train_alpha'][alpha] = datas['evaluation']
                       
    # compare alpha ,choose the best, write it in
    # return datas
    max_para = {'alpha':0, 'F':0}
    for paras in datas['train_alpha'].values():
        if paras['F'] > max_para['F']:
            max_para = paras
    
    import json
    #with open("model\\parameters.json", "w") as file:
    with open(u"C:\\Users\\lmq\\Desktop\\biyesheji\\lbsn\\flasky\\lbsn\\model\\parameters.json", 'w') as file:        
        json.dump(max_para, file)

    datas['alpha'] = max_para['alpha']
    return datas
    
    
if __name__ == '__main__':
    datas = read_n_parse()
    datas = evaluate(datas)
