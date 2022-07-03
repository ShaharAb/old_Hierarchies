import os
import pathlib
import nibabel as nib
import numpy as np


'''
KEY
Right_M1	1
Left_M1		2
Right_S1	3
Left_S1		4
Right_SMA	5
Left_SMA	6
Right_preSMA	7
Left_preSMA	8
Right_PMd	9
Left_PMd	10
Right_PMv	11
Left_PMv	12
'''

cwd = pathlib.Path().resolve()
atlas_dir = os.path.join(str(cwd.parent), 'my_ROIs/new_atlas')
# load hmat and atlas maps
hmat = nib.load(os.path.join(atlas_dir, 'HMAT_2mm.nii.gz'))
hmat_data = hmat.get_fdata().astype(int)

atlas = nib.load(os.path.join(atlas_dir, 'atlas116_2mm.nii.gz'))
atlas_data = atlas.get_fdata().astype(int)
new_data = np.zeros(atlas.shape)
flat_nonzero_atals = np.flatnonzero(atlas_data)
new_data.ravel()[flat_nonzero_atals] = atlas_data.ravel()[flat_nonzero_atals]

special_regions_lbl = [9, 10, 11, 12]
for lbl in special_regions_lbl:
    inds_in_HMAT = hmat_data == lbl
    inds_in_HMAT = inds_in_HMAT.astype(int)
    # flattening the mat and assigning according to its linear index
    flat_ind_HMAT = np.flatnonzero(inds_in_HMAT)
    new_data.ravel()[flat_ind_HMAT] = 200+lbl
    x = sum(sum(sum(new_data == (200+lbl))))


out_name = os.path.join(atlas_dir, 'my_genersl_atlas.nii.gz')
atlas_img = nib.Nifti1Image(new_data, atlas.affine, atlas.header)  # write mat to nifti
nib.save(atlas_img, out_name)
