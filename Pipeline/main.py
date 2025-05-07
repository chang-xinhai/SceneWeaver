

from app.agent.scenedesigner import SceneDesigner
from app.logger import logger
import os

def main(prompt,i):
    agent = SceneDesigner()
    try:
        # prompt = "Design me a bedroom."
        save_dir = "/mnt/fillipo/yandan/scenesage/record_scene/manus/"+prompt[:30].replace(" ","_").replace(".","").replace(",","_").replace("[","").replace("]","")
        save_dir = save_dir+"_"+str(i)
        if not os.path.exists(save_dir):
            os.system(f"mkdir {save_dir}")
            os.system(f"mkdir {save_dir}/pipeline")
        os.environ["save_dir"] = save_dir
        os.environ["UserDemand"] = prompt
        if not prompt.strip():
            logger.warning("Empty prompt provided.")
            return

        logger.warning("Processing your request...")
        agent.run(prompt)
        logger.info("Request processing completed.")
    except KeyboardInterrupt:
        logger.warning("Operation interrupted.")


if __name__ == "__main__":
    # prompts = ["Design me an office.","Design me a classroom.","Design me a gym.","Design me a game room.","Design me a children room.",
            #    "Design me a classroom."]
    # prompts = ["Design me a small shop."] #
    # prompts = ["Design me a laundromat."]
    # prompts = ["Design me a single room of restaurant."]
    prompts = ["Design me a bookstore."]
    for i in range(1):
        prompt = prompts[i]
        main(prompt,0)
