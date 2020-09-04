import pandas as pd
input_path = r"C:\Users\1080045106\Desktop\p"
output_path = r"C:\Users\1080045106\Desktop\dyna.key"


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
                        try:
                            id = int(st.strip())
                            self.temp_names += [self.nset_name]
                            self.node_id    += [id]
                        except:
                            df = pd.DataFrame(  data={'nset_name':self.temp_names , 'node_id':self.node_id}, 
                                                columns=['nset_name', 'node_id'])
                            for index, row in df[df['nset_name'] == st.strip()].iterrows():
                                self.temp_names += [self.nset_name]
                                self.node_id    += [int(row.node_id)]

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
            self.surface_id     += [len(self.surface_id)+1]
            self.surface_names  += [self.surface_name]
            self.surface_types  += [self.surface_type]
    
    def append(self, spdata):
        if self.bool:
            self.temp_names     += [self.surface_name]
            self.elset_name     += [str(spdata[0])]
            self.identification += [str(spdata[1])]

    def df_surface_name(self):
        df = pd.DataFrame(  index=self.surface_names,
                            data={'surface_id':self.surface_id, 'surface_name':self.surface_names, 'surface_type':self.surface_types}, 
                            columns=['surface_id', 'surface_name', 'surface_type'])
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
        df = pd.DataFrame(  index=self.tie_names,
                            data={'tie_id':self.tie_id, 'tie_name':self.tie_names, 'adjust':self.adjust, 'slave_surface':self.slave_surfaces, 'master_surface':self.master_surfaces}, 
                            columns=['tie_id', 'tie_name', 'adjust', 'slave_surface', 'master_surface'])
        return df

class Constraint:
    def __init__(self):
        self.constraint_id      = []
        self.constraint_names   = []
        self.nset_names         = []
        self.surface_names     = []
        
    def isChecked(self, spdata):
        if '*Coupling' == spdata[0].strip():
            self.surface_name      = ""
            self.nset_name          = ""
            self.constraint_name    = ""
            for sp in spdata[1:]:
                if "constraint name=" in sp:
                    self.constraint_name = str(sp.split("=")[1])
                elif "ref node=" in sp:
                    self.nset_name = str(sp.split("=")[1])
                elif "surface=" in sp:
                    self.surface_name = str(sp.split("=")[1])
            self.constraint_id      +=  [len(self.constraint_id) + 1]
            self.constraint_names   +=  [self.constraint_name]
            self.nset_names         +=  [self.nset_name]
            self.surface_names     +=  [self.surface_name]

    def df_constraint_name(self):
        df = pd.DataFrame(  index=self.constraint_names,
                            data={'constraint_id':self.constraint_id, 'constraint_name':self.constraint_names, 'nset_name':self.nset_names, 'surface_name':self.surface_names}, 
                            columns=['constraint_id', 'constraint_name', 'nset_name', 'surface_name'])
        return df


class Material:
    def __init__(self):
        self.bool = False
        self.material_id    = []
        self.material_names = []
        self.conductivity_list   = []
        self.density_list        = []
        self.young_list          = []
        self.poason_list         = []
        self.expansion_list      = []
        self.specific_heat_list  = []
        self.ogden_list          = []

    def isChecked(self, spdata):
        self.before_line = ""
        if '*Material' == spdata[0].strip():
            self.bool = True
            self.material_name = ""
            self.conductivity = 0
            self.density = 0
            self.young = 0
            self.poason = 0
            self.expansion = 0
            self.specific_heat = 0
            self.ogden = []            
            for sp in spdata[1:]:
                if "name=" in sp:
                    self.material_name = str(sp.split("=")[1])

        elif spdata[0].strip() in ['*Conductivity', '*Density', '*Elastic', '*Expansion', '*Specific?Heat', '*Hyperelastic']:
            self.before_line = spdata[0].strip()
        else:
            if self.bool:
                self.material_id         += [len(self.material_id) + 1]
                self.material_names      += [self.material_name]
                self.conductivity_list   += [self.conductivity]
                self.density_list        += [self.density]
                self.young_list          += [self.young]
                self.poason_list         += [self.poason]
                self.expansion_list      += [self.expansion]
                self.specific_heat_list  += [self.specific_heat]
                self.ogden_list          += [self.ogden]
            self.bool = False
        
    def append(self, spdata):
        if self.bool:
            if self.before_line == '*Conductivity':
                self.conductivity = float(spdata[0].strip())
            elif self.before_line == '*Density':    
                self.density = float(spdata[0].strip())
            elif self.before_line == '*Elastic':
                self.young = float(spdata[0].strip())
                self.poason = float(spdata[1].strip())
            elif self.before_line == '*Expansion':
                self.expansion = float(spdata[0].strip())
            elif self.before_line == '*Specific?Heat':
                self.specific_heat = float(spdata[0].strip())
            elif self.before_line == '*Hyperelastic':
                self.ogden += [float(st) for st in spdata[:6]]
            self.before_line = ""

    def df_material_name(self):
        df = pd.DataFrame(  index=self.material_names,
                            data={'material_id':self.material_id, 'material_name':self.material_names, 'conductivity':self.conductivity_list, 'density':self.density_list, 'young':self.young_list, 'poason':self.poason_list, 'specific_heat':self.specific_heat_list, 'ogden':self.ogden_list}, 
                            columns=['material_id', 'material_name', 'conductivity', 'density', 'young', 'poason', 'specific_heat', 'ogden'])
                            
        return df






class Boundary:
    def __init__(self):
        self.bool               = False
        self.amplitude_name     = ""
        self.amplitude_names    = []
        self.step_names         = []
        self.nset_names         = []
        self.u1                 = []
        self.u2                 = []
        self.u3                 = []
        self.ur1                = []
        self.ur2                = []
        self.ur3                = []
        self.u1v                = []
        self.u2v                = []
        self.u3v                = []
        self.ur1v               = []
        self.ur2v               = []
        self.ur3v               = []
        self.lists              = []

    def isChecked(self, spdata, step_name):
        if self.bool:
            self.step_names         += [step_name]
            self.amplitude_names    += [self.amplitude_name]
            self.nset_names         += [self.lists[0]]
            self.u1                 += [self.lists[1]]
            self.u2                 += [self.lists[2]]
            self.u3                 += [self.lists[3]]
            self.ur1                += [self.lists[4]]
            self.ur2                += [self.lists[5]]
            self.ur3                += [self.lists[6]]
            self.u1v                += [self.lists[7]]
            self.u2v                += [self.lists[8]]
            self.u3v                += [self.lists[9]]
            self.ur1v               += [self.lists[10]]
            self.ur2v               += [self.lists[11]]
            self.ur3v               += [self.lists[12]]
            self.bool = False

        if '*Boundary' == spdata[0].strip():
            self.bool = True
            self.amplitude_name     = ""
            for sp in spdata[1:]:
                if "amplitude=" in sp:
                    self.amplitude_name = str(sp.split("=")[1])
            self.lists = ["" , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            #self.lists = {"nset_name":"" ,"u1":False , "u2":False , "u3":False, "ur1":False, "ur2":False, "ur3":False, "u1v":0, "u2v":0, "u3v":0, "ur1v":0, "ur2v":0, "ur3v":0}
        
        

    def append(self, spdata):
        if self.bool:
            self.lists[0] = spdata[0].strip()
            self.lists[int(spdata[1].strip())] = 1
            if len(spdata) == 4:
                self.lists[int(spdata[1].strip()) + 6] = float(spdata[3].strip())

    def df_boundary_name(self):
        df = pd.DataFrame(  data={'step_name':self.step_names, 'amplitude':self.amplitude_names, 'nset_name':self.nset_names, 'u1':self.u1, 'u2':self.u2, 'u3':self.u3, 'ur1':self.ur1, 'ur2':self.ur2, 'ur3':self.ur3, 'u1v':self.u1v, 'u2v':self.u2v, 'u3v':self.u3v, 'ur1v':self.ur1v, 'ur2v':self.ur2v, 'ur3v':self.ur3v}, 
                            columns=['step_name', 'amplitude', 'nset_name', 'u1', 'u2', 'u3', "ur1", "ur2", "ur3", "u1v", "u2v", "u3v", "ur1v", "ur2v", "ur3v"])
        return df


class Step:
    def __init__(self):
        self.bool               = False
        self.step_name          = ""

    def isChecked(self, spdata):
        boundary.isChecked(spdata, self.step_name)
        if '*Step' == spdata[0].strip():
            self.bool               = True
            for sp in spdata[1:]:
                if "name=" in sp:
                    self.step_name = str(sp.split("=")[1])
            return
        elif '*End Step' == spdata[0].strip():
            self.bool               = False
            self.step_name          = ""
            return

    def append(self, spdata):
        boundary.append(spdata)




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
    elif element_type == "S3R":
        return [node_ids[0], node_ids[1], node_ids[2]]

def get_elform(element_type, ogden):
    if element_type == "C3D4":
        if len(ogden) == 0:
            return 10
        else:
            return 13






def get_node_on_translation(row):
    if row.u1 == 1 and row.u2 == 0 and row.u3 == 0:
        return 1
    elif row.u1 == 0 and row.u2 == 1 and row.u3 == 0:
        return 2
    elif row.u1 == 0 and row.u2 == 0 and row.u3 == 1:
        return 3
    elif row.u1 == 1 and row.u2 == 1 and row.u3 == 0:
        return 4
    elif row.u1 == 0 and row.u2 == 1 and row.u3 == 1:
        return 5
    elif row.u1 == 1 and row.u2 == 0 and row.u3 == 1:
        return 6
    elif row.u1 == 1 and row.u2 == 1 and row.u3 == 1:
        return 7
    else:
        return 0

def get_node_on_rotaion(row):
    if row.ur1 == 1 and row.ur2 == 0 and row.ur3 == 0:
        return 1
    elif row.ur1 == 0 and row.ur2 == 1 and row.ur3 == 0:
        return 2
    elif row.ur1 == 0 and row.ur2 == 0 and row.ur3 == 1:
        return 3
    elif row.ur1 == 1 and row.ur2 == 1 and row.ur3 == 0:
        return 4
    elif row.ur1 == 0 and row.ur2 == 1 and row.ur3 == 1:
        return 5
    elif row.ur1 == 1 and row.ur2 == 0 and row.ur3 == 1:
        return 6
    elif row.ur1 == 1 and row.ur2 == 1 and row.ur3 == 1:
        return 7
    else:
        return 0


node = Node()
element = Element()
nset = Nset()
elset = Elset()
solid = Solid()
surface = Surface()
tie = Tie()
boundary = Boundary()
step = Step()
constraint = Constraint()
material = Material()
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
            step.isChecked(spdata)
            constraint.isChecked(spdata)
            material.isChecked(spdata)
        else:
            node.append(spdata)
            element.append(spdata)
            nset.append(spdata)
            elset.append(spdata)
            surface.append(spdata)
            tie.append(spdata)
            step.append(spdata)
            material.append(spdata)


with open(output_path, mode='w') as f:

    df_solid_id = solid.df_solid_id()
    df_material_name = material.df_material_name()

    df_elset_component = elset.df_elset_component()
    df_element_id = element.df_element_id()
    df_solid_component = pd.merge(df_solid_id, df_elset_component, on='elset_name', how='left')
    df_part_component = pd.merge(df_solid_component, df_element_id, on='element_id', how='left')
    #print(df_part_component[['solid_id','elset_name','material_name','element_type']].groupby('solid_id').max())
    for index, secid in df_part_component[['solid_id','elset_name','material_name','element_type']].groupby('solid_id').max().iterrows():
        f.write("*SECTION_SOLID_TITLE\n")

        f.write(str(secid.elset_name) + "\n")
        f.write('{0: > #10}'.format(index))

        for aaa, mat in df_material_name[df_material_name['material_name'] == secid.material_name].iterrows():
            f.write('{0: > #10}'.format(get_elform(secid.element_type, mat.ogden)))
            f.write("\n")
            if len(mat.ogden) == 0:
                f.write("*MAT_ELASTIC_TITLE\n")
                f.write(secid.material_name)
                f.write("\n")
                f.write('{0: > #10}'.format(mat.material_id))
                f.write('{0: > #10}'.format(mat.density))       #ro
                f.write('{0: > #10}'.format(mat.young))         #e
                f.write('{0: > #10}'.format(mat.poason))        #pr
                f.write("\n")
            else:
                f.write("*MAT_OGDEN_RUBBER_TITLE\n")
                f.write(secid.material_name)
                f.write("\n")
                f.write('{0: > #10}'.format(mat.material_id))
                f.write('{0: > #10}'.format(mat.density))       #ro
                f.write('{0: > #10}'.format(0.499))             #pr
                f.write('{0: > #10}'.format(0))                 #n
                f.write('{0: > #10}'.format(3))                 #nv
                f.write('{0: > #10}'.format(1))                 #g
                f.write('{0: > #10}'.format(0.001))             #sigf
                f.write('{0: > #10}'.format(0))                 #g
                f.write("\n")
                f.write('{0: > #10}'.format(mat.ogden[0]))
                f.write('{0: > #10}'.format(mat.ogden[2]))
                f.write('{0: > #10}'.format(mat.ogden[4]))
                f.write('{0: > #10}'.format(0))
                f.write('{0: > #10}'.format(0))
                f.write('{0: > #10}'.format(0))
                f.write("\n")
                f.write('{0: > #10}'.format(mat.ogden[1]))
                f.write('{0: > #10}'.format(mat.ogden[3]))
                f.write('{0: > #10}'.format(mat.ogden[5]))
                f.write('{0: > #10}'.format(0))
                f.write('{0: > #10}'.format(0))
                f.write('{0: > #10}'.format(0))     
                f.write("\n")

                #*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID

            f.write("*PART\n")
            f.write(str(secid.elset_name) + "\n")
            f.write('{0: > #10}'.format(index))
            f.write('{0: > #10}'.format(index))
            f.write('{0: > #10}'.format(mat.material_id))
            f.write("\n")
        f.write("\n")


    
    f.write("*Node\n")
    df_node_id = node.df_node_id()
    df_nset_component = nset.df_nset_component()
    
    df_boundary_name = boundary.df_boundary_name()
    df_temptable = pd.merge(df_boundary_name, df_nset_component, on='nset_name', how='inner')[['node_id','u1', 'u2', 'u3', "ur1", "ur2", "ur3"]].groupby('node_id').max()
    df_node_component = pd.merge(df_node_id, df_temptable, on='node_id', how='left')

    for index, row in df_node_component.iterrows():
        f.write('{0: > #8}'.format(int(row.node_id)))
        f.write('{0:0< #16f}'.format(float(row.x)))
        f.write('{0:0< #16f}'.format(float(row.y)))
        f.write('{0:0< #16f}'.format(float(row.z)))
        f.write('{0:0< #16f}'.format(float(get_node_on_translation(row))))
        f.write('{0:0< #16f}'.format(float(get_node_on_rotaion(row))))
        f.write("\n")
    
    f.write("*ELEMENT_SOLID\n")
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
        f.write("\n")

    df_constraint_name = constraint.df_constraint_name()

    for index, pid in df_constraint_name.iterrows():
        f.write("*SET_NODE_TITLE\n")
        f.write(pid.surface_name)
        f.write("\n")
        f.write(str(pid.constraint_id))
        f.write("\n")
        temp_nodes = []
        for index, row in df_segment_component[df_segment_component['surface_name'] == pid.surface_name].iterrows():
            temp_nodes += [nid for nid in get_node_on_surface(row.element_type.strip(), row.identification.strip(), row.node_ids)]
        temp_nodes = list(set(temp_nodes))
        temp_nodes.sort()
        for index, st in enumerate(temp_nodes):
            f.write('{0: > #10}'.format(st))
            if (index + 1) % 8 == 0:
                f.write("\n")
        f.write("\n")


        f.write("*CONSTRAINED_NODAL_RIGID_BODY_SPC_TITLE\n")
        f.write(pid.constraint_name)
        f.write("\n")
        f.write('{0: > #10}'.format(pid.constraint_id))
        f.write('{0: > #10}'.format(0))
        f.write('{0: > #10}'.format(pid.constraint_id))
        f.write("\n")
        f.write(' 1.0000000         5         7')
        f.write("\n")
        
        ##*BOUNDARY_PRESCRIBED_MOTION_RIGID_ID




    f.write("*END")

