import os

cwd = os.getcwd()
path_1mm = os.path.join(cwd, 'HMAT/HMAT_website/HMAT.nii')
out_path = os.path.join(cwd, 'new_motor/HMAT_2mm.nii.gz')
mni_brain = os.path.join(cwd, '../MNI152_T1_2mm_brain.nii.gz')
# cmd_1mm_to_2mm = f"flirt -in {path_1mm} -ref {mni_brain} -applyxfm -out {out_path}"
# os.system(cmd_1mm_to_2mm)

cmd_applyisoxfm= f"flirt -in {path_1mm} -ref {mni_brain} -out {out_path} -applyisoxfm 2 "
os.system(cmd_applyisoxfm)

