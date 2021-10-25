
####################################
# TODO: override all three classes #
####################################


class User:
    def __init__(self, uid = ""):
        self.uid = uid
#		self.friends = np.array([])
#	def add_friend(self, fid):
#		self.friends = np.append(self.friends, fid)
    def __str__(self):
        return "User<%s>" % self.uid

class POI:
    def __init__(self, vid = "", vcid = "", vcname = "", lati = 0.0, lnti = 0.0, timeoff = 0):
        self.vid = vid
        self.vcid = vcid
        self.vcname = vcname
        self.lati = lati
        self.lnti = lnti
        self.timeoff = timeoff
    def __str__(self):
        # print "============="
        return "POI<%s>" % self.vid
        
class Activity:
    def __init__(self, uid = "", vid = "", when = None):
        self.uid = uid
        self.vid = vid
        self.when = when
    def __str__(self):
        return "User<%s> in POI<%s>" % (self.uid, self.vid)