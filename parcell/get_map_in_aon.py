import os
import pathlib
import numpy as np
import nibabel as nib
from ROI_funcs import conj_maps

cwd = pathlib.Path().resolve()
combo_dir = os.path.join(str(cwd.parent.parent), 'Hierarchies/my_ROIs/HMAT_alas116_combo/combo_atlas')
aon_mask = os.path.join(combo_dir, 'AON_in_combo_atlas.nii.gz')
aon_mask_file = pathlib.Path(aon_mask)
map = os.path.join(str(cwd.parent.parent), 'Hierarchies/subjs_data/Group_data/intactq001_in_schaefer200_res/'
'trw_schaefer200_in_intact_relibl001_t4.nii')
out_map_in_aon = os.path.join(str(cwd.parent.parent), 'Hierarchies/subjs_data/Group_data/intactq001_in_schaefer200_res/'
'AON_in_trw_schaefer200_in_intact_relibl001_t4.nii')

if not aon_mask_file.is_file():
    #  Gen map of AON rois in combo116
    aon_lbls_in_combo = [1, 2, 3, 4, 7, 8, 9, 10, 13, 14, 19, 20, 23, 24, 49, 50, 51,
                         52, 53, 54, 57, 58, 59, 60, 61, 62, 65, 66, 67, 68, 81, 82, 85, 86, 209, 210, 211, 212]
    combo_map = os.path.join(combo_dir, 'combo_atlas.nii.gz')
    # get only aon inds
    combo = nib.load(combo_map)
    combo_data = combo.get_fdata().astype(int)
    aon_in_combo_mask = np.zeros(combo.shape, int)
    for lbl in aon_lbls_in_combo:
        lbl_inds_in_combo = combo_data == lbl
        flat_inds = np.flatnonzero(lbl_inds_in_combo).astype(int)
        aon_in_combo_mask.ravel()[flat_inds] = 1
    # save mask as nifti
    img = nib.Nifti1Image(aon_in_combo_mask, combo.affine, combo.header)
    nib.save(img, aon_mask)


if not os.path.isfile(out_map_in_aon):
    conj_maps(map, aon_mask, out_map_in_aon)

