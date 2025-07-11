import os

from app.agent.scenedesigner import SceneDesigner
from app.logger import logger


def main(prompt, i):
    agent = SceneDesigner()
    try:
        # prompt = "Design me a bedroom."
        save_dir = "/mnt/fillipo/yandan/scenesage/record_scene/manus/" + prompt[
            :30
        ].replace(" ", "_").replace(".", "").replace(",", "_").replace("[", "").replace(
            "]", ""
        )
        save_dir = save_dir + "_" + str(i)
        if not os.path.exists(save_dir):
            os.system(f"mkdir {save_dir}")
            os.system(f"mkdir {save_dir}/pipeline")
            os.system(f"mkdir {save_dir}/args")
            os.system(f"mkdir {save_dir}/record_files")
            os.system(f"mkdir {save_dir}/record_scene")

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
    prompts = ["Design me a bedroom."]
    for p in prompts:
        for i in range(1):
            prompt = p
            main(prompt, i)
