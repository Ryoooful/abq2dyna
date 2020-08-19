import numpy as np
import pandas as pd

path = r'C:\Users\Ryoooful\OneDrive\Desktop\abq2dyna.inp'
Read_Node = False

with open(path) as f:
    lines = [s.strip() for s in  f.readlines()]
    for line in lines:
        if "**" in line:
            continue
        
        spdata = line.split(",")

        if "*" in line:
            Read_Node = False
            Read_Element =False
            Read_Nset = False
            Read_Elset = False

            if '*Node' == line:
                Read_Node = True
            elif '*Element' in line:
                Read_Element = True
                Element_Type = spdata[1].split("=")[1] 
                
            elif '*Nset' in line:
                Read_Nset = True
                internal = False
                generate = False
                Nset = ""
                Instance = ""
                if "internal" in line:
                    internal = True
                if "generate" in line:
                    generate = True
                for sp in spdata:                    
                    if "nset=" in sp:
                        Nset = sp.split("=")[1]
                        print(Nset)
                    elif "instance=" in sp:
                        Instance = sp.split("=")[1]

            elif '*Elset' in line:
                Read_Elset = True
                internal = False
                generate = False
                Elset = ""
                Instance = ""
                if "internal" in line:
                    internal = True
                if "generate" in line:
                    generate = True
                for sp in spdata:                    
                    if "nset=" in sp:
                        Elset = sp.split("=")[1]
                    elif "instance=" in sp:
                        Instance = sp.split("=")[1]
        else:
            

            if Read_Node:
                number = int(spdata[0])
                x = float(spdata[1])
                y = float(spdata[2])
                z = float(spdata[3])
                



