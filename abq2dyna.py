import pandas as pd

input_path = r"C:\Temp\abq2dyna.inp"
output_path = r"C:\Users\1080045106\Desktop\dyna.k"


class Node:
    def __init__(self):
        self.node_id    = []
        self.x          = []
        self.y          = []
        self.z          = []
        self.bool       = False

    def isChecked(self, line):
        if '*Node' == line:
            self.bool = True
        else:
            self.bool = False

    def append(self, spdata):
        if self.bool:
            self.node_id += [int(spdata[0])]
            self.x  += [float(spdata[1]) * 1000]
            self.y  += [float(spdata[2]) * 1000]
            self.z  += [float(spdata[3]) * 1000]

    def df_node_id(self):
        df = pd.DataFrame(  index=self.node_id, 
                            data={'node_id':self.node_id, 'x':self.x, 'y':self.y, 'z':self.z}, 
                            columns=['node_id', 'x', 'y', 'z'])
        return df


class Element:
    def __init__(self):
        self.element_id         = []
        self.element_types      = []
        self.node_id            = []
        self.temp_element_id    = []
        self.temp_node_id       = []
        self.bool               = False

    def isChecked(self, spdata):
        self.bool = False
        if '*Element' == spdata[0]:
            self.bool = True
            self.element_type = str(spdata[1].split("=")[1].strip())

    def append(self, spdata):
        if self.bool:
            self.temp_id = int(spdata[0])
            self.element_id     += [int(self.temp_id)]
            self.element_types  += [self.element_type]
            temp = []
            for st in spdata[1:]:
                self.temp_element_id    += [int(self.temp_id)]
                self.node_id            += [int(st)]
                temp                    += [int(st)]  
            self.temp_node_id   += [temp]
    
    def df_element_id(self):
        df = pd.DataFrame(  index=self.element_id, 
                            data={'element_id':self.element_id, 'element_type':self.element_types, 'node_ids':self.temp_node_id}, 
                            columns=['element_id', 'element_type', 'node_ids'])
        return df
    
    def df_element_component(self):
        df = pd.DataFrame(  data={'eid':self.element_id, 'nid':self.node_id}, 
                            columns=['element_id', 'node_id'])
        return df


class Elset:
    def __init__(self):
        self.elset_names    = []
        self.instance_names = []
        self.internals      = []
        self.generates      = []
        self.temp_names     = []
        self.element_id        = []
        self.bool           = False

    def isChecked(self, spdata):
        self.elset_name      = ""
        self.instance_name  = ""
        self.internal       = False
        self.generate       = False
        self.bool           = False
        if '*Elset' == spdata[0].strip():
            self.bool = True
            for sp in spdata[1:]:
                if "elset=" in sp:
                    self.elset_name = str(sp.split("=")[1])
                elif "instance=" in sp:
                    self.instance_name = str(sp.split("=")[1])
                elif sp.strip() =="internal":
                    self.internal = True
                elif sp.strip() =="generate":
                    self.generate = True

            self.elset_names    += [str(self.elset_name)]
            self.instance_names += [str(self.instance_name)]
            self.internals      += [self.internal]
            self.generates      += [self.generate]

    def append(self, spdata):
        if self.bool:
            if self.generate:
                for st in range(int(spdata[0]), int(spdata[1]) + int(spdata[2]), int(spdata[2])):
                    self.temp_names     += [str(self.elset_name)]
                    self.element_id        += [int(st)]
            else:
                for st in spdata:
                    if st.strip() != "":
                        self.temp_names     += [str(self.elset_name)]
                        self.element_id     += [int(st)]

    def df_elset_name(self):
        df = pd.DataFrame(  index=self.elset_names, 
                            data={'elset_name':self.elset_names, 'instance_name':self.instance_names, 'generate':self.generates, 'internal':self.internals}, 
                            columns=['elset_name', 'instance_name', 'internal', 'generate'])
        return df

    def df_elset_component(self):
        df = pd.DataFrame(  data={'elset_name':self.temp_names , 'element_id':self.element_id}, 
                            columns=['elset_name', 'element_id'])
        return df


class Nset:
    def __init__(self):
        self.nset_names     = []
        self.instance_names = []
        self.internals      = []
        self.generates      = []
        self.temp_names     = []
        self.node_id        = []
        self.bool           = False
        
    def isChecked(self, spdata):
        self.nset_name      = ""
        self.instance_name  = ""
        self.internal       = False
        self.generate       = False
        self.bool           = False
        if '*Nset' == spdata[0].strip():
            self.bool = True
            for sp in spdata[1:]:                    
                if "nset=" in sp:
                    self.nset_name = str(sp.split("=")[1])
                elif "instance=" in sp:
                    self.instance_name = str(sp.split("=")[1])
                elif sp.strip() =="internal":
                    self.internal = True
                elif sp.strip() =="generate":
                    self.generate = True

            self.nset_names     += [self.nset_name]
            self.instance_names += [self.instance_name]
            self.internals      += [self.internal]
            self.generates      += [self.generate]

    def append(self, spdata):
        if self.bool:
            if self.generate:
                for st in range(int(spdata[0]), int(spdata[1]) + int(spdata[2]), int(spdata[2])):
                    self.temp_names     += [self.nset_name]
                    self.node_id        += [int(st)]
            else:
                for st in spdata:
                    if st.strip() != "":
                        self.temp_names += [self.nset_name]
                        self.node_id    += [str(st)]

    def df_nset_name(self):
        df = pd.DataFrame(  index=self.nset_names, 
                            data={'nset_name':self.nset_names, 'instance_name':self.instance_names, 'generate':self.generates, 'internal':self.internals}, 
                            columns=['nset_name', 'instance_name', 'internal', 'generate'])
        return df

    def df_nset_component(self):
        df = pd.DataFrame(  data={'nset_name':self.temp_names , 'node_id':self.node_id}, 
                            columns=['nset_name', 'node_id'])
        return df

class Solid:
    def __init__(self):
        self.solid_id       = []
        self.elset_names    = []
        self.material_names = []

    def isChecked(self, spdata):
        if '*Solid Section' == spdata[0].strip():
            self.solid_id             += [int(len(self.solid_id) + 1)]
            for sp in spdata[1:]:                    
                if "elset=" in sp:
                    self.elset_names  += [str(sp.split("=")[1])]
                elif "material=" in sp:
                    self.material_names += [str(sp.split("=")[1])]

    def df_solid_id(self):
        df = pd.DataFrame(  index=self.solid_id, 
                            data={'solid_id':self.solid_id, 'elset_name':self.elset_names, 'material_name':self.material_names}, 
                            columns=['solid_id', 'elset_name', 'material_name'])
        return df



class Surface:
    def __init__(self):
        self.bool           = False
        self.surface_id     = []
        self.surface_names  = []
        self.surface_types  = []
        self.temp_names     = []
        self.elset_name     = []
        self.identification = []
    def isChecked(self, spdata):
        self.bool = False
        if '*Surface' == spdata[0].strip():
            self.bool = True
            self.surface_name   = ""
            self.surface_type   = ""
            for sp in spdata[1:]:
                if "type=" in sp:
                    self.surface_type = str(sp.split("=")[1])
                elif "name=" in sp:
                    self.surface_name = str(sp.split("=")[1])
            self.sid            = int(len(self.surface_id)+1)
            self.surface_id     += [self.sid]
            self.surface_names  += [self.surface_name]
            self.surface_types  += [self.surface_type]
    
    def append(self, spdata):
        if self.bool:
            self.temp_names     += [self.surface_name]
            self.elset_name     += [str(spdata[0])]
            self.identification += [str(spdata[1])]

    def df_surface_name(self):
        df = pd.DataFrame(  index=self.surface_names,
                            data={'surface_name':self.surface_names, 'surface_id':self.surface_id, 'surface_type':self.surface_types}, 
                            columns=['surface_name', 'surface_id', 'surface_type'])
        return df

    def df_surface_component(self):
        df = pd.DataFrame(  data={'surface_name':self.temp_names, 'elset_name':self.elset_name, 'identification':self.identification}, 
                            columns=['surface_name', 'elset_name', 'identification'])
        return df

class Tie:
    def __init__(self):
        self.bool               = False
        self.tie_id             = []
        self.tie_names          = []
        self.adjust             = []
        self.slave_surfaces     = []
        self.master_surfaces    = []

    def isChecked(self, spdata):
        self.bool = False
        if '*Tie' == spdata[0].strip():
            self.bool           = True
            self.tie_name       = ""
            self.adjust_bool    = False
            for sp in spdata[1:]:
                if "name=" in sp:
                    self.tie_name = str(sp.split("=")[1])
                elif "adjust_bool=" in sp:
                    if str(sp.split("=")[1]) == "yes":
                        self.adjust_bool = True
            self.tie_id         +=  [len(self.tie_id) + 1]
            self.tie_names      +=  [self.tie_name]
            self.adjust    +=  [self.adjust_bool]

    def append(self, spdata):
        if self.bool:
            self.slave_surfaces     += [spdata[0].strip()]
            self.master_surfaces    += [spdata[1].strip()]
            self.bool = False

    def df_tie_name(self):
        df = pd.DataFrame(  index = self.tie_names,
                            data={'tie_id':self.tie_id, 'tie_name':self.tie_names, 'adjust':self.adjust, 'slave_surface':self.slave_surfaces, 'master_surface':self.master_surfaces}, 
                            columns=['tie_id', 'tie_name', 'adjust', 'slave_surface', 'master_surface'])
        return df


class Boundary:
    def __init__(self):
        self.bool               = False
        self.boundary_names     = []
        self.amplitude_names    = []
        self.u1                 = []
        self.u2                 = []
        self.u3                 = []
        self.ur1                = []
        self.ur2                = []
        self.ur3                = []
        self.u1_value           = []
        self.u2_value           = []
        self.u3_value           = []
        self.ur1_value          = []
        self.ur2_value          = []
        self.ur3_value          = []


    def isChecked(self, spdata):
        self.bool = False
        if '*Boundary' == spdata[0].strip():
            self.bool              = True
            self.amplitude_name    = ""
            for sp in spdata[1:]:
                if "amplitude=" in sp:
                    self.amplitude_name = str(sp.split("=")[1])

            self.amplitude_names      +=  [self.amplitude_name]


class Coupling:
    def __init__(self):
        self.bool = False
        





def get_node_on_surface(element_type, identification, node_ids):
    if element_type == "C3D4":
        if identification == "S1":
            return [node_ids[2], node_ids[1], node_ids[0]]
        elif identification == "S2":
            return [node_ids[1], node_ids[3] ,node_ids[0]]
        elif identification == "S3":
            return [node_ids[2], node_ids[3], node_ids[1]]
        elif identification == "S4":
            return [node_ids[0], node_ids[3], node_ids[2]]



node = Node()
element = Element()
nset = Nset()
elset = Elset()
solid = Solid()
surface = Surface()
tie = Tie()
with open(input_path) as f:
    lines = [s.strip() for s in  f.readlines()]
    for index, line in enumerate(lines):
        if "**" in line:
            continue

        spdata = line.split(",")

        if "*" in line:
            node.isChecked(line)
            element.isChecked(spdata)
            nset.isChecked(spdata)
            elset.isChecked(spdata)
            solid.isChecked(spdata)
            surface.isChecked(spdata)
            tie.isChecked(spdata)
        else:
            node.append(spdata)
            element.append(spdata)
            nset.append(spdata)
            elset.append(spdata)
            surface.append(spdata)
            tie.append(spdata)




with open(output_path, mode='w') as f:

    df_solid_id = solid.df_solid_id()

    for index, row in df_solid_id.iterrows():
        f.write("*SECTION_SOLID_TITLE\n")
        f.write(str(row.elset_name) + "\n")
        f.write('{0: > #10}'.format(row.solid_id))      
        f.write('{0: > #10}'.format(10))                
        f.write("\n")
    
    for index, row in df_solid_id.iterrows():
        f.write("*PART\n")
        f.write(str(row.elset_name) + "\n")
        f.write('{0: > #10}'.format(row.solid_id))
        f.write('{0: > #10}'.format(row.solid_id))
        f.write('{0: > #10}'.format(0))
        f.write("\n")
    
    f.write("*Node\n")
    df_node_id = node.df_node_id()
    for index, row in df_node_id.iterrows():
        f.write('{0: > #8}'.format(int(row.node_id)))
        for st in row[1:]:
            f.write('{0:0< #16f}'.format(float(st)))
        f.write("\n")
    
    f.write("*ELEMENT_SOLID\n")
    df_elset_component = elset.df_elset_component()
    df_element_id = element.df_element_id()
    df_solid_component = pd.merge(df_solid_id, df_elset_component, on='elset_name', how='left')
    df_part_component = pd.merge(df_solid_component, df_element_id, on='element_id', how='left')

    for index, row in df_part_component.iterrows():
        f.write('{0: > #8}'.format(row.element_id))
        f.write('{0: > #8}'.format(row.solid_id))
        f.write("\n")
        for st in row.node_ids:
            f.write('{0: > #8}'.format(st))

        if len(row.node_ids) < 8:
            for n in range(len(row.node_ids)+1, 9):
                f.write('{0: > #8}'.format(row.node_ids[len(row.node_ids)-1]))
        f.write("\n")
    
    df_surface_name = surface.df_surface_name()
    df_surface_component = surface.df_surface_component()
    df_temptable = pd.merge(df_surface_component, df_elset_component, on='elset_name', how='left')
    df_segment_component = pd.merge(df_temptable, df_element_id, on='element_id', how='left')

    df_tie_name = tie.df_tie_name()

    for index, sid in df_surface_name.iterrows():
        f.write("*SET_SEGMENT\n")
        f.write('{0: > #10}'.format(sid.surface_id))
        f.write("\n")
        for index, row in df_segment_component[df_segment_component['surface_name'] == sid.surface_name].iterrows():
            temp_nodes = get_node_on_surface(row.element_type.strip(), row.identification.strip(), row.node_ids)
            for st in temp_nodes:
                f.write('{0: > #10}'.format(st))
            if len(temp_nodes) < 4:
                for n in range(len(temp_nodes), 4):
                    f.write('{0: > #10}'.format(temp_nodes[len(temp_nodes) - 1]))
            f.write("\n")

    for index, row in df_tie_name.iterrows():
        f.write("*CONTACT_TIED_SURFACE_TO_SURFACE_ID\n")
        f.write('{0: > #10}'.format(row.tie_id))
        f.write("\n")
        f.write('{0: > #10}'.format(df_surface_name.loc[row.slave_surface]['surface_id']))
        f.write('{0: > #10}'.format(df_surface_name.loc[row.master_surface]['surface_id']))
        f.write('{0: > #10}'.format(0))
        f.write('{0: > #10}'.format(0))
        f.write("\n")
        f.write('{0: > #50}'.format(20))
        f.write("\n")






    f.write("*END")

