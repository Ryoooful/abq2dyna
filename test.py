# -*- coding: utf-8 -*-. 
import pandas as pd
import sys
import os
import time

start = time.time()

input_path = r"C:\Users\Ryoooful\OneDrive\Desktop\step3.inp"
output_path = str(os.environ["HOMEDRIVE"]) + str(os.environ["HOMEPATH"]) + "\\Desktop\\" + os.path.splitext(os.path.basename(input_path))[0] + ".key"

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
    "t_transform_name":     {"transform_name":[], "transform_id":[], "transform_type":[], "x1":[], "y1":[], "z1":[], "x2":[], "y2":[], "z2":[]},
    "t_transform_component":{"transform_name":[], "nset_name":[]},
    "t_amplitude_name":     {"amplitude_name":[], "amplitude_id":[], "amplitude_type":[]},
    "t_amplitude_component":{"amplitude_name":[], "time":[], "step":[]},
    "t_mass_scaling":       {"dt":[], "mass_type":[], "frequency":[]}, 
    "t_step_name":          {"step_name":[], "step_id":[], "time":[]}, 
    "t_boundary_id":        {"boundary_id":[], "step_name":[], "nset_name":[], "amplitude_name":[]},
    "t_boundary_component": {"boundary_id":[], "freedom":[], "amount":[]}
        }

lsdyna = {
    "t_nid":            {"nid":[], "x":[], "y":[], "z":[], "tc":[], "rc":[]},
    "t_eid":            {"eid":[], "pid":[], "n1":[], "n2":[], "n3":[], "n4":[], "n5":[], "n6":[], "n7":[], "n8":[]},
    "t_secid":          {"secid":[], "title":[], "elform":[]},
    "t_pid":            {"pid":[], "title":[], "type":[]},
    "t_pid_part":       {"pid":[], "secid":[], "mid":[]},
    "t_pid_rigid":      {"pid":[], "cid":[], "nsid":[], "pnode":[]},
    "t_mid":            {"mid":[], "title":[], "type":[]},
    "t_mid_ogden":      {"mid":[], "ro":[], "pr":[], "mu1":[], "alpha1":[], "mu2":[], "alpha2":[], "mu3":[], "alpha3":[]},
    "t_mid_elastic":    {"mid":[], "ro":[], "e":[], "pr":[]},
    "t_cid":            {"cid":[], "title":[], "type":[]},
    "t_cid_exterior":   {"cid":[], "ssid":[], "sstyp":[]},
    "t_cid_surface":    {"cid":[], "ssid":[], "msid":[], "sstyp":[], "mstyp":[]},
    "t_sid":            {"sid":[], "title":[], "type":[]},
    "t_sid_component":  {"sid":[], "element_id":[], "nid":[]},
    "t_id":             {"id":[], "title":[], "type":[]},
    "t_id_node":        {"id":[], "nid":[], "dof":[], "vad":[], "lcid":[], "vid":[]},
    "t_id_set_node":    {"id":[], "sid":[], "dof":[], "vad":[], "lcid":[], "vid":[]},
    "t_vid":            {"vid":[], "xt":[], "yt":[], "zt":[], "xh":[], "yh":[], "zh":[]},
    "t_lcid":           {"lcid":[], "title":[]},
    "t_lcid_time":      {"lcid":[], "a1":[], "o1":[]}
        }

def get_name(name_label, spdata):
    for sp in spdata[1:]:
        if name_label + "=" in sp:
            return str(sp.split("=")[1])
    return None

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
    #コメント文はスキップする。
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
            abaqus["t_transform_name"]["transform_name"]    += [get_name("nset", spdata)]
            abaqus["t_transform_name"]["transform_id"]      += [len(abaqus["t_transform_name"]["transform_id"])]
            abaqus["t_transform_name"]["transform_type"]    += [get_name("type", spdata)]
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
            abaqus["t_step_name"]["time"]                   += [0]
        elif "*Variable Mass Scaling" == keyword: 
            abaqus["t_mass_scaling"]["dt"]                  += [get_name("dt", spdata)]
            abaqus["t_mass_scaling"]["mass_type"]           += [get_name("type", spdata)]
            abaqus["t_mass_scaling"]["frequency"]           += [get_name("frequency", spdata)]
        elif "*Boundary" == keyword:
            boundary_id = len(abaqus["t_boundary_id"]["boundary_id"]) + 1
            abaqus["t_boundary_id"]["boundary_id"]          += [boundary_id]
            abaqus["t_boundary_id"]["step_name"]            += [step_name]
            abaqus["t_boundary_id"]["nset_name"]            += [None]
            abaqus["t_boundary_id"]["amplitude_name"]       += [get_name("amplitude", spdata)]
            for col in [st for st in abaqus["t_boundary_id"].keys()][4:]:
                abaqus["t_boundary_id"][col] += [0]
        elif "*Amplitude" == keyword:
            amplitude_name = get_name("name", spdata)
            abaqus["t_amplitude_name"]["amplitude_id"]                += [len(abaqus["t_amplitude_name"]["amplitude_id"]) + 1]
            abaqus["t_amplitude_name"]["amplitude_name"]              += [amplitude_name]
            abaqus["t_amplitude_name"]["amplitude_type"]              += [get_name("time", spdata)]
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
    elif keyword == "*Dynamic": 
        abaqus["t_step_name"]["time"][-1]                   =  float(spdata[1])
    elif keyword == "*Boundary": 
        abaqus["t_boundary_id"]["nset_name"][-1]            =  spdata[0]
        abaqus["t_boundary_component"]["boundary_id"]       += [boundary_id]
        abaqus["t_boundary_component"]["freedom"]           += [spdata[1]]
        if len(spdata) == 4:
            abaqus["t_boundary_component"]["amount"]        += [float(spdata[3])]
        else:
            abaqus["t_boundary_component"]["amount"]        += [0]
    elif keyword == "*Amplitude": 
        for n in range(0, len(spdata), 2):
            abaqus["t_amplitude_component"]["amplitude_name"] += [amplitude_name]
            abaqus["t_amplitude_component"]["time"]           += [float(spdata[n])]
            abaqus["t_amplitude_component"]["step"]           += [float(spdata[n + 1])]

#Abaqusデータをデータフレーム化する。
for st in abaqus.keys():
    abaqus[st] = create_table(abaqus[st])

abaqus["t_transform_component"] = pd.merge(abaqus["t_transform_name"], abaqus["t_transform_component"], on='transform_name', how='left')
abaqus["t_nset_component"] = pd.merge(abaqus["t_nset_component"], abaqus["t_node_id"], on='node_id', how='left')
abaqus["t_boundary_id"] = pd.merge(abaqus["t_boundary_id"], abaqus["t_transform_component"], on='nset_name', how='left')
abaqus["q_solid_component"] = pd.merge(abaqus["t_solid_id"], abaqus["t_elset_component"], on='elset_name', how='left')
abaqus["q_part_component"] = pd.merge(abaqus["q_solid_component"], abaqus["t_element_id"], on='element_id', how='left')



endtim = round(abaqus["t_step_name"][["step_id", "time"]].sum()["time"], 3)
lsdyna["t_lcid"]["lcid"]            += [1]
lsdyna["t_lcid"]["title"]           += ["default"]
lsdyna["t_lcid_time"]["lcid"]       += [1]
lsdyna["t_lcid_time"]["a1"]         += [0]
lsdyna["t_lcid_time"]["o1"]         += [0]
lsdyna["t_lcid_time"]["lcid"]       += [1]
lsdyna["t_lcid_time"]["a1"]         += [endtim]
lsdyna["t_lcid_time"]["o1"]         += [0]

tmp = pd.merge(abaqus["t_step_name"], abaqus["t_boundary_id"], on='step_name', how='left')
#tmp = pd.merge(tmp, abaqus["t_boundary_component"], on='boundary_id', how='left')
#tmp = pd.merge(tmp, abaqus["t_amplitude_name"], on='amplitude_name', how='left')



#tmp = tmp[["step_id", "time", "nset_name", "amplitude_name", "amplitude_type", "freedom", "amount", "transform_type"]]
#tmp = tmp.sort_values(["nset_name", "freedom", "step_id"])
print(tmp)
sys.exit()

step_time = 0
for index, step in abaqus["t_step_name"].iterrows():
    for index, boundary in abaqus["t_boundary_id"][abaqus["t_boundary_id"]["step_name"] == step.step_name].iterrows():
        for index, row in abaqus["t_boundary_component"][abaqus["t_boundary_component"]["boundary_id"] == boundary.boundary_id].iterrows():

for index, boundary in pd.merge(abaqus["t_step_name"], abaqus["t_boundary_id"], on='step_name', how='left').iterrows():
    if boundary.amplitude_name != None:
        lcid_name = str(boundary.amplitude_name) + "," + str(boundary.amount)
        if lcid_name in lsdyna["t_lcid"]["title"]:
            lcid = lsdyna["t_lcid"]["lcid"][lsdyna["t_lcid"]["title"].index(lcid_name)]
        else:
            lcid = len(lsdyna["t_lcid"]["lcid"]) + 1
            lsdyna["t_lcid"]["lcid"]          += [lcid]
            lsdyna["t_lcid"]["title"]         += [lcid_name]
            for index, amplitude in abaqus["t_amplitude_component"][abaqus["t_amplitude_component"]["amplitude_name"] == boundary.amplitude_name].iterrows():
                lsdyna["t_lcid_time"]["lcid"] += [lcid]
                lsdyna["t_lcid_time"]["a1"]   += [amplitude.time]
                if boundary.amount == 0:
                    lsdyna["t_lcid_time"]["o1"]   += [0]
                else:
                    lsdyna["t_lcid_time"]["o1"]   += [amplitude.step]














sys.exit()
