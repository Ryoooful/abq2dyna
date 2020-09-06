import pandas as pd
input_path = r"C:\temp\abq2dyna.inp"
keyword = ""

table = {
    "t_node_id":            {"node_id":[], "x":[], "y":[], "z":[]},
    "t_element_id":         {"element_id":[], "element_type":[], "node_ids":[]},
    "t_element_component":  {"element_id":[], "node_id":[]}
    "t_elset_name":         {'elset_name':[], 'instance_name':[], 'generate':[], 'internal':[]}
    "elset_component":      {'elset_name':[] , 'element_id':[]}
        }

def create_table(table):
    return pd.DataFrame(data=table, columns=table.keys())

def get_name(name_label, spdata):
    for sp in spdata[1:]:
        if name_label + "=" == sp:
            return str(sp.split("=")[1])
    return ""

def get_bool(label, spdata):
    for sp in spdata[1:]:
        if label == sp:
            return True
    return False


with open(input_path) as f:
    lines = [s.strip() for s in f.readlines()]

for line in lines:
    ##Comment Brakeout
    if "**" == line[:2]:
        continue
    
    spdata = [s.strip() for s in line.split(",")]
    
    ##Save Keyword
    if "*" == spdata[0][:1]:
        keyword = spdata[0]
        if keyword == "*Element":
            element_type = get_name("type", spdata)
        elif keyword == "*Elset":
            element_type = get_name("elset", spdata)
        continue

    ##Append Data
    if   keyword == "*Node":
        table["t_node_id"]["node_id"]               += [int(spdata[0])]
        table["t_node_id"]["x"]                     += [float(spdata[1]) * 1000]
        table["t_node_id"]["y"]                     += [float(spdata[2]) * 1000]
        table["t_node_id"]["z"]                     += [float(spdata[3]) * 1000]
    elif keyword == "*Element":
        table["t_element_id"]["element_id"]         += [int(spdata[0])]
        table["t_element_id"]["element_type"]       += [element_type]
        table["t_element_id"]["node_ids"]           += [[int(st) for st in spdata[1:]]]
        table["t_element_component"]["element_id"]  += [int(spdata[0]) for st in spdata[1:]]
        table["t_element_component"]["node_id"]     += [int(st) for st in spdata[1:]]
    elif keyword == "*Elset":

        
print (create_table(table["t_element_component"]))
