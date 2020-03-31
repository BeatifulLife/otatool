class swVersion:
    def __init__(self,projectstr,versionstr,custom):
        self.projectstr=projectstr
        self.versionstr=versionstr
        self.custom=custom
        self.version=None
        self.localotadir=None
        self.localdeltadir=None
        self.project=None
        self.chip=None
        self.platform='MTK'
        self.mtk_custom="/mnt/data/Custom_MTK/"
        self.spr_custom="/mnt/data/Custom_SPR/"
        self.spr_project=["A","B","C","E","P","R"]
        self.platformmap={
             "a708":self.spr_custom+"A708-L",
             "K102":self.mtk_custom+"K102-L",
             "K116":self.mtk_custom+"K116-L",
             "K707":self.mtk_custom+"K707-L",
             "K801":self.mtk_custom+"K801-L",
             "K805":self.mtk_custom+"K805-L",
             "K960":self.mtk_custom+"K960-L",
             "S960":self.mtk_custom+"S960-L",
             "ZH960":self.mtk_custom+"ZH960-K"}

    def analyze(self):
        if self.projectstr is None:
            print("软件项目为空")
            return
        prostrs=self.projectstr.split("_")
        if len(prostrs)==4:
            self.version=prostrs[3]
            self.project=prostrs[0]
            self.chip=prostrs[1]

    def getVersion(self):
        return self.version

    def getProject(self):
        return self.project

    def getChip(self):
        return self.chip

    def getPlatform(self):
        if self.project is None:
            print("项目为空")
            return
        for i in self.spr_project:
            if self.project.startswith(i):
                self.platform="SPR"
                break
        return self.platform

    def getLocalotadir(self):
        if self.platform is not None:
            if self.platform=="MTK":
                self.localotadir=self.mtk_custom+self.project.upper()+"-"+self.version.upper()+"/"+self.custom+"/"+self.versionstr
            elif self.platform=="SPR":
                self.localotadir=self.spr_custom+self.project.upper()+"-"+self.version.upper()+"/"+self.custom+"/"+self.versionstr
        else:
            for i in self.platformmap.keys():
                if self.projectstr == i:
                    self.localotadir=self.platformmap[i]+"/"+self.custom+"/"+self.versionstr
                    break
        return self.localotadir

    def getLocaldeltadir(self):
        if self.platform is not None:
            if self.platform=="MTK":
                self.localdeltadir=self.mtk_custom+self.project.upper()+"-"+self.version.upper()+"/"+self.custom+"/delta"
            elif self.platform=="SPR":
                self.localdeltadir=self.spr_custom+self.project.upper()+"-"+self.version.upper()+"/"+self.custom+"/delta"
        else:
            for i in self.platformmap.keys():
                if self.projectstr == i:
                    self.localdeltadir=self.platformmap[i]+"/"+self.custom+"/delta"
                    break
        return self.localdeltadir
            
                
        
