import os
import pathlib
import glob

cwd = pathlib.Path().resolve()
c = 'wb_command -add-to-spec-file'
# the specification file to add to
specfile = os.path.join(cwd, 'subjs_data/Group_data/intactq001_in_schaefer200_res/valid_lbls/trws_in_Schaefer_sig_intact.spec')
structure = 'CORTEX_LEFT'  # the structure of the data file
# filename = os.path.join(cwd, 'Hierarchies/subjs_data/Group_data/intactq001_in_schaefer200_res') # the path to the file
filename = os.path.join(cwd.parent,
                        'Parcellations/HCP_WB_Tutorial_1.5_Pr_kN3mg/Q1-Q6_R440.L.inflated.32k_fs_LR.surf.gii')
os.system(f"{c} {specfile} {structure} {filename}")

structure = 'CORTEX_RIGHT'
filename = os.path.join(cwd.parent,
                        'Parcellations/HCP_WB_Tutorial_1.5_Pr_kN3mg/Q1-Q6_R440.R.inflated.32k_fs_LR.surf.gii')
os.system(f"{c} {specfile} {structure} {filename}")


files_dir = os.path.join(cwd, 'subjs_data/Group_data/intactq001_in_schaefer200_res/valid_lbls')

ext = ['.nii', 'L_inflated.shape.gii', 'R_inflated.shape.gii' ]
structures = ['CORTEX', 'CORTEX_LEFT', 'CORTEX_RIGHT' ]
for i, e in enumerate(ext):
    maps = glob.glob(f"{files_dir}/*{e}")
    for m in maps:
        os.system(f"{c} {specfile} {structures[i]} {m}")



