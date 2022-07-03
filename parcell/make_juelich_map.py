import os
import pathlib
import numpy as np
import nibabel as nib
from ROI_funcs import convert_mask_voxel2mm

cwd = pathlib.Path().resolve().parent
file_name = os.path.join(cwd, 'Juelich_prob_2mm.nii.gz')
ref_img = nib.load(file_name)
ref_img_data = ref_img.get_fdata()
shape_ref = ref_img.shape
my_juelich_atlas = np.zeros([shape_ref[0], shape_ref[1], shape_ref[2]]).astype(int)
for roi in range(shape_ref[3]):
    roi_data = ref_img_data[:, :, :, roi]
    roi_flat_ind = np.flatnonzero(roi_data).astype(int)
    my_juelich_atlas.ravel()[roi_flat_ind] = roi+1
    if roi > 48:
        print('check')
out_name = cwd / 'my_juelich_all.nii.gz'
new_img = nib.Nifti1Image(my_juelich_atlas, ref_img.affine, ref_img.header)  # write mat to nifti
nib.save(new_img, out_name)
u = np.unique(my_juelich_atlas)

data_fname_ref = cwd / 'MNI152_T1_2mm_brain.nii.gz'
data_fname_target = out_name
out_name = cwd / 'my_juelich_all_2mm.nii.gz'
convert_mask_voxel2mm(data_fname_ref, data_fname_target, out_name)
