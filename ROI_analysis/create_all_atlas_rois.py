import pandas as pd
import os
import pathlib
import nibabel as nib
import numpy as np

# this script generates parcels maps of ROI that are within the combo (atlas116 and HMAT) mask
# load xlsx file with labels
cwd = pathlib.Path().resolve()
# xls_file = os.path.join(str(cwd.parent), 'my_ROIs/HMAT_alas116_combo/roi_list_with_relevant.xlsx')
xls_file = os.path.join(str(cwd.parent), 'subjs_data/Group_data/intactq001_in_schaefer200_res/final_rois_table.xlsx')
df = pd.read_excel(xls_file, sheet_name='Sheet1')

# load atlas maps
# atlas = nib.load(os.path.join(str(cwd.parent), 'my_ROIs/HMAT_alas116_combo/combo_atlas.nii.gz'))
# atlas = nib.load(os.path.join(str(cwd.parent), 'my_ROIs/HMAT_alas116_combo/combo_atlas/combo_in_mask_rel_intact_q001'
#                                             '.nii'))
atlas = nib.load(os.path.join(str(cwd.parent), 'my_ROIs/schaefer/intact_reliable_q001/schaefer_200'
                                               '/schaefer200_in_trws_intact_q001.nii'))
atlas_data = atlas.get_fdata().astype(int)
flat_nonzind_atlas = np.flatnonzero(atlas_data).astype(int)

out_dir = os.path.join(str(cwd.parent), 'my_ROIs/schaefer/intact_reliable_q001/schaefer_200/parcs_in_trws')

# go over rows (ROIs) in first sheet
cnt = 0
for i in range(len(df)):
    cnt += 1
    if cnt > 0:
        roi = df.loc[i]
        # gen roi mat
        roi_mat = np.zeros(atlas.shape, int)

        #   get the inds of the curr label in atlas rois map
        if roi['final_lbls'] != 0:
            inds_in_atlas = atlas_data == roi['final_lbls']
            # flattening the mat and assigning according to its linear index
            roi_flat_inds = np.flatnonzero(inds_in_atlas)
            roi_flat_inds = roi_flat_inds.astype(int)
            # print(np.unique(is_member, return_counts=True)) gen map of roi out_name = os.path.join(str(cwd.parent),
            # f"my_ROIs/HMAT_alas116_combo/all_parcells/{roi['my_lbl']}_{roi['name']}.nii.gz")
            out_name = os.path.join(str(cwd.parent),
                                    f"{out_dir}/{roi['final_names']}.nii")
            my_roi_file = pathlib.Path(out_name)
            if not my_roi_file.is_file():
                roi_mat.ravel()[roi_flat_inds] = 1
                roi_img = nib.Nifti1Image(roi_mat, atlas.affine, atlas.header)  # write mat to nifti
                nib.save(roi_img, out_name)









