from ROI_funcs import convert_mask_voxel2mm
from ROI_funcs import premotor_in_atlas
import pathlib
import os

cwd = pathlib.Path().resolve()
data_fname_ref = os.path.join(str(cwd.parent.parent), 'Hierarchies/subjs_data/group_stand_mask_MNI_newScales_24N.nii.gz')
'''
data_fname_target = cwd / 'HMAT/HMAT_Right_PMd.nii'
out_name = os.path.join(str(cwd.parent), 'Hierarchies/my_ROIs/new_atlas/HMAT_Right_PMd.nii.gz')
convert_mask_voxel2mm(data_fname_ref, data_fname_target, out_name)  # for motor HMAT parcels
'''

data_fname_target = os.path.join(str(cwd.parent), 'WFU_PickAtlas_3/WFU_PickAtlas_3.0.5b/wfu_pickatlas/MNI_atlas_templates/atlas116.nii')
out_name = os.path.join(str(cwd.parent.parent), 'Hierarchies/my_ROIs/HMAT_alas116_combo/atlas116_2mm.nii.gz')
convert_mask_voxel2mm(data_fname_ref, data_fname_target, out_name)  # for all the other parcels

atlas = out_name
out_name = os.path.join(str(cwd.parent.parent), 'Hierarchies/my_ROIs/HMAT_alas116_combo/combo_atlas116_no_cerebel.nii.gz')
premotor_in_atlas(atlas, out_name)


