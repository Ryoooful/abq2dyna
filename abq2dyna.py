# -*- coding: utf-8 -*-. 
import pandas as pd
import sys
import os
import time
import numpy

start = time.time()

input_path = r"C:\Users\Ryoooful\Desktop\abq2dyna2.inp"
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
    "t_id_node":        {"id":[], "nid":[], "dof":[], "vad":[], "lcid":[], "vid":[], "death":[], "birth":[]},
    "t_id_set_node":    {"id":[], "sid":[], "dof":[], "vad":[], "lcid":[], "vid":[], "death":[], "birth":[]},
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

def set_default(table):
    temp = {}
    for column_name, item in table.iteritems():
        temp.setdefault(column_name, item.values)
    return temp



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
            abaqus["t_boundary_id"]["nset_name"]            += [""]
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

print("inpfile loaded\t" + str(time.time() - start))


abaqus["q_solid_component"] = pd.merge(abaqus["t_solid_id"], abaqus["t_elset_component"], on='elset_name', how='left')
abaqus["q_part_component"] = pd.merge(abaqus["q_solid_component"], abaqus["t_element_id"], on='element_id', how='left')
df = abaqus["q_part_component"][['solid_id','elset_name','material_name','element_type']].groupby(['solid_id', "element_type"], as_index=False).max()
tmp = set_default(df)

for idx in range(df.shape[0]):
    mat = abaqus["t_material_name"][abaqus["t_material_name"]['material_name'] == tmp["material_name"][idx]].iloc[0]
    secid = len(lsdyna["t_secid"]["secid"]) + 1
    pid   = len(lsdyna["t_pid"]["pid"]) + 1
    mid   = len(lsdyna["t_mid"]["mid"]) + 1
    cid   = len(lsdyna["t_cid"]["cid"]) + 1

    #セクションを設定する
    lsdyna["t_secid"]["secid"]    += [secid]
    lsdyna["t_secid"]["title"]    += [tmp["elset_name"][idx]]
    if tmp["element_type"][idx] == "C3D4":
        if len(mat["hyperelastic"]) == 0:
            #1点積分四面体要素
            lsdyna["t_secid"]["elform"]   += [10]
        else:
            #1点積分節点圧力四面体要素
            lsdyna["t_secid"]["elform"]   += [13]
    else:
        lsdyna["t_secid"]["elform"]   += [0]
    
    #パートを設定する
    lsdyna["t_pid"]["pid"]              += [pid]
    lsdyna["t_pid"]["title"]            += [tmp["elset_name"][idx]]
    lsdyna["t_pid"]["type"]             += ["part"]
    lsdyna["t_pid_part"]["pid"]         += [pid]
    lsdyna["t_pid_part"]["secid"]       += [secid]
    lsdyna["t_pid_part"]["mid"]         += [mid]

    #自己接触を設定する
    lsdyna["t_cid"]["cid"]              += [cid]
    lsdyna["t_cid"]["title"]            += [tmp["elset_name"][idx]]
    lsdyna["t_cid"]["type"]             += ["exterior"]
    lsdyna["t_cid_exterior"]["cid"]     += [cid]
    lsdyna["t_cid_exterior"]["ssid"]    += [secid]
    lsdyna["t_cid_exterior"]["sstyp"]   += [3]

    #材料データを設定する
    lsdyna["t_mid"]["mid"]              += [mid]
    lsdyna["t_mid"]["title"]            += [mat["material_name"]]
    if len(mat["hyperelastic"]) > 1:
        lsdyna["t_mid"]["type"]         += ["ogden"]
        lsdyna["t_mid_ogden"]["mid"]    += [mid]
        lsdyna["t_mid_ogden"]["ro"]     += [float(mat["density"])]
        lsdyna["t_mid_ogden"]["pr"]     += [0.499]
        lsdyna["t_mid_ogden"]["mu1"]    += [2 * mat["hyperelastic"][0] / mat["hyperelastic"][1]] #mu(dyna) = 2 * mu(abqus) / alpha(abaqus)
        lsdyna["t_mid_ogden"]["alpha1"] += [mat["hyperelastic"][1]]
        lsdyna["t_mid_ogden"]["mu2"]    += [2 * mat["hyperelastic"][2] / mat["hyperelastic"][3]]
        lsdyna["t_mid_ogden"]["alpha2"] += [mat["hyperelastic"][3]]
        lsdyna["t_mid_ogden"]["mu3"]    += [2 * mat["hyperelastic"][4] / mat["hyperelastic"][5]]
        lsdyna["t_mid_ogden"]["alpha3"] += [mat["hyperelastic"][5]]
        # for index, st in enumerate([col for col in lsdyna["t_mid_ogden"].keys()][3:]):
        #     lsdyna["t_mid_ogden"][st] += [float(mat["hyperelastic"][index - 3])]
    else:
        lsdyna["t_mid"]["type"]           += ["elastic"]
        lsdyna["t_mid_elastic"]["mid"]    += [mid]
        lsdyna["t_mid_elastic"]["ro"]     += [float(mat["density"] /1000000000000)]
        lsdyna["t_mid_elastic"]["e"]      += [float(mat["young"] /1000000)]
        lsdyna["t_mid_elastic"]["pr"]     += [float(mat["poason"])]


tmp = set_default(abaqus["q_part_component"])

#要素を設定する
for idx in range(abaqus["q_part_component"].shape[0]):
    lsdyna["t_eid"]["eid"]     += [tmp["element_id"][idx]]
    lsdyna["t_eid"]["pid"]     += [tmp["solid_id"][idx]]
    for n, st in enumerate([col for col in lsdyna["t_eid"].keys()][2:]):
        if len(tmp["node_ids"][idx]) >= n + 1:
            lsdyna["t_eid"][st] += [tmp["node_ids"][idx][n]]
        else:
            lsdyna["t_eid"][st] += [tmp["node_ids"][idx][len(tmp["node_ids"][idx]) - 1]]

df = pd.merge(abaqus["t_surface_name"], abaqus["t_surface_component"], on='surface_name', how='left')
df = pd.merge(df, abaqus["t_elset_component"], on='elset_name', how='left')
abaqus["q_segment_component"] = pd.merge(df, abaqus["t_element_id"], on='element_id', how='left')


#要素の面番号から節点集合に変更する
def create_set_node_from_surface(sid, set_type, heading):
    df = abaqus["q_segment_component"][abaqus["q_segment_component"]["surface_name"] == heading]
    tmp = set_default(df)
    for idx in range(df.shape[0]):
        #要素タイプから指定面の節点IDを抽出する。
        #4面体要素
        if tmp["element_type"][idx] == "C3D4":
            if tmp["identification"][idx] == "S1":
                plane = [tmp["node_ids"][idx][2], tmp["node_ids"][idx][1], tmp["node_ids"][idx][0]]
            elif tmp["identification"][idx] == "S2":
                plane = [tmp["node_ids"][idx][1], tmp["node_ids"][idx][3] ,tmp["node_ids"][idx][0]]
            elif tmp["identification"][idx] == "S3":
                plane = [tmp["node_ids"][idx][2], tmp["node_ids"][idx][3], tmp["node_ids"][idx][1]]
            elif tmp["identification"][idx] == "S4":
                plane = [tmp["node_ids"][idx][0], tmp["node_ids"][idx][3], tmp["node_ids"][idx][2]]
        #5面体(3角柱)要素
        elif tmp.element_type.values[idx] == "C3D6":
            if tmp["identification"][idx] == "S1":
                plane = [tmp["node_ids"][idx][0], tmp["node_ids"][idx][1], tmp["node_ids"][idx][2]]
            elif tmp["identification"][idx] == "S2":
                plane = [tmp["node_ids"][idx][3], tmp["node_ids"][idx][5], tmp["node_ids"][idx][4]]
            elif tmp["identification"][idx] == "S3":
                plane = [tmp["node_ids"][idx][0], tmp["node_ids"][idx][3], tmp["node_ids"][idx][4], tmp["node_ids"][idx][1]]
            elif tmp["identification"][idx] == "S4":
                plane = [tmp["node_ids"][idx][1], tmp["node_ids"][idx][4], tmp["node_ids"][idx][5], tmp["node_ids"][idx][2]]
            elif tmp["identification"][idx] == "S5":
                plane = [tmp["node_ids"][idx][2], tmp["node_ids"][idx][5], tmp["node_ids"][idx][3], tmp["node_ids"][idx][0]]
        #6面体要素
        elif tmp.element_type.values[idx] == "C3D8R":
            if tmp["identification"][idx] == "S1":
                plane = [tmp["node_ids"][idx][0], tmp["node_ids"][idx][1], tmp["node_ids"][idx][2], tmp["node_ids"][idx][3]]
            elif tmp["identification"][idx] == "S2":
                plane = [tmp["node_ids"][idx][4], tmp["node_ids"][idx][7], tmp["node_ids"][idx][6], tmp["node_ids"][idx][5]]
            elif tmp["identification"][idx] == "S3":
                plane = [tmp["node_ids"][idx][0], tmp["node_ids"][idx][4], tmp["node_ids"][idx][5], tmp["node_ids"][idx][1]]
            elif tmp["identification"][idx] == "S4":
                plane = [tmp["node_ids"][idx][1], tmp["node_ids"][idx][5], tmp["node_ids"][idx][6], tmp["node_ids"][idx][2]]
            elif tmp["identification"][idx] == "S5":
                plane = [tmp["node_ids"][idx][2], tmp["node_ids"][idx][6], tmp["node_ids"][idx][7], tmp["node_ids"][idx][3]]
            elif tmp["identification"][idx] == "S6":
                plane = [tmp["node_ids"][idx][3], tmp["node_ids"][idx][7], tmp["node_ids"][idx][4], tmp["node_ids"][idx][0]]
        #3角面
        elif tmp.element_type.values[idx] == "S3R":
            plane = [tmp["node_ids"][idx][0], tmp["node_ids"][idx][1], tmp["node_ids"][idx][2]]
        #4角面
        elif tmp.element_type.values[idx] == "S4R":
            plane = [tmp["node_ids"][idx][0], tmp["node_ids"][idx][1], tmp["node_ids"][idx][2], tmp["node_ids"][idx][3]]
        else:
            plane = [tmp["node_ids"][idx][0], tmp["node_ids"][idx][1], tmp["node_ids"][idx][2]]

        for nid in plane:
            lsdyna["t_sid_component"]["sid"]           += [sid]
            lsdyna["t_sid_component"]["element_id"]    += [tmp["element_id"][idx]]
            lsdyna["t_sid_component"]["nid"]           += [nid]
        if set_type == "segment" and len(plane) < 4:
            for n in range(len(plane), 4):
                lsdyna["t_sid_component"]["sid"]           += [sid]
                lsdyna["t_sid_component"]["element_id"]    += [tmp["element_id"][idx]]
                lsdyna["t_sid_component"]["nid"]           += [plane[len(plane) - 1]]

#接触面の設定を行う
tmp = set_default(abaqus["t_tie_name"])
for idx in range(abaqus["t_tie_name"].shape[0]):
    sid_slave  = len(lsdyna["t_sid"]["sid"]) + 1
    lsdyna["t_sid"]["sid"]                  += [sid_slave]
    lsdyna["t_sid"]["type"]                 += ["segment"]
    lsdyna["t_sid"]["title"]                += [tmp["slave_surface"][idx]]
    sid_master = len(lsdyna["t_sid"]["sid"]) + 1
    lsdyna["t_sid"]["sid"]                  += [sid_master]
    lsdyna["t_sid"]["type"]                 += ["segment"]
    lsdyna["t_sid"]["title"]                += [tmp["master_surface"][idx]]

    cid = len(lsdyna["t_cid"]["cid"]) + 1
    lsdyna["t_cid"]["cid"]                  += [cid]
    lsdyna["t_cid"]["title"]                += [tmp["tie_name"][idx]]
    lsdyna["t_cid"]["type"]                 += ["surface"]

    lsdyna["t_cid_surface"]["cid"]          += [cid]
    lsdyna["t_cid_surface"]["ssid"]         += [sid_slave]
    lsdyna["t_cid_surface"]["sstyp"]        += [0]
    create_set_node_from_surface(sid_slave, "segment", tmp["slave_surface"][idx])
    lsdyna["t_cid_surface"]["msid"]         += [sid_master]
    lsdyna["t_cid_surface"]["mstyp"]        += [0]
    create_set_node_from_surface(sid_master, "segment", tmp["master_surface"][idx])

abaqus["t_nset_component"] = pd.merge(abaqus["t_nset_component"], abaqus["t_node_id"], on='node_id', how='left')

#剛体を作成する
df = pd.merge(abaqus["t_constraint_name"], abaqus["t_nset_component"], on='nset_name', how='left')
tmp = set_default(df)
for idx in range(df.shape[0]):
    sid = len(lsdyna["t_sid"]["sid"]) + 1
    lsdyna["t_sid"]["sid"]                     += [sid]
    lsdyna["t_sid"]["type"]                    += ["node"]
    lsdyna["t_sid"]["title"]                   += [tmp["surface_name"][idx]]
    lsdyna["t_sid_component"]["sid"]           += [sid]
    lsdyna["t_sid_component"]["element_id"]    += [None]
    lsdyna["t_sid_component"]["nid"]           += [tmp["node_id"][idx]]
    create_set_node_from_surface(sid, "node", tmp["surface_name"][idx])    
    pid = len(lsdyna["t_pid"]["pid"]) + 1
    lsdyna["t_pid"]["pid"]                     += [pid]
    lsdyna["t_pid"]["title"]                   += [tmp["constraint_name"][idx]]
    lsdyna["t_pid"]["type"]                    += ["rigid"]
    lsdyna["t_pid_rigid"]["pid"]               += [pid]
    lsdyna["t_pid_rigid"]["cid"]               += [0]
    lsdyna["t_pid_rigid"]["nsid"]              += [sid]
    lsdyna["t_pid_rigid"]["pnode"]             += [tmp["node_id"][idx]]


abaqus["t_transform_component"] = pd.merge(abaqus["t_transform_name"], abaqus["t_transform_component"], on='transform_name', how='left')

df = pd.merge(abaqus["t_step_name"], abaqus["t_boundary_id"], on='step_name', how='left')
df = pd.merge(df, abaqus["t_boundary_component"], on='boundary_id', how='left')
df = pd.merge(df, abaqus["t_transform_component"], on='nset_name', how='left')
df = pd.merge(df, abaqus["t_amplitude_name"], on='amplitude_name', how='left')
df = df[["step_id", "nset_name", "amplitude_name", "amplitude_type", "freedom", "amount", "transform_type"]]
abaqus["q_history_component"] = df.sort_values(["nset_name", "freedom", "step_id"])


for index, boundary in abaqus["q_history_component"].groupby(["nset_name", "freedom"], as_index=False).max().reset_index(drop=True).iterrows():
    tmp = abaqus["q_history_component"].loc[(abaqus["q_history_component"]["freedom"] == boundary.freedom) & (abaqus["q_history_component"]["nset_name"] == boundary.nset_name)]
    tmp = pd.merge(abaqus["t_step_name"], tmp, on='step_id', how='left')
    total_time = 0
    value = 0
    death = None

    lcid = len(lsdyna["t_lcid"]["lcid"]) + 1
    lsdyna["t_lcid"]["lcid"]      += [lcid]
    lsdyna["t_lcid"]["title"]     += [str(boundary.nset_name) + "," + str(boundary.freedom)]
    lsdyna["t_lcid_time"]["lcid"] += [lcid]
    lsdyna["t_lcid_time"]["a1"]   += [0]
    lsdyna["t_lcid_time"]["o1"]   += [0]
    for index, step in tmp.iterrows():
        step_time   =  step.time

        if 1 <= int(boundary.freedom) and int(boundary.freedom) <= 3:
            step_amount =  step.amount * 1000
        else:
            step_amount =  step.amount
        
        if not step.isnull().nset_name:
            if death == None:
                death = total_time

            if death != None:
                #OP=NEWはここで処理する
                if step.amplitude_name == "":
                    total_time  += (step_time - death)
                    value = step_amount
                    lsdyna["t_lcid_time"]["lcid"] += [lcid]
                    lsdyna["t_lcid_time"]["a1"]   += [total_time]
                    lsdyna["t_lcid_time"]["o1"]   += [value]
                else:
                    amplitude = abaqus["t_amplitude_component"][abaqus["t_amplitude_component"]["amplitude_name"] == step.amplitude_name]
                    for index, row in amplitude.iterrows():
                        if row.time != 0:
                            tmp_time  = total_time + (step_time   * row.time / (amplitude.max().time - amplitude.min().time)) 
                            value     = step_amount * row.step
                            lsdyna["t_lcid_time"]["lcid"] += [lcid]
                            lsdyna["t_lcid_time"]["a1"]   += [tmp_time]
                            lsdyna["t_lcid_time"]["o1"]   += [value]
                    total_time  += (step_time - death)
        else:
            if death != None:
                total_time += (step_time - death)
                lsdyna["t_lcid_time"]["lcid"] += [lcid]
                lsdyna["t_lcid_time"]["a1"]   += [total_time]
                lsdyna["t_lcid_time"]["o1"]   += [value]
            else:
                total_time += step_time
    
    lsdyna["t_lcid_time"]["lcid"] += [lcid]
    lsdyna["t_lcid_time"]["a1"]   += [total_time + 0.1]
    lsdyna["t_lcid_time"]["o1"]   += [value]

    nset = abaqus["t_nset_component"][abaqus["t_nset_component"]["nset_name"] == boundary.nset_name]            
    if boundary.transform_type == "C":
        if not boundary.nset_name in lsdyna["t_id"]["title"]:
            for index, node in nset.iterrows():
                vid = len(lsdyna["t_vid"]["vid"]) + 1
                lsdyna["t_vid"]["vid"]            += [vid]
                lsdyna["t_vid"]["xt"]             += [node.x]
                lsdyna["t_vid"]["yt"]             += [node.y]
                lsdyna["t_vid"]["zt"]             += [node.z]
                lsdyna["t_vid"]["xh"]             += [node.x * 1.1]  ##円筒座標系のZ方向次第でXYZの掛け率変更
                lsdyna["t_vid"]["yh"]             += [node.y * 1.1]  ##POINT
                lsdyna["t_vid"]["zh"]             += [node.z]        ##POINT

                id = len(lsdyna["t_id"]["id"]) + 1
                lsdyna["t_id"]["id"]             += [id]
                lsdyna["t_id"]["title"]          += [boundary.nset_name]
                lsdyna["t_id"]["type"]           += ["node"]

                lsdyna["t_id_node"]["id"]        += [id]
                lsdyna["t_id_node"]["nid"]       += [node.node_id]
                lsdyna["t_id_node"]["dof"]   += [-4]
                # if ((abaqus["t_boundary_component"]["boundary_id"] == boundary.boundary_id) & (abaqus["t_boundary_component"]["freedom"] == 3)).any():
                #     lsdyna["t_id_node"]["dof"]   += [-4]
                # else:
                #     lsdyna["t_id_node"]["dof"]   += [4]
                lsdyna["t_id_node"]["vad"]       += [2]
                lsdyna["t_id_node"]["lcid"]      += [lcid]    
                lsdyna["t_id_node"]["vid"]       += [vid]
                lsdyna["t_id_node"]["death"]     += [death] 
                lsdyna["t_id_node"]["birth"]     += [0] 
    else:
        if 1 <= int(boundary.freedom) and int(boundary.freedom) <= 3:
            dof = int(boundary.freedom)
        elif 4 <= int(boundary.freedom) and int(boundary.freedom) <= 6:
            dof = int(boundary.freedom) + 1
        else:
            dof = 1

        if len(nset) == 1:
            #RIGIDの場合
            id = len(lsdyna["t_id"]["id"]) + 1
            lsdyna["t_id"]["id"]                       += [id]
            lsdyna["t_id"]["title"]                    += [boundary.nset_name]
            lsdyna["t_id"]["type"]                     += ["node"]

            lsdyna["t_id_node"]["id"]                  += [id]
            lsdyna["t_id_node"]["nid"]                 += [int(nset.iloc[0]["node_id"])]
            lsdyna["t_id_node"]["dof"]                 += [dof]
            lsdyna["t_id_node"]["vad"]                 += [2]
            lsdyna["t_id_node"]["vid"]                 += [0]
            lsdyna["t_id_node"]["lcid"]                += [lcid] 
            lsdyna["t_id_node"]["death"]               += [death] 
            lsdyna["t_id_node"]["birth"]               += [0] 
        else:
            id = len(lsdyna["t_id"]["id"]) + 1
            lsdyna["t_id"]["id"]                           += [id]
            lsdyna["t_id"]["title"]                        += [boundary.nset_name]
            lsdyna["t_id"]["type"]                         += ["set_node"]
            
            #SET_NODEを作成する
            if not boundary.nset_name in lsdyna["t_sid"]["title"]:
                sid = len(lsdyna["t_sid"]["sid"]) + 1
                lsdyna["t_sid"]["sid"]                     += [sid]
                lsdyna["t_sid"]["title"]                   += [boundary.nset_name]
                lsdyna["t_sid"]["type"]                    += ["node"]
                for index, node in nset.iterrows():
                    lsdyna["t_sid_component"]["sid"]           += [sid]
                    lsdyna["t_sid_component"]["element_id"]    += [None]
                    lsdyna["t_sid_component"]["nid"]           += [node.node_id]
            else:
                sid = lsdyna["t_sid"]["title"].index(boundary.nset_name) + 1
                
            lsdyna["t_id_set_node"]["id"]                  += [id]
            lsdyna["t_id_set_node"]["sid"]                 += [sid]
            lsdyna["t_id_set_node"]["dof"]                 += [dof]
            lsdyna["t_id_set_node"]["vad"]                 += [2]
            lsdyna["t_id_set_node"]["vid"]                 += [0]
            lsdyna["t_id_set_node"]["lcid"]                += [lcid]
            lsdyna["t_id_set_node"]["death"]               += [death] 
            lsdyna["t_id_set_node"]["birth"]               += [0] 

tmp = set_default(abaqus["t_node_id"])
for idx in range(abaqus["t_node_id"].shape[0]):
    lsdyna["t_nid"]["nid"]  += [tmp["node_id"][idx]]
    lsdyna["t_nid"]["x"]    += [tmp["x"][idx]]
    lsdyna["t_nid"]["y"]    += [tmp["y"][idx]]
    lsdyna["t_nid"]["z"]    += [tmp["z"][idx]]
    lsdyna["t_nid"]["tc"]   += [0]
    lsdyna["t_nid"]["rc"]   += [0]

for st in lsdyna.keys():    
    lsdyna[st] = create_table(lsdyna[st])

print("keyfile writing\t" + str(time.time() - start))

with open(output_path, mode='w') as f:
    f.write("*KEYWORD\n")

    f.write("*TITLE\n")
    f.write(input_path)
    f.write("\n")

    f.write("*CONTROL_ACCURACY\n")
    f.write('{0: > #10}'.format(1)) #osu
    f.write('{0: > #10}'.format(4)) #inn
    f.write('{0: > #10}'.format(0)) #pidosu
    f.write("\n")

    f.write("*CONTROL_CONTACT\n")
    f.write(" 0.0000000 0.0000000         0         0         0         0         0         0")   #slsfac    rwpnal    islchk    shlthk    penopt    thkchg     orien    enmass
    f.write("\n")
    f.write("         0         0         0         0 0.0000000         0         0         0")   #usrstr    usrfrc     nsbcs    interm     xpene     ssthk      ecdt   tiedprj
    f.write("\n")
    f.write(" 0.0000000 0.0000000 0.0000000 0.0000000 0.0000000 0.0000000 0.0000000          ")   #sfric     dfric       edc       vfc        th     th_sf    pen_sf     ptscl
    f.write("\n")
    f.write("         2         0         0         0         0         0 0.0000000")   #ignore    frceng   skiprwg    outseg   spotstp   spotdel   spothin
    f.write("\n")
    f.write("         1         0         1 0.0000000 1.0000000         0 0.0000000         0")   #ignore    frceng   skiprwg    outseg   spotstp   spotdel   spothin
    f.write("\n")
    f.write("         0         0         0         0         0           0.0000000          ")   #shledg    pstiff    ithcnt    tdcnof     ftall              shltrw    igactc
    f.write("\n")

    f.write("*CONTROL_ENERGY\n")
    f.write('{0: > #10}'.format(2)) #hgen
    f.write('{0: > #10}'.format(2)) #rwen
    f.write('{0: > #10}'.format(2)) #slnten
    f.write('{0: > #10}'.format(2)) #rylen
    f.write("\n")

    f.write("*CONTROL_HOURGLASS\n")
    f.write('{0: > #10}'.format(5))    #ihq
    f.write('{0: > #10}'.format(0.05)) #qh
    f.write("\n")

    f.write("*CONTROL_TIMESTEP\n")
    f.write('{0:0< #10f}'.format(0))        #dtinit
    f.write('{0:0< #10f}'.format(0.9))      #tssfac
    f.write('{0: > #10}'.format(0))         #isdo
    f.write('{0:0< #10f}'.format(0))        #tslimt
    f.write('{0: > #10}'.format(-0.000005)) #dt2ms
    f.write('{0: > #10}'.format(0))         #lctm
    f.write('{0: > #10}'.format(0))         #erode
    f.write('{0: > #10}'.format(0))         #ms1st
    f.write("\n")
    f.write('{0: > #10}'.format(0))         #dt2msf
    f.write('{0: > #10}'.format(0))         #dt2mslc
    f.write('{0: > #10}'.format(0))         #imscl
    f.write('{0: > #30}'.format(0))         #rmscl
    f.write("\n")

    f.write("*CONTROL_TERMINATION\n")
    f.write('{0: > #10}'.format(lsdyna["t_lcid_time"].max()["a1"])) #endtim
    f.write("\n")

    
    f.write("*SECTION_SOLID_TITLE\n")
    tmp = set_default(lsdyna["t_secid"])
    for idx in range(lsdyna["t_secid"].shape[0]):
        f.write(tmp["title"][idx])
        f.write("\n")
        f.write('{0: > #10}'.format(tmp["secid"][idx]))
        f.write('{0: > #10}'.format(tmp["elform"][idx]))
        f.write("\n")

    df = pd.merge(lsdyna["t_pid"], lsdyna["t_pid_part"], on='pid', how='left')
    tmp = set_default(df)
    for idx in range(df.shape[0]):
        if tmp["type"][idx] == "part":
            f.write("*PART\n")
            f.write(tmp["title"][idx] + "\n")
            f.write('{0: > #10}'.format(int(tmp["pid"][idx])))
            f.write('{0: > #10}'.format(int(tmp["secid"][idx])))
            f.write('{0: > #10}'.format(int(tmp["mid"][idx])))
            f.write("\n")

    df = pd.merge(lsdyna["t_pid"], lsdyna["t_pid_rigid"], on='pid', how='left')
    tmp = set_default(df)
    for idx in range(df.shape[0]):
        if tmp["type"][idx] == "rigid":
            f.write("*CONSTRAINED_NODAL_RIGID_BODY_TITLE\n")
            f.write(tmp["title"][idx] + "\n")
            f.write('{0: > #10}'.format(tmp["pid"][idx]))
            f.write('{: <10}'.format(""))                       #cid
            f.write('{0: > #10}'.format(int(tmp["nsid"][idx]))) #nsid
            f.write('{0: > #10}'.format(int(tmp["pnode"][idx])))#pnode
            f.write('{: <10}'.format(""))                       #iprt
            f.write('{: <10}'.format(""))                       #drflag
            f.write('{: <10}'.format(""))                       #rrflag
            f.write("\n")
    
    for index, row in pd.merge(lsdyna["t_mid"], lsdyna["t_mid_elastic"], on='mid', how='left').iterrows():
        if row.type == "elastic":
            f.write("*MAT_ELASTIC_TITLE\n")
            f.write(row.title + "\n")
            f.write('{0: > #10}'.format(row.mid))
            f.write('{: >10}'.format('{:.3e}'.format(row.ro)))       
            f.write('{0: > #10}'.format(row.e))       
            f.write('{0:0< #10f}'.format(row.pr))        
            f.write('{: <10}'.format(""))           #da
            f.write('{: <10}'.format(""))           #db
            f.write('{: <10}'.format(""))           #k
            f.write("\n")
    
    for index, row in pd.merge(lsdyna["t_mid"], lsdyna["t_mid_ogden"], on='mid', how='left').iterrows():
        if row.type == "ogden":
            f.write("*MAT_OGDEN_RUBBER_TITLE\n")
            f.write(row.title + "\n")
            f.write('{0: > #10}'.format(row.mid))
            f.write('{: >10}'.format('{:.3e}'.format(row.ro)))                  
            f.write('{0:0< #10f}'.format(row.pr))       
            f.write('{0: > #10}'.format(0))      #n
            f.write('{0: > #10}'.format(3))      #nv
            f.write('{0:0< #10f}'.format(1))     #g
            f.write('{0:0< #10f}'.format(0.001)) #nv
            f.write('{0:0< #10f}'.format(0))     #ref
            f.write("\n")
            f.write('{: >10}'.format('{:.3e}'.format(row.mu1))) 
            f.write('{: >10}'.format('{:.3e}'.format(row.mu2)))            
            f.write('{: >10}'.format('{:.3e}'.format(row.mu3))) 
            f.write('{0:0< #10f}'.format(0))     #mu4
            f.write('{0:0< #10f}'.format(0))     #mu5             
            f.write('{0:0< #10f}'.format(0))     #mu6   
            f.write('{0:0< #10f}'.format(0))     #mu7
            f.write('{0:0< #10f}'.format(0))     #mu8
            f.write("\n")
            f.write('{: >10}'.format('{:.3e}'.format(row.alpha1))) 
            f.write('{: >10}'.format('{:.3e}'.format(row.alpha2))) 
            f.write('{: >10}'.format('{:.3e}'.format(row.alpha3))) 
            f.write('{0:0< #10f}'.format(0))     #alpha4
            f.write('{0:0< #10f}'.format(0))     #alpha5             
            f.write('{0:0< #10f}'.format(0))     #alpha6   
            f.write('{0:0< #10f}'.format(0))     #alpha7 
            f.write('{0:0< #10f}'.format(0))     #alpha8 
            f.write("\n")

    for index, lcid in lsdyna["t_lcid"].iterrows():
        f.write("*DEFINE_CURVE_TITLE\n")
        f.write(lcid.title + "\n")
        f.write('{0: > #10}'.format(lcid.lcid))
        f.write("\n")
        for index, row in lsdyna["t_lcid_time"][lsdyna["t_lcid_time"]['lcid'] == lcid.lcid].iterrows():
            f.write('{0: > #20}'.format(row.a1))
            f.write('{0: > #20}'.format(row.o1))
            f.write("\n")

    for index, row in pd.merge(lsdyna["t_cid"], lsdyna["t_cid_exterior"], on='cid', how='left').iterrows():
        if row.type == "exterior":
            f.write("*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID\n")
            f.write('{0: > #10}'.format(row.cid))
            f.write('{: <70}'.format(row.title) + "\n")  
            f.write('{0: > #10}'.format(int(row.ssid)))
            f.write('{0: > #10}'.format(0))         #msid
            f.write('{0: > #10}'.format(int(row.sstyp))) #sstyp
            f.write('{0: > #10}'.format(0))         #mstyp
            f.write('{: <10}'.format(""))           #sboxid
            f.write('{: <10}'.format(""))           #mboxid
            f.write('{: <10}'.format(""))           #spr
            f.write('{: <10}'.format(""))           #mpr
            f.write("\n")
            f.write('{0:0< #10f}'.format(0.1))       #fs
            f.write('{0:0< #10f}'.format(0.1))       #fd
            f.write('{: <10}'.format(""))           #dc
            f.write('{: <10}'.format(""))           #vc
            f.write('{0:0< #10f}'.format(20))        #vdc
            f.write('{: <10}'.format(""))           #penchk
            f.write('{: <10}'.format(""))           #bt
            f.write('{: <10}'.format(""))           #dt
            f.write("\n")
            f.write('{0:0< #10f}'.format(2))        #sfs
            f.write('{0:0< #10f}'.format(2))        #sfm
            f.write('{: <10}'.format(""))           #sst
            f.write('{: <10}'.format(""))           #mst
            f.write('{: <10}'.format(""))           #sfst
            f.write('{: <10}'.format(""))           #sfmt
            f.write('{: <10}'.format(""))           #fsf
            f.write('{: <10}'.format(""))           #vsf
            f.write("\n")
            f.write('{0: > #10}'.format(2))         #soft
            f.write('{: <10}'.format(""))           #sofscl
            f.write('{: <10}'.format(""))           #lcidab
            f.write('{: <10}'.format(""))           #maxpar
            f.write('{0:0< #10f}'.format(3))        #sbopt
            f.write('{0: > #10}'.format(5))         #depth
            f.write("\n")
    
    for index, row in pd.merge(lsdyna["t_cid"], lsdyna["t_cid_surface"], on='cid', how='left').iterrows():
        if row.type == "surface":
            f.write("*CONTACT_TIED_SURFACE_TO_SURFACE_ID\n")
            f.write('{0: > #10}'.format(row.cid))
            f.write('{: <70}'.format(row.title) + "\n")  
            f.write('{0: > #10}'.format(int(row.ssid)))  #ssid
            f.write('{0: > #10}'.format(int(row.msid)))        #msid
            f.write('{0: > #10}'.format(int(row.sstyp))) #sstyp
            f.write('{0: > #10}'.format(int(row.mstyp)))         #mstyp
            f.write('{: <10}'.format(""))           #sboxid
            f.write('{: <10}'.format(""))           #mboxid
            f.write('{: <10}'.format(""))           #spr
            f.write('{: <10}'.format(""))           #mpr
            f.write("\n")
            f.write('{: <10}'.format(""))           #fs
            f.write('{: <10}'.format(""))           #fd
            f.write('{: <10}'.format(""))           #dc
            f.write('{: <10}'.format(""))           #vc
            f.write('{0:0< #10f}'.format(20))        #vdc
            f.write('{: <10}'.format(""))           #penchk
            f.write('{: <10}'.format(""))           #bt
            f.write('{: <10}'.format(""))           #dt
            f.write("\n")
            f.write('{: <10}'.format(""))           #soft
            f.write('{: <10}'.format(""))           #sofscl
            f.write('{: <10}'.format(""))           #lcidab
            f.write('{: <10}'.format(""))           #maxpar
            f.write('{: <10}'.format(""))           #sbopt
            f.write('{: <10}'.format(""))           #depth
            f.write("\n")

    
    for index, row in lsdyna["t_sid"].iterrows():
        if row.type == "segment":
            f.write("*SET_SEGMENT_TITLE\n")
            f.write('{: <80}'.format(row.title) + "\n")  
            f.write('{0: > #10}'.format(row.sid))   #sid
            f.write('{: <10}'.format(""))           #da1
            f.write('{: <10}'.format(""))           #da2
            f.write('{: <10}'.format(""))           #da3
            f.write('{: <10}'.format(""))           #da4
            f.write('{: <10}'.format(""))           #solver
            f.write("\n")
            element_id = 0
            for index, row in lsdyna["t_sid_component"][lsdyna["t_sid_component"]['sid'] == row.sid].iterrows():
                if element_id == 0:
                    element_id = row.element_id
                elif element_id != row.element_id:
                    element_id = row.element_id
                    f.write('{: <10}'.format(""))           #a1
                    f.write('{: <10}'.format(""))           #a2
                    f.write('{: <10}'.format(""))           #a3
                    f.write('{: <10}'.format(""))           #a4
                    f.write("\n")
                f.write('{0: > #10}'.format(int(row.nid)))       #nid
            f.write("\n")
        elif row.type == "node":
            f.write("*SET_NODE_TITLE\n")
            f.write('{: <80}'.format(row.title) + "\n")  
            f.write('{0: > #10}'.format(row.sid))   #sid
            f.write('{: <10}'.format(""))           #da1
            f.write('{: <10}'.format(""))           #da2
            f.write('{: <10}'.format(""))           #da3
            f.write('{: <10}'.format(""))           #da4
            f.write('{: <10}'.format(""))           #solver
            for index, row in lsdyna["t_sid_component"][lsdyna["t_sid_component"]['sid'] == row.sid].sort_values("nid").reset_index().iterrows():
                if index % 8 == 0: 
                    f.write("\n")
                f.write('{0: > #10}'.format(int(row.nid)))
            f.write("\n")

    
    df = pd.merge(lsdyna["t_id_set_node"], lsdyna["t_id"], on='id', how='left')
    tmp = set_default(df)
    for idx in range(df.shape[0]):
        f.write("*BOUNDARY_PRESCRIBED_MOTION_SET_ID\n")
        f.write('{0: > #10}'.format(tmp["id"][idx]))
        f.write(tmp["title"][idx] + "\n")
        f.write('{0: > #10}'.format(tmp["sid"][idx]))
        f.write('{0: > #10}'.format(tmp["dof"][idx]))
        f.write('{0: > #10}'.format(tmp["vad"][idx]))
        f.write('{0: > #10}'.format(tmp["lcid"][idx]))
        f.write('{: <10}'.format(""))
        f.write('{0: > #10}'.format(tmp["vid"][idx]))
        f.write("\n")

    df = pd.merge(lsdyna["t_id_node"], lsdyna["t_id"], on='id', how='left')
    tmp = set_default(df)
    for idx in range(df.shape[0]):
        f.write("*BOUNDARY_PRESCRIBED_MOTION_NODE_ID\n")
        f.write('{0: > #10}'.format(tmp["id"][idx]))
        f.write(tmp["title"][idx] + "\n")
        f.write('{0: > #10}'.format(tmp["nid"][idx]))
        f.write('{0: > #10}'.format(tmp["dof"][idx]))
        f.write('{0: > #10}'.format(tmp["vad"][idx]))
        f.write('{0: > #10}'.format(tmp["lcid"][idx]))
        f.write('{: <10}'.format(""))
        f.write('{0: > #10}'.format(tmp["vid"][idx]))
        f.write("\n")

    tmp = set_default(lsdyna["t_vid"])
    for idx in range(lsdyna["t_vid"].shape[0]):
        f.write("*DEFINE_VECTOR\n") 
        f.write('{0: > #10}'.format(int(tmp["vid"][idx])))
        f.write('{0:0< #10f}'.format(tmp["xt"][idx]))
        f.write('{0:0< #10f}'.format(tmp["yt"][idx]))
        f.write('{0:0< #10f}'.format(tmp["zt"][idx]))
        f.write('{0:0< #10f}'.format(tmp["xh"][idx]))
        f.write('{0:0< #10f}'.format(tmp["yh"][idx]))
        f.write('{0:0< #10f}'.format(tmp["zh"][idx]))
        f.write("\n")

    f.write("*ELEMENT_SOLID\n")
    tmp = set_default(lsdyna["t_eid"])
    for idx in range(lsdyna["t_eid"].shape[0]):
        f.write('{0: > #8}'.format(tmp["eid"][idx]))
        f.write('{0: > #8}'.format(tmp["pid"][idx]))
        f.write("\n")
        f.write('{0: > #8}'.format(tmp["n1"][idx]))
        f.write('{0: > #8}'.format(tmp["n2"][idx]))
        f.write('{0: > #8}'.format(tmp["n3"][idx]))
        f.write('{0: > #8}'.format(tmp["n4"][idx]))
        f.write('{0: > #8}'.format(tmp["n5"][idx]))
        f.write('{0: > #8}'.format(tmp["n6"][idx]))
        f.write('{0: > #8}'.format(tmp["n7"][idx]))
        f.write('{0: > #8}'.format(tmp["n8"][idx]))
        f.write("\n")

    f.write("*NODE\n")
    tmp = set_default(lsdyna["t_nid"])
    for idx in range(lsdyna["t_nid"].shape[0]):
        f.write('{0: > #8}'.format(int(tmp["nid"][idx])))
        f.write('{0:0< #16f}'.format(float(tmp["x"][idx])))
        f.write('{0:0< #16f}'.format(float(tmp["y"][idx])))
        f.write('{0:0< #16f}'.format(float(tmp["z"][idx])))
        f.write('{0: > #8}'.format(float(tmp["tc"][idx])))
        f.write('{0: > #8}'.format(float(tmp["rc"][idx])))
        f.write("\n")

    f.write("*END\n")

print("End\t" + str(time.time() - start))



