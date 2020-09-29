# -*- coding: utf-8 -*-. 
import pandas as pd
import sys

input_path = r"C:\temp\abq2dyna.inp"
output_path = r"C:\Users\1080045106\Desktop\dyna.key"
keyword = ""

#Abaqusファイルのテーブル構造
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
    "t_transform_name":     {"transform_name":[], "transform_id":[], "type":[], "x1":[], "y1":[], "z1":[], "x2":[], "y2":[], "z2":[]},
    "t_transform_component":{"transform_name":[], "nset_name":[]},
    "t_amplitude_name":     {"amplitude_name":[], "amplitude_id":[], "time":[]},
    "t_amplitude_component":{"amplitude_name":[], "time":[], "step":[]},
    "t_step_name":          {"step_name":[], "step_id":[]}, 
    "t_boundary_id":        {"boundary_id":[], "step_name":[], "nset_name":[], "amplitude_name":[], "u1":[], "u2":[], "u3":[], "ur1":[], "ur2":[], "ur3":[]},
    "t_boundary_component": {"boundary_id":[], "freedom":[], "amount":[]}
        }

lsdyna = {
    "t_nid":            {"nid":[], "x":[], "y":[], "z":[], "tc":[], "rc":[]},
    "t_eid":            {"eid":[], "pid":[], "n1":[], "n2":[], "n3":[], "n4":[], "n5":[], "n6":[], "n7":[], "n8":[]},
    "t_secid_solid":    {"secid":[], "title":[], "elform":[]},
    "t_part_id":        {"pid":[], "heading":[], "secid":[], "mid":[]},
    "t_mid_ogden":      {"mid":[], "title":[], "ro":[], "pr":[], "mu1":[], "alpha1":[], "mu2":[], "alpha2":[], "mu3":[], "alpha3":[]},
    "t_mid_elastics":   {"mid":[], "title":[], "ro":[], "e":[], "pr":[]},
    "t_cid_exterior":   {"cid":[], "heading":[], "ssid":[], "sstyp":[]},
    "t_sid":            {"sid":[], "title":[], "type":[]},
    "t_sid_component":  {"sid":[], "element_id":[], "nid":[]},
    "t_pid_rigid":      {"pid":[], "title":[], "cid":[], "nsid":[], "cmo":[], "con1":[], "con2":[]},
    "t_bid_node":       {"id":[], "heading":[], "nid":[], "dof":[], "vad":[], "lcid":[], "vid":[]},
    "t_bid_set_node":   {"id":[], "heading":[], "sid":[], "dof":[], "vad":[], "lcid":[], "vid":[]},
    "t_cid_surface":    {"cid":[], "heading":[], "ssid":[], "msid":[], "sstyp":[], "mstyp":[]},
    "t_vid":            {"vid":[], "xt":[], "yt":[], "zt":[], "xh":[], "yh":[], "zh":[]},
    "t_lcid":           {"lcid":[], "title":[]},
    "t_lcid_time":      {"lcid":[], "a1":[], "o1":[]}
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

#Abaqusファイルのテキストデータをリストに格納する
with open(input_path) as f:
    lines = [s.strip() for s in f.readlines()]


#Abaqusファイルのテキストデータを１行ずつ読み込む
for line in lines:
    #コメント分はスキップする。
    if "**" == line[:2]:
        continue
    
    #カンマ区切りでデータを分割する。
    spdata = [s.strip() for s in line.split(",")]
    
    #キーワードを習得し、フラグの作成と各テーブルへの追加を行う。
    if "*" == spdata[0][:1]:
        keyword = spdata[0]
        if "*Solid Section" == keyword:
            abaqus["t_solid_id"]["solid_id"]                += [len(abaqus["t_solid_id"]["solid_id"]) + 1]
            abaqus["t_solid_id"]["elset_name"]              += [get_name("elset", spdata)]
            abaqus["t_solid_id"]["material_name"]           += [get_name("material", spdata)]
        elif "*Coupling" == keyword:
            abaqus["t_constraint_name"]["constraint_id"]    += [len(abaqus["t_constraint_name"]["constraint_id"]) + 1]
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
            abaqus["t_transform_name"]["transform_name"]         += [get_name("nset", spdata)]
            abaqus["t_transform_name"]["transform_id"]      += [len(abaqus["t_transform_name"]["transform_id"])]
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
            abaqus["t_step_name"]["step_id"]                += [len(abaqus["t_step_name"]["step_id"]) + 1]
            abaqus["t_step_name"]["step_name"]              += [step_name]
        elif "*Boundary" == keyword:
            boundary_id = len(abaqus["t_boundary_id"]["boundary_id"]) + 1
            abaqus["t_boundary_id"]["boundary_id"]          += [boundary_id]
            abaqus["t_boundary_id"]["step_name"]            += [step_name]
            abaqus["t_boundary_id"]["nset_name"]            += [""]
            abaqus["t_boundary_id"]["amplitude_name"]       += [get_name("amplitude", spdata)]
            for col in [st for st in abaqus["t_boundary_id"].keys()][4:]:
                abaqus["t_boundary_id"][col] += [0]
        elif "*Amplitude" == keyword:
            amplitude_name = get_name("name", spdata)
            abaqus["t_amplitude_name"]["amplitude_id"]                += [len(abaqus["t_amplitude_name"]["amplitude_id"]) + 1]
            abaqus["t_amplitude_name"]["amplitude_name"]              += [amplitude_name]
            abaqus["t_amplitude_name"]["time"]                        += [get_name("time", spdata)]
        elif "*End Step" == keyword: 
            step_name = ""
        continue

    #キーワードの構成情報を各テーブルに追加する。
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
                elif st != "":
                    # tmp = create_table(abaqus["t_nset_component"])
                    # for index, row in tmp[tmp["nset_name"] == st].reset_index().iterrows():
                    #     abaqus["t_nset_component"]["nset_name"]  += [nset_name]
                    #     abaqus["t_nset_component"]["node_id"]    += [int(row.node_id)]
                    # del tmp
                    abaqus["t_transform_component"]["transform_name"] += [nset_name]
                    abaqus["t_transform_component"]["nset_name"]      += [st]
    elif keyword == "*Transform": 
        for index, st in enumerate([col for col in abaqus["t_transform_name"].keys()][3:]):
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
    elif keyword == "*Boundary": 
        abaqus["t_boundary_id"]["nset_name"][-1]         =  spdata[0]
        abaqus["t_boundary_component"]["boundary_id"]     += [boundary_id]
        abaqus["t_boundary_component"]["freedom"]       += [spdata[1]]
        #abaqus["t_boundary_id"][list(abaqus["t_boundary_id"].keys())[int(spdata[1]) + 3]][-1] = 1
        if len(spdata) == 4:
            abaqus["t_boundary_component"]["amount"]    += [float(spdata[3])]
            #abaqus["t_boundary_id"][list(abaqus["t_boundary_id"].keys())[int(spdata[1]) + 9]][-1] = float(spdata[3])
        else:
            abaqus["t_boundary_component"]["amount"]    += [None]
    elif keyword == "*Amplitude": 
        for n in range(0, len(spdata), 2):
            abaqus["t_amplitude_component"]["amplitude_name"] += [amplitude_name]
            abaqus["t_amplitude_component"]["time"]           += [float(spdata[n])]
            abaqus["t_amplitude_component"]["step"]           += [float(spdata[n + 1])]

#Abaqusデータをデータフレーム化する。
for st in abaqus.keys():
    abaqus[st] = create_table(abaqus[st])


# sys.exit()
#Convert .k 

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
    lsdyna["t_part_id"]["mid"]          += [mat["material_id"]]
    lsdyna["t_cid_exterior"]["cid"]     += [row.solid_id]
    lsdyna["t_cid_exterior"]["heading"] += [row.elset_name]
    lsdyna["t_cid_exterior"]["ssid"]    += [row.solid_id]
    lsdyna["t_cid_exterior"]["sstyp"]   += [3]
    if len(mat["hyperelastic"]) > 1:
        lsdyna["t_mid_ogden"]["mid"]    += [mat["material_id"]]
        lsdyna["t_mid_ogden"]["title"]  += [mat["material_name"]]
        lsdyna["t_mid_ogden"]["ro"]     += [float(mat["density"])]
        lsdyna["t_mid_ogden"]["pr"]     += [0.499]
        for index, st in enumerate([col for col in lsdyna["t_mid_ogden"].keys()][4:]):
            lsdyna["t_mid_ogden"][st] += [float(mat["hyperelastic"][index - 3])]
    else:
        lsdyna["t_mid_elastics"]["mid"]    += [mat["material_id"]]
        lsdyna["t_mid_elastics"]["title"]  += [mat["material_name"]]
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

def create_set_node_from_surface(sid, set_type, heading):
    for index, row in abaqus["q_segment_component"][abaqus["q_segment_component"]["surface_name"] == heading].iterrows():
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

        for nid in plane:
            lsdyna["t_sid_component"]["sid"]           += [sid]
            lsdyna["t_sid_component"]["element_id"]    += [row.element_id]
            lsdyna["t_sid_component"]["nid"]           += [nid]
        if set_type == "segment" and len(plane) < 4:
            for n in range(len(plane), 4):
                lsdyna["t_sid_component"]["sid"]           += [sid]
                lsdyna["t_sid_component"]["element_id"]    += [row.element_id]
                lsdyna["t_sid_component"]["nid"]           += [plane[len(plane) - 1]]
        
for tie, row in abaqus["t_tie_name"].iterrows():
    lsdyna["t_cid_surface"]["cid"]          += [len(lsdyna["t_cid_surface"]["cid"]) + 1]    
    lsdyna["t_cid_surface"]["heading"]      += [row.tie_name]
    sid = len(lsdyna["t_sid"]["sid"]) + 1
    lsdyna["t_cid_surface"]["ssid"]         += [sid]
    lsdyna["t_cid_surface"]["sstyp"]        += [0]
    lsdyna["t_sid"]["sid"]       += [sid]
    lsdyna["t_sid"]["type"]      += ["segment"]
    lsdyna["t_sid"]["title"]   += [row.slave_surface]
    create_set_node_from_surface(sid, "segment", row.slave_surface)
    
    sid = len(lsdyna["t_sid"]["sid"]) + 1
    lsdyna["t_cid_surface"]["msid"]         += [sid]
    lsdyna["t_cid_surface"]["mstyp"]        += [0]
    lsdyna["t_sid"]["sid"]       += [sid]
    lsdyna["t_sid"]["type"]      += ["segment"]
    lsdyna["t_sid"]["title"]   += [row.master_surface]
    create_set_node_from_surface(sid, "segment", row.master_surface)

#変位量がある拘束は削除する。
tmp = pd.merge(abaqus["t_boundary_id"], abaqus["t_boundary_component"], on='boundary_id', how='left')
tmp = tmp[tmp["amount"].isnull()].drop(['boundary_id', 'step_name', 'amplitude_name', 'amount'], axis=1)
tmp = tmp[~tmp.duplicated()]

#拘束がある場合はチェックつける。
for index, row in abaqus["t_boundary_id"].iterrows():
    for index2, row2 in tmp[tmp["nset_name"] == row.nset_name].iterrows():
        abaqus["t_boundary_id"].iat[index, int(row2.freedom) + 3] = 1
del tmp

#sys.exit()

#初期条件時の拘束をt_node_idに付与する。
abaqus["t_transform_component"] = pd.merge(abaqus["t_transform_name"], abaqus["t_transform_component"], on='transform_name', how='left')
tmp = abaqus["t_transform_component"][abaqus["t_transform_component"]["type"] == ""]
tmp = pd.merge(abaqus["t_transform_component"], abaqus["t_boundary_id"], on='nset_name', how='left')
tmp = pd.merge(tmp, abaqus["t_nset_component"], on='nset_name', how='left')
tmp = pd.merge(abaqus["t_node_id"], tmp, on='node_id', how='left').loc[:,["node_id", "x", "y", "z", "u1", "u2", "u3", "ur1", "ur2", "ur3"]]
abaqus["t_node_id"] = tmp.groupby("node_id").min()
abaqus["t_nset_component"] = pd.merge(abaqus["t_nset_component"], abaqus["t_node_id"], on='node_id', how='left')
del tmp

# tmp = abaqus["t_boundary_component"].drop(['freedom'], axis=1).groupby("boundary_id").max().isnull()
# print(tmp)
# tmp = pd.merge(abaqus["t_boundary_id"], tmp, on='boundary_id', how='left')


abaqus["t_boundary_id"] = pd.merge(abaqus["t_boundary_id"], abaqus["t_transform_component"], on='nset_name', how='left')
# del tmp

#print(abaqus["t_boundary_component"].dropna(subset=['amount']))


def get_node_on_translation(freedom1, freedom2, freedom3):
    if freedom1 == 1 and freedom2 == 0 and freedom3 == 0:
        return 1
    elif freedom1 == 0 and freedom2 == 1 and freedom3 == 0:
        return 2
    elif freedom1 == 0 and freedom2 == 0 and freedom3 == 1:
        return 3
    elif freedom1 == 1 and freedom2 == 1 and freedom3 == 0:
        return 4
    elif freedom1 == 0 and freedom2 == 1 and freedom3 == 1:
        return 5
    elif freedom1 == 1 and freedom2 == 0 and freedom3 == 1:
        return 6
    elif freedom1 == 1 and freedom2 == 1 and freedom3 == 1:
        return 7
    else:
        return 0




#剛体を作成する
for index, row in pd.merge(abaqus["t_constraint_name"], abaqus["t_nset_component"], on='nset_name', how='left').iterrows():
    sid = len(lsdyna["t_sid"]["sid"]) + 1
    lsdyna["t_sid"]["sid"]                     += [sid]
    lsdyna["t_sid"]["type"]                    += ["node"]
    lsdyna["t_sid"]["title"]                 += [row.constraint_name]
    lsdyna["t_sid_component"]["sid"]           += [sid]
    lsdyna["t_sid_component"]["element_id"]    += [None]
    lsdyna["t_sid_component"]["nid"]           += [row.node_id]
    create_set_node_from_surface(sid, "node", row.surface_name)
    lsdyna["t_pid_rigid"]["pid"]               += [row.constraint_id]
    lsdyna["t_pid_rigid"]["title"]             += [row.constraint_name]
    lsdyna["t_pid_rigid"]["cid"]               += [0]     
    lsdyna["t_pid_rigid"]["nsid"]              += [sid]               
    lsdyna["t_pid_rigid"]["cmo"]               += [0]
    # lsdyna["t_pid_rigid"]["con1"]              += [0]
    # lsdyna["t_pid_rigid"]["con2"]              += [0]
    lsdyna["t_pid_rigid"]["con1"]              += [get_node_on_translation(row.u1, row.u2, row.u3)]
    lsdyna["t_pid_rigid"]["con2"]              += [get_node_on_translation(row.ur1, row.ur2, row.ur3)]



lsdyna["t_lcid"]["lcid"]      += [1]
lsdyna["t_lcid"]["title"]     += ["default"]
lsdyna["t_lcid_time"]["lcid"] += [1]
lsdyna["t_lcid_time"]["a1"]   += [0]
lsdyna["t_lcid_time"]["o1"]   += [0]
lsdyna["t_lcid_time"]["lcid"] += [1]
lsdyna["t_lcid_time"]["a1"]   += [abaqus["t_amplitude_component"].max()["time"]]
lsdyna["t_lcid_time"]["o1"]   += [0]

for index, boundary in abaqus["t_boundary_id"].iterrows():
    if boundary.amplitude_name == "":
        lcid = 1
    else:
        lcid = len(lsdyna["t_lcid"]["lcid"]) + 1
        lsdyna["t_lcid"]["lcid"]          += [lcid]
        lsdyna["t_lcid"]["title"]         += [boundary.amplitude_name]
        for index, amplitude in abaqus["t_amplitude_component"][abaqus["t_amplitude_component"]["amplitude_name"] == boundary.amplitude_name].iterrows():
            lsdyna["t_lcid_time"]["lcid"] += [lcid]
            lsdyna["t_lcid_time"]["a1"]   += [amplitude.time]
            lsdyna["t_lcid_time"]["o1"]   += [amplitude.step]
    
    if boundary.type == "C":
        for index, node in abaqus["t_nset_component"][abaqus["t_nset_component"]["nset_name"] == boundary.nset_name].iterrows():
            vid = len(lsdyna["t_vid"]["vid"]) + 1
            lsdyna["t_bid_node"]["id"]        += [len(lsdyna["t_bid_node"]["id"]) + 1]
            lsdyna["t_bid_node"]["heading"]   += [boundary.nset_name]
            lsdyna["t_bid_node"]["nid"]       += [node.node_id]
            if node.ur3 == 1:
                lsdyna["t_bid_node"]["dof"]   += [4]
            else:
                lsdyna["t_bid_node"]["dof"]   += [-4]
            lsdyna["t_bid_node"]["vad"]       += [2]
            lsdyna["t_bid_node"]["lcid"]      += [lcid]    
            lsdyna["t_bid_node"]["vid"]       += [vid]
            lsdyna["t_vid"]["vid"]            += [vid]
            lsdyna["t_vid"]["xt"]             += [node.x]
            lsdyna["t_vid"]["yt"]             += [node.y]
            lsdyna["t_vid"]["zt"]             += [node.z]
            lsdyna["t_vid"]["xh"]             += [node.x * 1.1]  ##円筒座標系のZ方向次第でXYZの掛け率変更
            lsdyna["t_vid"]["yh"]             += [node.y * 1.1]  ##POINT
            lsdyna["t_vid"]["zh"]             += [node.z]        ##POINT
    else:
        sid = len(lsdyna["t_sid"]["sid"]) + 1
        lsdyna["t_sid"]["sid"]       += [sid]
        lsdyna["t_sid"]["type"]      += ["node"]
        lsdyna["t_sid"]["title"]     += [boundary.nset_name]
        for index, node in abaqus["t_nset_component"][abaqus["t_nset_component"]["nset_name"] == boundary.nset_name].iterrows():
            lsdyna["t_sid_component"]["sid"]           += [sid]
            lsdyna["t_sid_component"]["element_id"]    += [None]
            lsdyna["t_sid_component"]["nid"]           += [node.node_id]
        lsdyna["t_bid_set_node"]["id"]                 += [len(lsdyna["t_bid_set_node"]["id"]) + 1]
        lsdyna["t_bid_set_node"]["heading"]            += [boundary.nset_name]
        lsdyna["t_bid_set_node"]["sid"]                += [sid]
        lsdyna["t_bid_set_node"]["dof"]                += [0] #POINT
        lsdyna["t_bid_set_node"]["vad"]                += [2]
        lsdyna["t_bid_set_node"]["vid"]                += [0]
        lsdyna["t_bid_set_node"]["lcid"]               += [lcid] 


for nid, row in abaqus["t_node_id"].iterrows():
    lsdyna["t_nid"]["nid"]  += [nid]
    lsdyna["t_nid"]["x"]    += [row.x]
    lsdyna["t_nid"]["y"]    += [row.y]
    lsdyna["t_nid"]["z"]    += [row.z]
    lsdyna["t_nid"]["tc"]   += [get_node_on_translation(row.u1, row.u2, row.u3)]
    lsdyna["t_nid"]["rc"]   += [get_node_on_translation(row.ur1, row.ur2, row.ur3)]


for st in lsdyna.keys():
    lsdyna[st] = create_table(lsdyna[st])


#write dyna file

with open(output_path, mode='w') as f:
    f.write("*SECTION_SOLID_TITLE\n")
    for pid, row in lsdyna["t_secid_solid"].iterrows():
        f.write(row.title)
        f.write("\n")
        f.write('{0: > #10}'.format(row.secid))
        f.write('{0: > #10}'.format(row.elform))
        f.write("\n")

    f.write("*PART\n")
    for pid, row in lsdyna["t_part_id"].iterrows():
        f.write(row.heading + "\n")
        f.write('{0: > #10}'.format(row.pid))
        f.write('{0: > #10}'.format(row.secid))
        f.write('{0: > #10}'.format(row.mid))
        f.write("\n")
    
    
    for pid, row in lsdyna["t_cid_exterior"].iterrows():
        f.write("*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID\n")
        f.write('{0: > #10}'.format(row.cid))
        f.write(row.heading)
        f.write("\n")
        f.write('{0: > #10}'.format(row.ssid))
        f.write("          ")
        f.write('{0: > #10}'.format(row.sstyp))
        f.write("          ")
        f.write("\n")
        f.write('{0: > #10}'.format(0.1))
        f.write('{0: > #10}'.format(0.1))
        f.write("          ")
        f.write("          ")
        f.write('{0: > #10}'.format(20))
        f.write("\n")
        f.write('{0: > #10}'.format(2))
        f.write('{0: > #10}'.format(2))
        f.write("\n")
        f.write('{0: > #10}'.format(2))
        f.write("          ")
        f.write("          ")
        f.write("          ")
        f.write('{0: > #10}'.format(3))
        f.write('{0: > #10}'.format(5))
        f.write("\n")
        
    for pid, row in lsdyna["t_mid_elastics"].iterrows():
        f.write("*MAT_ELASTIC_TITLE\n")
        f.write(row.title + "\n")
        f.write('{0: > #10}'.format(row.mid))
        f.write('{0: > #10}'.format(row.ro))       
        f.write('{0: > #10}'.format(row.e))         
        f.write('{0: > #10}'.format(row.pr))        
        f.write("\n")
    #"t_mid_ogden":      {"mid":[], "ro":[], "pr":[], "mu1":[], "alpha1":[], "mu2":[], "alpha2":[], "mu3":[], "alpha3":[]},

    for sid, row in lsdyna["t_sid"].iterrows():
        if row.type == "segment":
            f.write("*SET_SEGMENT_TITLE\n")
            f.write(row.title)
            f.write("\n")
            f.write('{0: > #10}'.format(row.sid))
            element_id = 0
            for index, row in lsdyna["t_sid_component"][lsdyna["t_sid_component"]['sid'] == row.sid].iterrows():
                if element_id != row.element_id:
                    element_id = row.element_id
                    f.write("\n")
                f.write('{0: > #10}'.format(row.nid))
            f.write("\n")
            
        elif row.type == "node":
            f.write("*SET_NODE_TITLE\n")
            f.write(row.title)
            f.write("\n")
            f.write('{0: > #10}'.format(row.sid))
            for index, row in lsdyna["t_sid_component"][lsdyna["t_sid_component"]['sid'] == row.sid].reset_index().iterrows():
                if index % 8 == 0: 
                    f.write("\n")
                f.write('{0: > #10}'.format(row.nid))
            f.write("\n")

    for index, lcid in lsdyna["t_lcid"].iterrows():
        f.write("*DEFINE_CURVE_TITLE\n")
        f.write(lcid.title)
        f.write("\n")
        f.write('{0: > #10}'.format(lcid.lcid))
        f.write("\n")
        for index, row in lsdyna["t_lcid_time"][lsdyna["t_lcid_time"]['lcid'] == lcid.lcid].iterrows():
            f.write('{0: > #20}'.format(row.a1))
            f.write('{0: > #20}'.format(row.o1))
            f.write("\n")
        

    for cid, row in lsdyna["t_cid_surface"].iterrows():
        f.write("*CONTACT_TIED_SURFACE_TO_SURFACE_ID\n")
        f.write('{0: > #10}'.format(row.cid))
        f.write(row.heading)
        f.write("\n")
        f.write('{0: > #10}'.format(row.ssid))
        f.write('{0: > #10}'.format(row.msid))
        f.write('{0: > #10}'.format(row.sstyp))
        f.write('{0: > #10}'.format(row.mstyp))
        f.write("\n")
        f.write('{0: > #50}'.format(20))
        f.write("\n")
        f.write("\n")
    
    for cid, row in lsdyna["t_pid_rigid"].iterrows():
        f.write("*CONSTRAINED_NODAL_RIGID_BODY_SPC_TITLE\n")
        f.write(row.title)
        f.write("\n")
        f.write('{0: > #10}'.format(row.pid))
        f.write("          ")
        f.write('{0: > #10}'.format(row.nsid))
        f.write("\n")
        f.write('{0: > #10}'.format(1))
        f.write('{0: > #10}'.format(5))
        f.write('{0: > #10}'.format(7))
        f.write("\n")
    
    for nid, row in lsdyna["t_bid_node"].iterrows():
        f.write("*BOUNDARY_PRESCRIBED_MOTION_NODE_ID\n")
        f.write('{0: > #10}'.format(row.id))
        f.write(row.heading)
        f.write("\n")
        f.write('{0: > #10}'.format(row.nid))
        f.write('{0: > #10}'.format(row.dof))
        f.write('{0: > #10}'.format(row.vad))
        f.write('{0: > #10}'.format(row.lcid))
        f.write("          ")
        f.write('{0: > #10}'.format(row.vid))
        f.write("\n")

    for nid, row in lsdyna["t_bid_set_node"].iterrows():
        f.write("*BOUNDARY_PRESCRIBED_MOTION_SET_ID\n")
        f.write('{0: > #10}'.format(row.id))
        f.write(row.heading)
        f.write("\n")
        f.write('{0: > #10}'.format(row.sid))
        f.write('{0: > #10}'.format(row.dof))
        f.write('{0: > #10}'.format(row.vad))
        f.write('{0: > #10}'.format(row.lcid))
        f.write("          ")
        f.write('{0: > #10}'.format(row.vid))
        f.write("\n")

    f.write("*ELEMENT_SOLID\n")
    for pid, row in lsdyna["t_eid"].iterrows():
        f.write('{0: > #8}'.format(row.eid))
        f.write('{0: > #8}'.format(row.pid))
        f.write("\n")
        f.write('{0: > #8}'.format(row.n1))
        f.write('{0: > #8}'.format(row.n2))
        f.write('{0: > #8}'.format(row.n3))
        f.write('{0: > #8}'.format(row.n4))
        f.write('{0: > #8}'.format(row.n5))
        f.write('{0: > #8}'.format(row.n6))
        f.write('{0: > #8}'.format(row.n7))
        f.write('{0: > #8}'.format(row.n8))
        f.write("\n")

    f.write("*NODE\n")
    for pid, row in lsdyna["t_nid"].iterrows():
        f.write('{0: > #8}'.format(int(row.nid)))
        f.write('{0:0< #16f}'.format(float(row.x)))
        f.write('{0:0< #16f}'.format(float(row.y)))
        f.write('{0:0< #16f}'.format(float(row.z)))
        f.write('{0: > #8}'.format(float(row.tc)))
        f.write('{0: > #8}'.format(float(row.rc)))
        f.write("\n")

    for nid, row in lsdyna["t_vid"].iterrows():
        f.write("*DEFINE_VECTOR\n") 
        f.write('{0: > #10}'.format(int(row.vid)))
        f.write('{0:0< #10f}'.format(row.xt))
        f.write('{0:0< #10f}'.format(row.yt))
        f.write('{0:0< #10f}'.format(row.zt))
        f.write('{0:0< #10f}'.format(row.xh))
        f.write('{0:0< #10f}'.format(row.yh))
        f.write('{0:0< #10f}'.format(row.zh))
        f.write("\n")

print("end")




