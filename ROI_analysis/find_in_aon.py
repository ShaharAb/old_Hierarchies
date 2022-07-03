import os
import pathlib
import nibabel as nib
import numpy as np

# find my rois in AON mask
mainD = pathlib.Path().resolve()
aon = os.path.join(mainD.parent, 'action_observation_absBIn.nii.gz')
my_atlas = os.path.join(mainD.parent, 'my_ROIs/my_atlas.nii.gz')
'''my_atlas_in_aon = os.path.join(mainD.parent, 'my_ROIs/my_atlas_in_AON')
cmd = f"fslmaths {aon} -mul {my_atlas} {my_atlas_in_aon} "
print(cmd)
# os.system(cmd)'''
my_atlas_img = nib.load(my_atlas)
my_atlas_data = my_atlas_img.get_fdata()

aon_img = nib.load(aon)
aon_data = aon_img.get_fdata()
my_atlas_in_aon = aon_data * my_atlas_data

u = np.unique(my_atlas_in_aon)
print(u)
