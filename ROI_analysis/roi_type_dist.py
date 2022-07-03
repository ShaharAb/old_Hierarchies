import pandas as pd
import os
import pathlib
import nibabel as nib
import numpy as np
import glob
import xlsxwriter

cwd = pathlib.Path().resolve()
all_t_p = os.path.join(str(cwd.parent), 'subjs_data/Group_corr_maps/WHB_maps/cdf_grad_maps/sig_types_cdf_q001.nii')
all_t_map = nib.load(all_t_p)
all_t_data = all_t_map.get_fdata().astype(int)

rois_loc = os.path.join(str(cwd.parent), 'my_ROIs/HMAT_alas116_combo/combo_atlas/ROIs')
ext = 'nii'
rois = glob.glob(f"{rois_loc}/*.{ext}")
aon_rois = [1, 2, 3, 4, 7, 8, 9, 10, 13, 14, 19, 20, 23, 24, 49, 50, 51,
            52, 53, 54, 57, 58, 59, 60, 61, 62, 65, 66, 67, 68, 81, 82, 85, 86, 209, 210, 211, 212]

column_names = ['roi_name', 'nvxls_t1', 'nvxls_t2', 'nvxls_t3', 'nvxls_t4']
df = pd.DataFrame([], columns=column_names)
for i, r in enumerate(rois):
    r_name = os.path.split(r)[1][:-(len(ext) + 1)]
    r_num = int(r_name.split("_")[0])
    if r_num in aon_rois:
        v_t_cnt = [0, 0, 0, 0]
        roi_map = nib.load(r)
        roi_data = roi_map.get_fdata().astype(int)
        # get the types of voxels in the roi
        flat_nonzind_roi = np.flatnonzero(roi_data).astype(int)
        types = all_t_data.ravel()[flat_nonzind_roi]
        u_types = np.unique(types, return_index=False, return_inverse=False, return_counts=True, axis=None)
        # try this: ###################################################
        # unique_labels, counts = np.unique(img_data, return_counts=True)
        # unique_labels = np.asarray(unique_labels)

        for n, t in enumerate(u_types[0]):
            if t > 0:
                t_cnt = u_types[1][n]
                v_t_cnt[t-1] = t_cnt

        df = df.append({'roi_name': r_name, 'nvxls_t1': v_t_cnt[0], 'nvxls_t2': v_t_cnt[1],
         'nvxls_t3': v_t_cnt[2], 'nvxls_t4': v_t_cnt[3]}, column_names)

print(df)
f_name = os.path.join(str(cwd.parent),'subjs_data/Group_corr_maps/WHB_maps/cdf_grad_maps/inflated_surf/roi_type_dist.xlsx')
# Create a workbook and add a worksheet.
datatoexcel = pd.ExcelWriter(f_name)
# write DataFrame to excel
df.to_excel(datatoexcel)
# save the excel
datatoexcel.save()





