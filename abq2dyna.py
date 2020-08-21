import pandas as pd

path = r"C:\Temp\abq2dyna.inp"

#Mainコード
#ABAQUSファイルで開く
with open(path) as f:
    lines = [s.strip() for s in  f.readlines()]
    Read_Element =False
    Read_Set = False
    Read_Node = False
    Read_Surface = False
    #Node変数
    Node_ID = []
    Node_X  = []
    Node_Y  = []
    Node_Z  = []

    #Element変数
    Element_ID      = []
    Element_Types   = []
    Element_Counts  = []
    Element_Nodes   = []

    ##サーフェス変数
    Surface_Names = []
    Surface_Types = []
    Surface_Elsets = []

    ##節点集合(Nset)と要素集合(Elset)の変数
    Set_Types          = []
    Set_Names          = []
    Set_Internals      = []
    Set_Generates      = []
    Set_Instance_Names = []
    Set_Nodes          = []

    for line in lines:
    ##コメントは飛ばす
        if "**" in line:
            continue
        
        spdata = line.split(",")

    ##KEY値の処理を加える
        if "*" in line:
        ##節点データの読み込みを終了する。
            if Read_Node:
                Read_Node = False
            elif Read_Element:
                Read_Element = False
            elif Read_Set:
                Read_Set = False
                Set_Nodes += [Temp_Nodes]

    ##KEY値の取込みフラグを立てる
        ##節点の取込みを開始する。
            if '*Node' == line:
                Read_Node = True
                

        ##要素の取込みを開始する。
            elif '*Element' in line:
                Read_Element = True
                Temp_Type = spdata[1].split("=")[1] 

        ##サーフェスの取込みを開始する。
            elif '*Surface' in line:
                Read_Surface = True
                Temp_Type = ""
                Temp_Name = ""
                for sp in spdata:                    
                    if "type=" in sp:
                        Temp_Type = sp.split("=")[1]
                    elif "name=" in sp:
                        Temp_Name = sp.split("=")[1]

        ##節点集合(Nset)と要素集合(Elset)の取込みを開始する。
            elif '*Nset' in line or '*Elset' in line:
                Read_Set = True                
                internal = False
                generate = False
                Temp_Name = ""
                instance_name = ""

                for sp in spdata:                    
                    if "nset=" in sp or "elset=" in sp:
                        Temp_Name = sp.split("=")[1]
                    elif "instance=" in sp:
                        instance_name = sp.split("=")[1]
                    elif sp.strip() =="internal":
                        internal = True
                    elif sp.strip() =="generate":
                        generate = True
                
                Set_Types += [spdata[0].replace("*","")]
                Set_Names += [Temp_Name]
                Set_Internals += [internal]
                Set_Generates += [generate]
                Set_Instance_Names += [instance_name]
                Temp_Nodes = []

    ##各データの取り込みを行う。
        else:
            ##nodeの取込みを行う。
            if Read_Node:
                Node_ID += [int(spdata[0])]
                Node_X  += [float(spdata[1])]
                Node_Y  += [float(spdata[2])]
                Node_Z  += [float(spdata[3])]

            ##Elementの取込みを行う。
            if Read_Element:
                Temp_Nodes = []
                for st in spdata[1:]:
                    Temp_Nodes.append(int(st.strip()))
                Element_ID     += [int(spdata[0])]
                Element_Types  += [Temp_Type]
                Element_Counts += [int(len(spdata)) - 1]
                Element_Nodes  += [Temp_Nodes]

            #if Read_Surface:
                


            ##節点集合(Nset)と要素集合(Elset)の取込みを行う。
            if Read_Set:
                if generate:
                    for st in range(int(spdata[0]), int(spdata[1]), int(spdata[2])):
                        Temp_Nodes.append(st)
                else:
                    for st in spdata:       
                        if st.strip() != "":
                            Temp_Nodes.append(st.strip())

NodesFrame   = pd.DataFrame(index=Node_ID, data={'x':Node_X, 'y':Node_Y, 'z':Node_Z}, columns=['x', 'y', 'z'])
ElementFrame = pd.DataFrame(index=Element_ID, data={'type':Element_Types, 'count':Element_Counts, 'nodes':Element_Nodes}, columns=['type', 'count', 'nodes'])
SetFrame = pd.DataFrame(data={'name':Set_Names, 'type':Set_Types, 'instance_name':Set_Instance_Names, 'internal':Set_Internals, 'generate':Set_Generates, 'nodes':Set_Nodes}, columns=['name','type', 'instance_name', 'internal', 'generate', 'nodes'])
