from methods import train, run
from data import datas

from sys import argv, exit
from getopt import getopt

   
if __name__ == '__main__':    
    user_id = 10
    no_training = False
    
    # runit from cmd
    try:
        options,args = getopt(argv[1:],"u:U:",["no-training"])
    except getopt.GetoptError:
        exit()    
    for name,value in options:
        if name in ("-u","-U"):
            user_id = int(value)
        if name in ("no-training"):
            no_training = True    
    
    # TODO: change to inner id        
    if no_training:
        run(datas, user_id)
    else:
        train(datas)
        run(datas, user_id)
    