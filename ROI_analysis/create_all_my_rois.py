import pandas as pd
import os
import pathlib
import nibabel as nib
import numpy as np

# this script generates parcels maps of ROI that are within the localizer mask (based on individual voxels threshold)
# load xlsx file with labels
cwd = pathlib.Path().resolve()
xls_file = os.path.join(str(cwd.parent), 'my_ROIs/roi_labels.xlsx')
df = pd.read_excel(xls_file, sheet_name='both_atlases')

# load hmat and atlas maps
hmat = nib.load(os.path.join(str(cwd.parent), 'my_ROIs/hmatROIs_in_localizer.nii.gz'))
hmat_data = hmat.get_fdata().astype(int)
flat_nonzind_HMAT = np.flatnonzero(hmat_data).astype(int)
atlas = nib.load(os.path.join(str(cwd.parent), 'my_ROIs/atlas116_in_localizer.nii.gz'))
atlas_data = atlas.get_fdata().astype(int)

my_atlas_mat = np.zeros(hmat.shape, float)
# go over rows (ROIs) in first sheet
cnt = 0
for i in range(len(df)):
    cnt += 1
    if cnt > 0:
        roi = df.loc[i]
        # gen roi mat of size of n indices X 4 (conditions)
        # for each condition -
        roi_mat = np.zeros(hmat.shape, float)
        flat_ind_HMAT = []
        flat_ind_atlas = []
        #   get the inds of the curr label in HMAT and atlas rois maps
        if roi['HMAT_label'] != 0:
            inds_in_HMAT = hmat_data == roi['HMAT_label']
            # flattening the mat and assigning according to its linear index
            flat_ind_HMAT = np.flatnonzero(inds_in_HMAT)
        if roi['atlas116_label'] != 0:
            atlas_lbl = [roi['atlas116_label']]
            if isinstance(atlas_lbl, str):
                atlas_lbl = atlas_lbl.split("&")
                atlas_lbl = map(int, atlas_lbl)
            else:
                atlas_lbl = [atlas_lbl]
            for lbl in atlas_lbl:
                print(lbl)
                inds_in_atlas = atlas_data == lbl
                flat_ind_atlas = np.concatenate((flat_ind_atlas, np.flatnonzero(inds_in_atlas)), axis=0)
                # exclude inds that are not zero in hmat
            is_member = np.isin(flat_ind_atlas, flat_nonzind_HMAT)
            flat_ind_atlas = flat_ind_atlas[is_member.astype(int) == 0]
            # print(np.unique(is_member, return_counts=True))
        roi_flat_inds = np.concatenate((flat_ind_HMAT, flat_ind_atlas), axis=0)
        roi_flat_inds = roi_flat_inds.astype(int)
        # gen map of roi
        out_name = os.path.join(str(cwd.parent), f"my_ROIs/my_parcels/{roi['my_label']}_{roi['ROI_name']}.nii.gz")
        my_roi_file = pathlib.Path(out_name)
        if not my_roi_file.is_file():
            roi_mat.ravel()[roi_flat_inds] = 1
            roi_img = nib.Nifti1Image(roi_mat, hmat.affine, hmat.header)  # write mat to nifti
            nib.save(roi_img, out_name)

        my_atlas_mat.ravel()[roi_flat_inds] = roi['my_label']
# print(np.unique(my_atlas_mat, return_counts=True))
out_name = os.path.join(str(cwd.parent), f"my_ROIs/my_atlas.nii.gz")
my_atlas_file = pathlib.Path(out_name)
if not my_atlas_file.is_file():
    atlas_img = nib.Nifti1Image(my_atlas_mat, hmat.affine, hmat.header)  # write mat to nifti
    nib.save(atlas_img, out_name)







