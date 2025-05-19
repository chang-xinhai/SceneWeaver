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
    # prompts = ["Design me a bookstore."]
    # "Design me a meeting room."
    # "Design me a classroom."
    # "Design me a waiting room."
    # "Design me a clinic room."
    # "Design me an art studio.""
    # "Design me a kitchen."
    # "Design me a children room.", "Design me a game room.", "Design me a laboratory.","Design me a small bookstore.",
    # "Design me a waiting room.","Design me a laundry room."
    # "Design me a restaurant room.",
    # "Design me an office."
    # prompts = [
    #    "Design me a small bookstore with some shelfs, reading tables and chairs. Each shelf is full of objects and has more than 10 books inside, no book on the ground. Add lamp, books, and other objects on the table. "] #computer room
    # prompts = [
    #     "A bedroom rich of furniture, decoration on the wall, and small objects."
    # ]
    # prompts = ["An office room with desks well organized and each chair faces the desk. The room is clean and tidy. The tabletop objects are well placed with right direction (face to the chair)."]
    # prompts = ["A living room."]
    # prompts = ["A classroom for 16 students. The room is well organized with related objects. Each desk has studying objects on it. The blackboard hanges on the wall with a clock and other decorations. Shelves on the side contain several books inside."]
    # prompts = ["A laundromat with 10 machines around the room, add some washing supplies on each machine. Add other related objects, such as baskets, washthub, and clock in the room."]  # computer room
    # prompts = ["A baby room for a 1-year-old infant. Warm and detailed with daily supplies."]
    prompts = ["Design an indoor hot spring room. It has some Spa Pool and related objects. With some cabinet and shelf to store towel and cloth and other daily items."]
    # prompts = ["An office for one persion with an office desk with a chair, a vase, a bookshelf with objects, a sofa with two chairs, and some decorations on the wall. The desk has office supplies on the top."]
    for p in prompts:
        for i in range(1):
            prompt = p
            main(prompt, i)
            # try:
            #     prompt = p
            #     main(prompt, i+2)
            # except:
            #     continue
    # import sys
    # prompt = sys.argv[-2]
    # i = sys.argv[-1]
    # main(prompt, i)
