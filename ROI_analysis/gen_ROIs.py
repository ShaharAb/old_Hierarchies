import os
from pathlib import Path

pwd = Path().resolve().parent
hmat_map = os.path.join(str(pwd.parent), 'Parcellations/my_rois/HMAT_2mm_brain.nii.gz')
localizer_map = os.path.join(str(pwd), 'subjs_data/Group_corr_maps/WHB_maps/func_localizer_mask_24n.nii')
atlas116_map = os.path.join(str(pwd.parent), 'Parcellations/my_rois/atlas116_2mm.nii.gz')

localizer_hmat = os.path.join(str(pwd), 'test/hmatROIs_in_localizer.nii.gz')
# conjunct maps with localizer
conj_cmd = f"fslmaths {hmat_map} -mul {localizer_map} {localizer_hmat}"
print(conj_cmd)
os.system(conj_cmd)

localizer_atlas116 = os.path.join(str(pwd), 'test/atlas116_in_localizer.nii.gz')
# conjunct maps with localizer
conj_cmd = f"fslmaths {atlas116_map} -mul {localizer_map} {localizer_atlas116}"
print(conj_cmd)
os.system(conj_cmd)


