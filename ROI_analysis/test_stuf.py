import os
import pathlib
import nibabel as nib
import h5py
import numpy as np

# find my rois in AON mask
mainD = pathlib.Path().resolve()
aon = os.path.join(mainD.parent, 'action_observation_absBIn')
my_atlas = os.path.join(mainD.parent, 'my_ROIs/my_atlas')
my_atlas_in_aon = os.path.join(mainD.parent, 'my_ROIs/my_atlas_in_AON')
cmd = f"fslmaths {aon} -mul {my_atlas} {my_atlas_in_aon} "
print(cmd)
# os.system(cmd)

img = nib.load(my_atlas_in_aon)
data = img.get_fdata()
u = np.unique(data)






isc_loc = '/media/user/bigPart/DATA/analysis/Hierarchies/subjs_data/Group_data/WHB_res/sub1_01_intact_isc_img.nii'
isc_img = nib.load(isc_loc)
# data = isc_img.get_fdata()

'''new_img = nib.Nifti1Image(data, isc_img.affine, isc_img.header)  # write mat to nifti
nib.save(new_img, '/media/user/bigPart/DATA/analysis/Hierarchies/subjs_data/Group_data/WHB_res/sub1_01_intact_isc_img_test.nii')'''

c_isc = h5py.File('/media/user/bigPart/DATA/analysis/Hierarchies/subjs_data/Group_data/WHB_res/01_intact_isc_img.mat')
k = list(c_isc.keys())
isc_mat_data = c_isc[k[1]]
s1_data = isc_mat_data[:, :, :, 0]
new_img = nib.Nifti1Image(s1_data, isc_img.affine, isc_img.header)  # write mat to nifti
nib.save(new_img, '/media/user/bigPart/DATA/analysis/Hierarchies/subjs_data/Group_data/WHB_res/sub1_test_intact_fromMat2py.nii')