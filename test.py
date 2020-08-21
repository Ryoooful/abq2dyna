import pandas as pd

path = r"C:\Temp\abq2dyna.inp"

class Node:
    id = []
    x  = []
    y  = []
    z  = []
    bool = False
    def start(self, line):
        if '*Node' == line:
            self.bool = True
        else:
            self.bool = False

    def append(self, spdata):
        if '*' in spdata[0]:
            self.bool = False
        
        if self.bool:
            self.id += [int(spdata[0])]
            self.x  += [float(spdata[1])]
            self.y  += [float(spdata[2])]
            self.z  += [float(spdata[3])]

    def dataframe(self):
        return pd.DataFrame(index=self.id, data={'x':self.x, 'y':self.y, 'z':self.z}, columns=['x', 'y', 'z'])


class Element:
    id      = []
    Types   = []
    Counts  = []
    Nodes   = []
    Type    = ""
    bool = False
    def start(self, line):
        if '*Element' in line:
            self.bool = True
            self.Type = spdata[1].split("=")[1] 
            
    def append(self, spdata):
        if '*' in spdata[0]:
            self.bool = False

        if self.bool:
            Temp_Nodes = []
            for st in spdata[1:]:
                Temp_Nodes.append(int(st.strip()))

            self.id     += [int(spdata[0])]
            self.Types  += self.Type
            self.Counts += [int(len(spdata)) - 1]
            self.Nodes  += [Temp_Nodes]

    def dataframe(self):
        return pd.DataFrame(index=self.id, data={'type':self.Types, 'count':self.Counts, 'nodes':self.Nodes}, columns=['type', 'count', 'nodes'])


node = Node()
element = Element()
with open(path) as f:
    lines = [s.strip() for s in  f.readlines()]
    for line in lines:
        if "**" in line:
            continue

        spdata = line.split(",")

        if "*" in line:
            node.start(line)
            element.start(line)
        else:
            node.append(spdata)
            element.append(spdata)
                


print (element.dataframe())