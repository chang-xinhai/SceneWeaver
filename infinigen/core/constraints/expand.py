
import copy
import mathutils
import numpy as np


EXPAND_DISTANCE = {

    #front
    "LargeShelfFactory":[0.5,0,0],
    "LargeShelfBaseFactory":[0.5,0,0],
    # "LargePlantContainerFactory":[0.5,0,0],
    "KitchenSpaceFactory":[0.5,0,0],
    "KitchenCabinetBaseFactory":[0.5,0,0],
    "KitchenCabinetFactory":[0.5,0,0],
    "CabinetDrawerBaseFactory":[0.5,0,0],
    "TVStandFactory":[0.5,0,0],
    "CabinetDoorBaseFactory":[0.5,0,0],
    "CabinetDoorIkeaFactory":[0.5,0,0],
    "CabinetBaseFactory":[0.5,0,0],
    "CellShelfFactory":[0.5,0,0],
    "CellShelfBaseFactory":[0.5,0,0],
    "SimpleBookcaseFactory":[0.5,0,0],
    "SimpleBookcaseBaseFactory":[0.5,0,0],
    "SidetableDeskFactory":[0.5,0,0],
    "SimpleDeskFactory":[0.5,0,0],
    "SimpleDeskBaseFactory":[0.5,0,0],
    "SingleCabinetFactory":[0.5,0,0],
    "SingleCabinetBaseFactory":[0.5,0,0],
    "TriangleShelfBaseFactory":[0.5,0,0],
    "TriangleShelfFactory":[0.5,0,0],
    "ArmChairFactory":[0.5,0,0],
    "SofaFactory":[0.5,0,0],
    "BathroomSinkFactory":[0.5,0,0],
    "ToiletFactory":[0.5,0,0],
    "StandingSinkFactory":[0.5,0,0],
    "OvenFactory":[0.5,0,0],
    "BeverageFridgeFactory":[0.5,0,0],
    "DishwasherFactory":[0.5,0,0],
    "MicrowaveFactory":[0.5,0,0],
    

    # front,side
    "BedFactory":[0.5,0,0.5],
    "BedFrameFactory":[0.5,0,0.5],
    
    #front,back,side
    "KitchenIslandFactory":[0.5,0.5,0.8],
    "CountertopFactory":[0.5,0.5,0.8],
   
}

def get_expand_distance(name):
    for key in EXPAND_DISTANCE.keys():
        if name.startswith(key):
            # import pdb
            # pdb.set_trace()
            print(name,EXPAND_DISTANCE[key])
            return EXPAND_DISTANCE[key]
    print(name," not expand !!!!!!!")
    return [0,0,0]


def expand_mesh(geom,name):

    d_front,d_back,d_side = get_expand_distance(name)

    if  d_front==0 and d_back==0 and d_side==0:
        mesh_copy = copy.deepcopy(geom)
        return mesh_copy

    T_old = geom.current_transform
    mesh_copy = copy.deepcopy(geom)
    mesh_copy.apply_transform(np.linalg.inv(T_old)) 
    vertices = mesh_copy.vertices
    ### move to proper pose for rescale
    # back expand = False
    back,front = vertices.min(0)[0], vertices.max(0)[0]
    left,right = vertices.min(0)[1], vertices.max(0)[1]
    v_center =  [(back+front)/2,  #back
                (left+right)/2, #left and right -> middle
                0] # do not change z, so 0 is ok
    vertices -=  v_center

    loc, rot, scale = mathutils.Matrix(T_old).decompose()
    ### rescale
    scaling_factor_front = ((front-back)/2*scale[0]+d_front)/scale[0]/((front-back)/2)
    scaling_factor_back = ((front-back)/2*scale[0]+d_back)/scale[0]/((front-back)/2)
    scaling_factor_side = ((right-left)*scale[1]+d_side)/scale[1]/(right-left)
    print(name,scaling_factor_front,scaling_factor_side)

    scale_matrix = np.eye(3)
    scale_matrix[scale_matrix[0, :]>0] *= scaling_factor_front # front
    scale_matrix[scale_matrix[0, :]<0] *= scaling_factor_back # back
    scale_matrix[1, :] *= scaling_factor_side # side
    vertices = vertices @ scale_matrix

    ### move back to original pose, finish expand
    vertices += v_center
    geom.vertices = vertices
    mesh_copy.apply_transform(T_old) 
    return mesh_copy