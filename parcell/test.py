import os
import pathlib
import numpy as np
import nibabel as nib
from pathlib import Path
# from wb_cmd import convert_vol_to_pial


cwd = pathlib.Path().resolve()
fname = os.path.join(cwd, '../Parcellations/julich_from_web'
                              '/JULICH_BRAIN_CYTOARCHITECTONIC_MAPS_2_9_MNI152_2009C_NONL_ASYM.pmaps.nii.gz')

vol = spm_vol(fname)
img_arr = spm_read_vols(vol)


# file_name = os.path.join(cwd, '../Juelich_prob_2mm.nii.gz')
ref_img = nib.load(file_name)
ref_img_data = ref_img.get_fdata().astype(int)
shape_ref = ref_img.shape
'''t_data = ref_img_data[:, :, :, 70]

out_name = 'Juelich-prob-2mm_t70.nii.gz'
new_img = nib.Nifti1Image(t_data, ref_img.affine, ref_img.header)  # write mat to nifti
nib.save(new_img, out_name)'''

'''
HMAT_dir = cwd / 'HMAT/HMAT_website'
filelist = HMAT_dir.glob('**/*.nii')
for file in filelist:
    print(str(file))



out_path = os.path.join(cwd, '/myMotor_roi')
mni_brain = 'MNI152_T1_2mm_brain.nii.gz'
mni_mask = 'MNI152_T1_2mm_brain_mask.nii.gz'
# os.mkdir(out_path)

filelist = Path(HMAT_dir).glob('**/*.nii')
cnt = 0
for file in filelist:
    old_file = str(file)
    old_name = str(file.stem)

    if old_name.startswith('HMAT_'):
        cnt += 1
        print(cnt)
        out_mask_path = os.path.join(out_path, old_name + '_2mm')

        # generate vol ROI
        # convert to different map resolution (1mm to 2mm)
        out_vol_file = str(os.path.join(out_mask_path, '.nii.gz'))
        temp_path = os.path.join(out_path, 'temp' + old_name + '_2mm')
        cmd_1mm_to_2mm = f"flirt -in {old_file} -ref {mni_brain} -applyxfm -out {temp_path}"
        print(cmd_1mm_to_2mm)

'''

'''# combine maps using fslmaths
    flist = out_path.glob('**/*.nii.gz')
    cnt = 0
    nifti_out_path = os.path.join(out_path, 'motor_ROIs')
    cmd = "fslmaths"
    for f in flist:
        fpath = str(f).split('.')[0]
        if "HMAT" in fpath:
            cnt += 1
            if cnt == 1:
                cmd = f"{cmd} {fpath}"
            else:
                cmd = f"{cmd} -add {fpath}"

    # execute to generate general motor roi nifti map with roi labels
    cmd = f"{cmd} {nifti_out_path}"
    os.system(cmd)'''