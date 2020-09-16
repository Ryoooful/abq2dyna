import pandas as pd
input_path = r"C:\temp\abq2dyna.inp"
keyword = ""

abaqus = {
    "t_node_id":            {"node_id":[], "x":[], "y":[], "z":[]},
    "t_element_id":         {"element_id":[], "element_type":[], "node_ids":[]},
    "t_element_component":  {"element_id":[], "node_id":[]},
    "t_elset_name":         {"elset_id":[], "elset_name":[], "instance_name":[], "generate":[], "internal":[]},
    "t_elset_component":    {"elset_name":[], "element_id":[]},
    "t_nset_name":          {"nset_id":[], "nset_name":[], "instance_name":[], "generate":[], "internal":[]},
    "t_nset_component":     {"nset_name":[], "node_id":[]},
    "t_solid_id":           {"solid_id":[], "elset_name":[], "material_name":[]},
    "t_tie_name":           {"tie_id":[], "tie_name":[], "adjust":[], "slave_surface":[], "master_surface":[]},
    "t_surface_name":       {"surface_id":[], "surface_name":[], "surface_type":[]},
    "t_surface_component":  {"surface_name":[], "elset_name":[], "identification":[]},
    "t_constraint_name":    {"constraint_id":[], "constraint_name":[], "nset_name":[], "surface_name":[]},
    "t_material_name":      {"material_id":[], "material_name":[], "hyperelastic":[], "conductivity":[], "density":[], "young":[], "poason":[], "specific_heat":[]},
    "t_transform_name":     {"nset_name":[], "type":[], "x1":[], "y1":[], "z1":[], "x2":[], "y2":[], "z2":[]},
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
            abaqus["t_solid_id"]["solid_id"]                += [len(abaqus["t_solid_id"]["solid_id"]) + 1]
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
            abaqus["t_elset_name"]["elset_id"]              += [len(abaqus["t_elset_name"]["elset_id"]) + 1]
            abaqus["t_elset_name"]["elset_name"]            += [elset_name]
            abaqus["t_elset_name"]["instance_name"]         += [get_name("instance", spdata)]
            abaqus["t_elset_name"]["generate"]              += [elset_generate]
            abaqus["t_elset_name"]["internal"]              += [get_bool("internal", spdata, False)]
        elif "*Nset" == keyword:
            nset_name = get_name("nset", spdata)
            nset_generate = get_bool("generate", spdata, False)
            abaqus["t_nset_name"]["nset_id"]                += [len(abaqus["t_nset_name"]["nset_id"]) + 1]
            abaqus["t_nset_name"]["nset_name"]              += [nset_name]
            abaqus["t_nset_name"]["instance_name"]          += [get_name("instance", spdata)]
            abaqus["t_nset_name"]["generate"]               += [nset_generate]
            abaqus["t_nset_name"]["internal"]               += [get_bool("internal", spdata, False)]
        elif "*Tie" == keyword:
            abaqus["t_tie_name"]["tie_id"]                  += [len(abaqus["t_tie_name"]["tie_id"])]
            abaqus["t_tie_name"]["tie_name"]                += [get_name("name", spdata)]
            abaqus["t_tie_name"]["adjust"]                  += [get_bool("adjust", spdata, True)]
        elif "*Surface" == keyword:
            surface_name = get_name("name", spdata)
            abaqus["t_surface_name"]["surface_id"]          += [len(abaqus["t_surface_name"]["surface_id"]) + 1]
            abaqus["t_surface_name"]["surface_name"]        += [surface_name]
            abaqus["t_surface_name"]["surface_type"]        += [get_name("type", spdata)]
        elif "*Transform" == keyword:
            abaqus["t_transform_name"]["nset_name"]         += [get_name("nset", spdata)]
            abaqus["t_transform_name"]["type"]              += [get_name("type", spdata)]
        elif "*Material" == keyword:
            material_name = get_name("name", spdata)
            abaqus["t_material_name"]["material_id"]        += [len(abaqus["t_material_name"]["material_id"]) + 1]
            abaqus["t_material_name"]["material_name"]      += [material_name]
            abaqus["t_material_name"]["hyperelastic"]       += [[]]
            for col in [st for st in abaqus["t_material_name"].keys()][3:]:
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
    elif keyword == "*Tie":  
        abaqus["t_tie_name"]["slave_surface"]            += [str(spdata[0])]
        abaqus["t_tie_name"]["master_surface"]           += [str(spdata[1])]
    elif keyword == "*Surface":  
        abaqus["t_surface_component"]["surface_name"]    += [surface_name]
        abaqus["t_surface_component"]["elset_name"]      += [str(spdata[0])]
        abaqus["t_surface_component"]["identification"]  += [str(spdata[1])]
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
            abaqus["t_nset_component"]["node_id"]        += [int(st)    for st in range(int(spdata[0]), int(spdata[1]) + int(spdata[2]), int(spdata[2]))]
        else:
            for st in spdata:
                if st.isdecimal() and st != "":
                    abaqus["t_nset_component"]["nset_name"]      += [nset_name]
                    abaqus["t_nset_component"]["node_id"]        += [int(st)]
                else:
                    tmp = create_table(abaqus["t_nset_component"])
                    for index, row in tmp[tmp["nset_name"] == st].reset_index().iterrows():
                        abaqus["t_nset_component"]["nset_name"]  += [nset_name]
                        abaqus["t_nset_component"]["node_id"]    += [int(row.node_id)]
                    del tmp
    elif keyword == "*Transform": 
        for index, st in enumerate([col for col in abaqus["t_transform_name"].keys()][2:]):
            abaqus["t_transform_name"][st] += [float(spdata[index - 2])]

    elif keyword == "*Conductivity": 
        abaqus["t_material_name"]["conductivity"][len(abaqus["t_material_name"]["conductivity"]) - 1]     = float(spdata[0])
    elif keyword == "*Density": 
        abaqus["t_material_name"]["density"][len(abaqus["t_material_name"]["density"]) - 1]               = float(spdata[0])
    elif keyword == "*Elastic": 
        abaqus["t_material_name"]["young"][len(abaqus["t_material_name"]["young"]) - 1]                   = float(spdata[0])
        abaqus["t_material_name"]["poason"][len(abaqus["t_material_name"]["poason"]) - 1]                 = float(spdata[1])
    elif keyword == "*Specific Heat": 
        abaqus["t_material_name"]["specific_heat"][len(abaqus["t_material_name"]["specific_heat"]) - 1]   = float(spdata[0])
    elif keyword == "*Hyperelastic": 
        abaqus["t_material_name"]["hyperelastic"][len(abaqus["t_material_name"]["hyperelastic"]) - 1]     = [float(st) for st in spdata[:6]]
        keyword = ""

for st in abaqus.keys():
    abaqus[st] = create_table(abaqus[st])




#Convert .k 


def get_node_on_translation(row):
    if   row.u1 == 1 and row.u2 == 0 and row.u3 == 0:
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
    if   row.ur1 == 1 and row.ur2 == 0 and row.ur3 == 0:
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
    "t_secid_solid":    {"secid":[], "title":[], "elform":[]},
    "t_part_id":        {"pid":[], "heading":[], "secid":[], "mid":[]},
    "t_mid_ogden":      {"mid":[], "ro":[], "pr":[], "mu1":[], "alpha1":[], "mu2":[], "alpha2":[], "mu3":[], "alpha3":[]},
    "t_mid_elastics":   {"mid":[], "ro":[], "e":[], "pr":[]},
    "t_cid_exterior":   {"cid":[], "ssid":[], "msid":[], "sstyp":[], "mstyp":[]},
    "t_sid":            {"sid":[], "type":[]},
    "t_sid_component":  {"sid":[], "nid":[]},
    "t_pid_rigid":      {"pid":[], "cid":[], "nsid":[], "sstyp":[], "mstyp":[]},
    "t_bid_rigid":      {},
    "t_bid_node":       {},
    "t_lcid":           {"lcid":[]},
    "t_lcid_time":      {"lcid":[], "a1":[], "o1":[]},
    "t_sid_segment":    {"sid":[], "nid1":[], "nid2":[], "nid3":[], "nid4":[]},
    "t_cid_surface":    {"cid":[], "ssid":[], "msid":[], "sstyp":[], "mstyp":[]},
    "t_vid":            {}
        }

abaqus["q_solid_component"] = pd.merge(abaqus["t_solid_id"], abaqus["t_elset_component"], on='elset_name', how='left')
abaqus["q_part_component"] = pd.merge(abaqus["q_solid_component"], abaqus["t_element_id"], on='element_id', how='left')

tmp = abaqus["q_part_component"][['solid_id','elset_name','material_name','element_type']].groupby('solid_id').max().reset_index()
tmp.index = tmp.index + 1
for secid, row in tmp.iterrows():
    mat = abaqus["t_material_name"][abaqus["t_material_name"]['material_name'] == row.material_name].iloc[0]
    lsdyna["t_secid_solid"]["secid"]    += [row.solid_id]
    lsdyna["t_secid_solid"]["title"]    += [row.elset_name]
    if row.element_type == "C3D4":
        if len(mat["hyperelastic"]) == 0:
            lsdyna["t_secid_solid"]["elform"]   += [10]
        else:
            lsdyna["t_secid_solid"]["elform"]   += [13]

    lsdyna["t_part_id"]["pid"]          += [row.solid_id]
    lsdyna["t_part_id"]["heading"]      += [row.elset_name]
    lsdyna["t_part_id"]["secid"]        += [row.solid_id]
    lsdyna["t_part_id"]["mid"]          += [mat["material_id"] + 1]
    lsdyna["t_cid_exterior"]["cid"]     += [row.solid_id]
    lsdyna["t_cid_exterior"]["ssid"]    += [row.solid_id]
    lsdyna["t_cid_exterior"]["msid"]    += [3]
    lsdyna["t_cid_exterior"]["sstyp"]   += [0]
    lsdyna["t_cid_exterior"]["mstyp"]   += [0]
    if len(mat["hyperelastic"]) > 1:
        lsdyna["t_mid_ogden"]["mid"]    += [mat["material_id"] + 1]
        lsdyna["t_mid_ogden"]["ro"]     += [float(mat["density"])]
        lsdyna["t_mid_ogden"]["pr"]     += [0.499]
        for index, st in enumerate([col for col in lsdyna["t_mid_ogden"].keys()][3:]):
            lsdyna["t_mid_ogden"][st] += [float(mat["hyperelastic"][index - 3])]
    else:
        lsdyna["t_mid_elastics"]["mid"]    += [mat["material_id"] + 1]
        lsdyna["t_mid_elastics"]["ro"]     += [float(mat["density"])]
        lsdyna["t_mid_elastics"]["e"]      += [float(mat["young"])]
        lsdyna["t_mid_elastics"]["pr"]     += [float(mat["poason"])]
del tmp


for eid, row in abaqus["q_part_component"].iterrows():
    lsdyna["t_eid"]["eid"]     += [row.element_id]
    lsdyna["t_eid"]["pid"]     += [row.solid_id]
    for n, st in enumerate([col for col in lsdyna["t_eid"].keys()][2:]):
        if len(row.node_ids) >= n + 1:
            lsdyna["t_eid"][st] += [row.node_ids[n]]
        else:
            lsdyna["t_eid"][st] += [row.node_ids[len(row.node_ids) - 1]]

tmp = pd.merge(abaqus["t_surface_name"], abaqus["t_surface_component"], on='surface_name', how='left')
tmp = pd.merge(tmp, abaqus["t_elset_component"], on='elset_name', how='left')
abaqus["q_segment_component"] = pd.merge(tmp, abaqus["t_element_id"], on='element_id', how='left')
del tmp

def create_set_node_from_surface(surface_id, set_type):
    lsdyna["t_sid"]["sid"]                 += [surface_id]
    lsdyna["t_sid"]["type"]                += [set_type]
    for sid, row in abaqus["q_segment_component"][abaqus["q_segment_component"]["surface_id"] == surface_id].iterrows():
        if row.element_type == "C3D4":
            if row.identification == "S1":
                plane = [row.node_ids[2], row.node_ids[1], row.node_ids[0]]
            elif row.identification == "S2":
                plane = [row.node_ids[1], row.node_ids[3] ,row.node_ids[0]]
            elif row.identification == "S3":
                plane = [row.node_ids[2], row.node_ids[3], row.node_ids[1]]
            elif row.identification == "S4":
                plane = [row.node_ids[0], row.node_ids[3], row.node_ids[2]]
        elif element_type == "S3R":
            plane = [row.node_ids[0], row.node_ids[1], row.node_ids[2]]
        else:
            plane = [row.node_ids[0], row.node_ids[1], row.node_ids[2]]

        for index, nid in plane
            lsdyna["t_sid_component"]["sid"]   += [surface_id]
            lsdyna["t_sid_component"]["nid"]   += [nid]

for tie, row in abaqus["t_tie_name"].iterrows():
    lsdyna["t_cid_surface"]["cid"]          += [tie + 1]    
    
    sid = int(abaqus["t_surface_name"][abaqus["t_surface_name"]["surface_name"] == row.slave_surface]["surface_id"])
    lsdyna["t_cid_surface"]["ssid"]         += [sid]
    lsdyna["t_cid_surface"]["sstyp"]        += [0]
    create_set_node_from_surface(sid, "segment")
    
    sid = int(abaqus["t_surface_name"][abaqus["t_surface_name"]["surface_name"] == row.master_surface]["surface_id"])
    lsdyna["t_cid_surface"]["msid"]         += [sid]
    lsdyna["t_cid_surface"]["mstyp"]        += [0]
    create_set_node_from_surface(sid, "segment")


for pid, row in abaqus["t_constraint_name"].iterrows():
    lsdyna["t_pid_rigid"]["pid"]          += [row.constraint_id]
    lsdyna["t_pid_rigid"]["cid"]          += [0]
    sid = int(abaqus["t_surface_name"][abaqus["t_surface_name"]["surface_name"] == row.surface_name]["surface_id"])
    lsdyna["t_pid_rigid"]["nsid"]         += [sid]
    lsdyna["t_pid_rigid"]["sstyp"]        += [0]
    lsdyna["t_pid_rigid"]["mstyp"]        += [0]
    create_set_node_from_surface(sid, "node")


abaqus["q_transform_component"] = pd.merge(abaqus["t_transform_name"], abaqus["t_nset_component"], on='nset_name', how='left')

#for id, row in abaqus["q_transform_component"].iterrows():
#    lsdyna[]


abaqus["q_segment_component"].to_csv(r"C:\Users\Ryoooful\OneDrive\Desktop\q_segment_component.csv")
#create_table(lsdyna["t_pid_rigid"]).to_csv(r"C:\Users\Ryoooful\OneDrive\Desktop\t_pid_rigid.csv")

