import json
import re
from functools import reduce
import method_3_SD_iter1_prompt as prompts
from gpt import GPT4
from prompt_room import extract_json, dict2str, lst2str
import sys


def generate_scene_iter1(user_demand,iter):

    gpt = GPT4()

    results = dict()
    render_path = f"/home/yandan/workspace/infinigen/render{iter-1}+.jpg"
    with open(f"/home/yandan/workspace/infinigen/layout{iter-1}+.json", "r") as f:
        layout = json.load(f)
    action="Add books and stationery on the desks and shelves."
    roomsize = layout["roomsize"]
    roomsize_str = f"[{roomsize[0]},{roomsize[1]}]"
    step_1_big_object_prompt_user = prompts.step_1_big_object_prompt_user.format(demand=user_demand, 
                                                               roomsize = roomsize_str,
                                                               scene_layout=layout["objects"],
                                                               action=action)
    
    prompt_payload = gpt.get_payload_scene_image(prompts.step_1_big_object_prompt_system, 
                                                 step_1_big_object_prompt_user,
                                                 render_path)
    gpt_text_response = gpt(payload=prompt_payload, verbose=True)
    print(gpt_text_response)

    gpt_dict_response = extract_json(gpt_text_response)
    results = gpt_dict_response
    

if __name__ == "__main__":
    # user_demand = "Add floor lamp next to the armchair and wall art above the sofa."
    user_demand = "CLassroom."
    generate_scene_iter1(user_demand,iter=9)
