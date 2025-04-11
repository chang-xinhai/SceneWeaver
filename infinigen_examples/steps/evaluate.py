
def eval_metric(state,):
    
    return 

def eval_physics_score(state):
    Nobj = 0
    for name,info in state.objs.items():
        if name.startswith("window") or name=="newroom_0-0" or name=="entrance":
                continue
        else:
            Nobj += 1
    
    OOB = 0
    BBL = 0
    return Nobj,OOB,BBL


def eval_general_score():
    real = 0
    func = 0
    complet = 0
    return real,func,complet

def eval_align_score():
    GPT_sim = 0
    CLIP_sim = 0
    return GPT_sim, CLIP_sim