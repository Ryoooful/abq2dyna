import pandas as pd

input_path = r"C:\Temp\abq2dyna.inp"
output_path = r"C:\Users\1080045106\Desktop\dynaa.k"


class Node:
    def __init__(self):
        self.id = []
        self.x  = []
        self.y  = []
        self.z  = []
        self.bool = False

    def isChecked(self, line):
        if '*Node' == line:
            self.bool = True
        else:
            self.bool = False

    def append(self, spdata):
        if '*' in spdata[0]:
            self.bool = False
        
        if self.bool:
            self.id += [int(spdata[0])]
            self.x  += [float(spdata[1]) * 1000]
            self.y  += [float(spdata[2]) * 1000]
            self.z  += [float(spdata[3]) * 1000]

    def dataframe(self):
        df = pd.DataFrame(index=self.id, data={'nid':self.id, 'x':self.x, 'y':self.y, 'z':self.z}, columns=['nid', 'x', 'y', 'z'])
        return df


class Element:
    def __init__(self):
        self.eid            = []
        self.element_names  = []
        self.array_nid      = []
        self.temp_eid       = []
        self.nid            = []
        self.bool           = False

    def isChecked(self, spdata):
        if '*Element' == spdata[0]:
            self.bool = True
            self.element_name = spdata[1].split("=")[1].strip()
        else:
            self.bool = False

    def append(self, spdata):
        if self.bool:
            self.id = int(spdata[0])
            self.eid            += [self.id]
            self.element_names  += [self.element_name]
            temp = []
            for st in spdata[1:]:
                self.temp_eid   += [self.id]
                self.nid        += [int(st.strip())]
                temp            += [int(st.strip())]  
            self.array_nid += [temp]
            

    
    def df_element_id(self):
        df = pd.DataFrame(index=self.eid, data={'eid':self.eid, 'element_name':self.element_names, 'nid':self.array_nid}, columns=['eid', 'element_name', 'nid'])
        return df
    
    def df_element_node(self):
        df = pd.DataFrame(data={'eid':self.temp_eid, 'nid':self.nid}, columns=['eid', 'nid'])
        return df


class Segment:
    def __init__(self):
        self.bool = False
        self.segment_types          = []
        self.segment_names          = []
        self.instance_names         = []
        self.internals              = []
        self.generates              = []

        self.temp_segment_names     = []
        self.nid                    = []

        self.generate = False
        
    def isChecked(self, spdata):
        if self.bool:
            self.bool = False

        if '*Nset' == spdata[0].strip() or '*Elset' == spdata[0].strip():
            self.bool = True
            self.segment_name = ""
            self.instance_name = ""
            self.internal = False
            self.generate = False

            self.segment_type = spdata[0].strip()
            for sp in spdata[1:]:                    
                if "nset=" in sp or "elset=" in sp:
                    self.segment_name = sp.split("=")[1]
                elif "instance=" in sp:
                    self.instance_name = sp.split("=")[1]
                elif sp.strip() =="internal":
                    self.internal = True
                elif sp.strip() =="generate":
                    self.generate = True

            self.segment_names  += [self.segment_name]
            self.segment_types  += [self.segment_type]
            self.instance_names += [self.instance_name]
            self.internals      += [self.internal]
            self.generates      += [self.generate]

    def append(self, spdata):
        if self.bool:
            if self.generate:
                for st in range(int(spdata[0]), int(spdata[1]) + 1, int(spdata[2])):
                    self.temp_segment_names += [self.segment_name]
                    self.nid                += [st]

            else:
                for st in spdata:
                    if st.strip() != "":
                        self.temp_segment_names += [self.segment_name]
                        self.nid                += [st]

    def df_segment_name(self):
        df = pd.DataFrame(index=self.segment_names, 
                            data={'segment_name':self.segment_names, 'segment_type':self.segment_types, 'instance_name':self.instance_names, 'generate':self.generates, 'internal':self.internals}, 
                            columns=['segment_name', 'segment_type', 'instance_name', 'internal', 'generate'])
        return df

    def df_segment_node(self):
        df = pd.DataFrame(data={'segment_name':self.temp_segment_names , 'id':self.nid}, 
                            columns=['segment_name', 'id'])
        return df

class Solid:
    def __init__(self):
        self.segment_id     = []
        self.segment_names  = []
        self.material_names = []

    def isChecked(self, spdata):
        if '*Solid Section' == spdata[0].strip():
            self.segment_id             += [len(self.segment_id) + 1]
            for sp in spdata[1:]:                    
                if "nset=" in sp or "elset=" in sp:
                    self.segment_names  += [sp.split("=")[1]]
                elif "material=" in sp:
                    self.material_names += [sp.split("=")[1]]

    def df_solid_name(self):
        df = pd.DataFrame(index=self.segment_id, data={'segment_id':self.segment_id, 'segment_name':self.segment_names, 'material_name':self.material_names}, 
                            columns=['segment_id', 'segment_name', 'material_name'])
        return df


node = Node()
element = Element()
segment = Segment()
solid = Solid()
with open(input_path) as f:
    lines = [s.strip() for s in  f.readlines()]
    for line in lines:
        if "**" in line:
            continue

        spdata = line.split(",")

        if "*" in line:
            node.isChecked(line)
            element.isChecked(spdata)
            segment.isChecked(spdata)
            solid.isChecked(spdata)
        else:
            node.append(spdata)
            element.append(spdata)
            segment.append(spdata)
            
nodes = node.dataframe()
elements = element.df_element_id()
segments = segment.df_segment_node()
solids = solid.df_solid_name()


temp_elements = pd.merge(solids, segments, on='segment_name', how='left').drop(columns='segment_name').drop(columns='material_name').rename(columns={'id':'eid'}).rename(columns={'segment_id':'pid'})
temp_elements['eid'] = temp_elements['eid'].astype(int)
temp = pd.merge(temp_elements, elements, on='eid')

#print(temp)

with open(output_path, mode='w') as f:

    for index, row in solids.iterrows():
        f.write("*SECTION_SOLID_TITLE\n")
        f.write(str(row[1]) + "\n")
        f.write('{0: > #10}'.format(index)) #secid
        f.write('{0: > #10}'.format(10))        #elform メッシュ種類
        f.write("\n")

    for index, row in solids.iterrows():
        seid = index
        f.write("*PART\n")
        f.write(str(row[1]) + "\n")
        f.write('{0: > #10}'.format(seid))
        f.write('{0: > #10}'.format(seid))
        f.write('{0: > #10}'.format(0))
        f.write("\n")

    f.write("*Node\n")
    for index, row in nodes.iterrows():
        f.write('{0: > #8}'.format(int(row[0])))
        for st in row[1:]:
            f.write('{0:0< #16f}'.format(float(st)))
        f.write("\n")
    
    f.write("*ELEMENT_SOLID\n")
    for index, row in temp.iterrows():
        f.write('{0: > #8}'.format(row.eid))
        f.write('{0: > #8}'.format(row.pid))
        f.write("\n")
        for st in row.nid:
            f.write('{0: > #8}'.format(st))
        f.write('{0: > #8}'.format(row[3][3]))
        f.write('{0: > #8}'.format(row[3][3]))
        f.write('{0: > #8}'.format(row[3][3]))
        f.write('{0: > #8}'.format(row[3][3]))
        f.write("\n")

    f.write("*END")
        
        


