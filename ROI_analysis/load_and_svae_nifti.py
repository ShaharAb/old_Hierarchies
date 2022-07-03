import os
import pathlib
import nibabel as nib
import numpy as np

cwd = pathlib.Path().resolve()
map_file = os.path.join(cwd.parent, 'HarvardOxford-sub-prob-2mm.nii.gz')
map_img = nib.load(map_file)
map_data = map_img.get_fdata().astype(int)
one_data = map_data[:, :, :, 0]
unique_labels, counts = np.unique(one_data, return_counts=True)
unique_labels = np.asarray(unique_labels)

# flattening the mat and assigning according to its linear index
flat_inds = np.flatnonzero(one_data)
flat_inds = flat_inds.astype(int)
out_name = os.path.join(cwd.parent, 'test0_hem.nii')
my_roi_file = pathlib.Path(out_name)
if not my_roi_file.is_file():
    one_data.ravel()[flat_inds] = 1
    new_img = nib.Nifti1Image(one_data, map_img.affine, map_img.header)  # write mat to nifti
    nib.save(new_img, out_name)
