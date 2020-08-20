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
    nid = []
    nx  = []
    ny  = []
    nz  = []

    #Element変数
    el_id      = []
    el_types   = []
    el_counts  = []
    el_nodes   = []

    ##節点集合(Nset)と要素集合(Elset)の変数
    st_types          = []
    st_names          = []
    st_internals      = []
    st_generates      = []
    st_instance_names = []
    st_nodes          = []

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
                st_nodes += [nodes]

    ##KEY値の取込みフラグを立てる
        ##節点の取込みを開始する。
            if '*Node' == line:
                Read_Node = True
                

        ##要素の取込みを開始する。
            elif '*Element' in line:
                Read_Element = True
                Element_Type = spdata[1].split("=")[1] 

        ##サーフェスの取込みを開始する。
            elif '*Surface' in line:
                Read_Surface = True

        ##節点集合(Nset)と要素集合(Elset)の取込みを開始する。
            elif '*Nset' in line or '*Elset' in line:
                Read_Set = True                
                internal = False
                generate = False
                st_name = ""
                instance_name = ""

                for sp in spdata:                    
                    if "nset=" in sp or "elset=" in sp:
                        st_name = sp.split("=")[1]
                    elif "instance=" in sp:
                        instance_name = sp.split("=")[1]
                    elif sp.strip() =="internal":
                        internal = True
                    elif sp.strip() =="generate":
                        generate = True
                
                st_types += [spdata[0].replace("*","")]
                st_names += [st_name]
                st_internals += [internal]
                st_generates += [generate]
                st_instance_names += [instance_name]
                nodes = []

    ##各データの取り込みを行う。
        else:
            ##nodeの取込みを行う。
            if Read_Node:
                nid += [int(spdata[0])]
                nx  += [float(spdata[1])]
                ny  += [float(spdata[2])]
                nz  += [float(spdata[3])]

            ##Elementの取込みを行う。
            if Read_Element:
                ElementNodes = []
                for st in spdata[1:]:
                    ElementNodes.append(int(st.strip()))
                el_id     += [int(spdata[0])]
                el_types  += [Element_Type]
                el_counts += [int(len(spdata)) - 1]
                el_nodes  += [ElementNodes]
                
            if Read_Surface:



            ##節点集合(Nset)と要素集合(Elset)の取込みを行う。
            if Read_Set:
                if generate:
                    for st in range(int(spdata[0]), int(spdata[1]), int(spdata[2])):
                        nodes.append(st)
                else:
                    for st in spdata:       
                        if st.strip() != "":
                            nodes.append(st.strip())

NodesFrame   = pd.DataFrame(index=nid, data={'x':nx, 'y':ny, 'z':nz}, columns=['x', 'y', 'z'])
ElementFrame = pd.DataFrame(index=el_id, data={'type':el_types, 'count':el_counts, 'nodes':el_nodes}, columns=['type', 'count', 'nodes'])
SetFrame = pd.DataFrame(data={'name':st_names, 'type':st_types, 'instance_name':st_instance_names, 'internal':st_internals, 'generate':st_generates, 'nodes':st_nodes}, columns=['name','type', 'instance_name', 'internal', 'generate', 'nodes'])
