import os
import pathlib

cwd = pathlib.Path().resolve().parent

map_to_conv = os.path.join(cwd.parent, 'Hierarchies/subjs_data/Group_corr_maps/WHB_maps/grad_all_maps.nii')
left_pial = os.path.join(cwd, 'HCP_WB_Tutorial_1.5_Pr_kN3mg/Q1-Q6_R440.L.pial.32k_fs_LR.surf.gii')
right_pial = os.path.join(cwd, 'HCP_WB_Tutorial_1.5_Pr_kN3mg/Q1-Q6_R440.R.pial.32k_fs_LR.surf.gii')

out_left = os.path.join(cwd.parent, 'Hierarchies/subjs_data/Group_data/combo_ROIs_res/loc_in_combo_atlas116_L.shape.gii')
out_right = os.path.join(cwd.parent, 'Hierarchies/subjs_data/Group_data/combo_ROIs_res/loc_in_combo_atlas116_R.shape.gii')

os.system(f"wb_command -volume-to-surface-mapping {map_to_conv} {left_pial} {out_left} -trilinear")
os.system(f"wb_command -volume-to-surface-mapping {map_to_conv} {right_pial} {out_right} -trilinear")

