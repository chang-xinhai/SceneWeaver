conda activate infinigen_python
#python -m infinigen.launch_blender -m infinigen_examples.generate_indoors -- --seed 0 --task coarse --output_folder outputs/indoors/coarse_notopen -g debug.gin overhead.gin singleroom.gin -p compose_indoors.terrain_enabled=False compose_indoors.overhead_cam_enabled=True restrict_solving.solve_max_rooms=1 compose_indoors.invisible_room_ceilings_enabled=True compose_indoors.restrict_single_supported_roomtype=True

python -m infinigen.launch_blender -m infinigen_examples.generate_indoors -- --seed 0 --task coarse --output_folder outputs/indoors/coarse_expand_whole -g fast_solve.gin overhead.gin studio.gin -p compose_indoors.terrain_enabled=False

