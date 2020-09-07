import pandas as pd
input_path = r"C:\temp\abq2dyna.inp"
keyword = ""

abaqus = {
    "t_node_id":            {"node_id":[], "x":[], "y":[], "z":[]},
    "t_element_id":         {"element_id":[], "element_type":[], "node_ids":[]},
    "t_element_component":  {"element_id":[], "node_id":[]},
    "t_elset_name":         {"elset_name":[], "instance_name":[], "generate":[], "internal":[]},
    "t_elset_component":    {"elset_name":[], "element_id":[]},
    "t_nset_name":          {"nset_name":[], "instance_name":[], "generate":[], "internal":[]},
    "t_nset_component":     {"nset_name":[], "node_id":[]},
    "t_solid_id":           {"solid_id":[], "elset_name":[], "material_name":[]},
    "t_tie_name":           {"tie_id":[], "tie_name":[], "adjust":[], "slave_surface":[], "master_surface":[]},
    "t_constraint_name":    {"constraint_id":[], "constraint_name":[], "nset_name":[], "surface_name":[]},
    "t_material_name":      {"material_id":[], "material_name":[], "hyperelastic":[], "conductivity":[], "density":[], "young":[], "poason":[], "specific_heat":[]},
    "t_step_name":          {"step_name":[], "step_id":[]}
        }


def get_name(name_label, spdata):
    for sp in spdata[1:]:
        if name_label + "=" in sp:
            return str(sp.split("=")[1])
    return ""

def get_bool(label, spdata, yesno):
    for sp in spdata[1:]:
        if yesno:
            if label + "=" in sp:
                if sp.split("=")[1] == "yes":
                    return True
        else:
            if label == sp:
                return True
    return False



def create_table(table):
    return pd.DataFrame(data=table, columns=table.keys())

#df.iloc[0][column_name]

with open(input_path) as f:
    lines = [s.strip() for s in f.readlines()]


#Read Code .inp
for line in lines:
    ##Skip Comment Text
    if "**" == line[:2]:
        continue
    
    spdata = [s.strip() for s in line.split(",")]
    
    ##Save Keyword
    if "*" == spdata[0][:1]:
        keyword = spdata[0]
        if "*Solid Section" == keyword:
            abaqus["t_solid_id"]["solid_id"]                += [len(abaqus["t_solid_id"]["solid_id"])]
            abaqus["t_solid_id"]["elset_name"]              += [get_name("elset", spdata)]
            abaqus["t_solid_id"]["material_name"]           += [get_name("material", spdata)]
        elif "*Coupling" == keyword:
            abaqus["t_constraint_name"]["constraint_id"]    += [len(abaqus["t_constraint_name"]["constraint_id"])]
            abaqus["t_constraint_name"]["constraint_name"]  += [get_name("constraint name", spdata)]
            abaqus["t_constraint_name"]["nset_name"]        += [get_name("ref node", spdata)]
            abaqus["t_constraint_name"]["surface_name"]     += [get_name("surface", spdata)]
        elif "*Element" == keyword:
            element_type = get_name("type", spdata)
        elif "*Elset" == keyword:
            elset_name = get_name("elset", spdata)
            elset_generate = get_bool("generate", spdata, False)
            abaqus["t_elset_name"]["elset_name"]            += [elset_name]
            abaqus["t_elset_name"]["instance_name"]         += [get_name("instance", spdata)]
            abaqus["t_elset_name"]["generate"]              += [elset_generate]
            abaqus["t_elset_name"]["internal"]              += [get_bool("internal", spdata, False)]
        elif "*Nset" == keyword:
            nset_name = get_name("nset", spdata)
            nset_generate = get_bool("generate", spdata, False)
            abaqus["t_nset_name"]["nset_name"]              += [nset_name]
            abaqus["t_nset_name"]["instance_name"]          += [get_name("instance", spdata)]
            abaqus["t_nset_name"]["generate"]               += [nset_generate]
            abaqus["t_nset_name"]["internal"]               += [get_bool("internal", spdata, False)]
        elif "*Tie" == keyword:
            abaqus["t_tie_name"]["tie_id"]                  += [len(abaqus["t_tie_name"]["tie_id"])]
            abaqus["t_tie_name"]["tie_name"]                += [get_name("name", spdata)]
            abaqus["t_tie_name"]["adjust"]                  += [get_bool("adjust", spdata, True)]
        elif "*Material" == keyword:
            material_name = get_name("name", spdata)
            abaqus["t_material_name"]["material_id"]        += [len(abaqus["t_material_name"]["material_id"])]
            abaqus["t_material_name"]["material_name"]      += [material_name]
            abaqus["t_material_name"]["hyperelastic"]       += []
            for col in [st for st in abaqus["t_material_name"].keys()][2:]:
                abaqus["t_material_name"][col] += [0]
        elif "*Step" == keyword: 
            step_name = get_name("name", spdata)
            abaqus["t_step_name"]["step_id"]                += [len(abaqus["t_step_name"]["step_id"])]
            abaqus["t_step_name"]["step_name"]              += [step_name]
        elif "*End Step" == keyword: 
            step_name = ""

        continue

    ##Append Data
    if   keyword == "*Node":
        abaqus["t_node_id"]["node_id"]                   += [int(spdata[0])]
        abaqus["t_node_id"]["x"]                         += [float(spdata[1]) * 1000]
        abaqus["t_node_id"]["y"]                         += [float(spdata[2]) * 1000]
        abaqus["t_node_id"]["z"]                         += [float(spdata[3]) * 1000]
    elif keyword == "*Element":
        abaqus["t_element_id"]["element_id"]             += [int(spdata[0])]
        abaqus["t_element_id"]["element_type"]           += [element_type]
        abaqus["t_element_id"]["node_ids"]               += [[int(st) for st in spdata[1:] if st.isdecimal()]]
        abaqus["t_element_component"]["element_id"]      += [int(spdata[0])  for st in spdata[1:]]
        abaqus["t_element_component"]["node_id"]         += [int(st) for st in spdata[1:]]
    elif keyword == "*Elset":        
        if elset_generate:
            abaqus["t_elset_component"]["elset_name"]    += [elset_name  for st in range(int(spdata[0]), int(spdata[1]) + int(spdata[2]), int(spdata[2]))]
            abaqus["t_elset_component"]["element_id"]    += [int(st)     for st in range(int(spdata[0]), int(spdata[1]) + int(spdata[2]), int(spdata[2]))]
        else:
            abaqus["t_elset_component"]["elset_name"]    += [elset_name  for st in spdata if st.isdecimal()]
            abaqus["t_elset_component"]["element_id"]    += [int(st)     for st in spdata if st.isdecimal()]
    elif keyword == "*Nset":  
        if nset_generate:
            abaqus["t_nset_component"]["nset_name"]      += [nset_name  for st in range(int(spdata[0]), int(spdata[1]) + int(spdata[2]), int(spdata[2]))]
            abaqus["t_nset_component"]["node_id"]        += [int(st)     for st in range(int(spdata[0]), int(spdata[1]) + int(spdata[2]), int(spdata[2]))]
        else:
            for st in spdata:
                if st.isdecimal():
                    abaqus["t_nset_component"]["nset_name"]      += [nset_name]
                    abaqus["t_nset_component"]["node_id"]        += [int(st)]
                else:
                    tmp = create_table(abaqus["t_nset_component"])
                    for index, row in tmp[tmp["nset_name"] == nset_name].reset_index().iterrows():
                        abaqus["t_nset_component"]["nset_name"]  += [nset_name]
                        abaqus["t_nset_component"]["node_id"]    += [int(row.node_id)]
                    del tmp
    elif keyword == "*Tie":  
        abaqus["t_tie_name"]["slave_surface"]          += [spdata[0]]
        abaqus["t_tie_name"]["master_surface"]         += [spdata[1]]
    elif keyword == "*Conductivity": 
        abaqus["t_material_name"]["conductivity"][len(abaqus["t_material_name"]["conductivity"]) - 1]     = [spdata[0]]
    elif keyword == "*Density": 
        abaqus["t_material_name"]["density"][len(abaqus["t_material_name"]["density"]) - 1]               = [spdata[0]]
    elif keyword == "*Elastic": 
        abaqus["t_material_name"]["young"][len(abaqus["t_material_name"]["young"]) - 1]                   = [spdata[0]]
        abaqus["t_material_name"]["poason"][len(abaqus["t_material_name"]["poason"]) - 1]                 = [spdata[1]]
    elif keyword == "*Specific Heat": 
        abaqus["t_material_name"]["specific_heat"][len(abaqus["t_material_name"]["specific_heat"]) - 1]   = [spdata[0]]
    elif keyword == "*Hyperelastic": 
        abaqus["t_material_name"]["hyperelastic"][len(abaqus["t_material_name"]["hyperelastic"]) - 1]     = [float(st) for st in spdata[:6]]
        keyword = ""

for st in abaqus.keys():
    abaqus[st] = create_table(abaqus[st])

#Convert .k 
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

lsdyna = {
    "t_nid":            {"nid":[], "x":[], "y":[], "z":[], "tc":[], "rc":[]},
    "t_eid":            {"eid":[], "pid":[], "n1":[], "n2":[], "n3":[], "n4":[], "n5":[], "n6":[], "n7":[], "n8":[]},
    "t_secid_solid":    {"secid":[], "title":[], "elform":[] },
    "t_part_id":        {"pid":[], "heading":[], "secid":[], "mid":[]},
    "t_mid_ogden":      {"mid":[], "ro":[]},
    "t_mid_elastics":   {"mid":[], "ro":[], "e":[], "pr":[]},
    "t_cid_exterior":   {"cid":[], "":[]},
    "t_sid_nset":       {},
    "t_pid_rigid":      {},
    "t_bid_rigid":      {},
    "t_bid_node":       {},
    "t_lcid":           {},
    "t_sid_segment":    {},
    "t_cid_surface":    {},
    "t_vid":            {}
        }

abaqus["q_solid_component"] = pd.merge(abaqus["t_solid_id"], abaqus["t_elset_component"], on='elset_name', how='left')
abaqus["q_part_component"] = pd.merge(abaqus["q_solid_component"], abaqus["t_element_id"], on='element_id', how='left')

print(abaqus["q_part_component"][['solid_id','elset_name','material_name','element_type']].groupby('solid_id').max().reset_index())
