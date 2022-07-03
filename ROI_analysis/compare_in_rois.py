import os
import pathlib
import nibabel as nib
import numpy as np
import glob
import matplotlib
import re

import pylab as p

from roi_funcs import get_roi_type
from roi_funcs import get_roi_stats
from roi_funcs import plot_roi_bars
import pandas as pd
matplotlib.use('TkAgg')

cwd = pathlib.Path().resolve()
n_subj = 24
nii_img = nib.load(os.path.join(str(cwd.parent), 'MNI152_T1_2mm_brain.nii.gz'))
# apply fisher z transform to individual subjects data in each ROI and condition
conds = ['01_intact', '02_HG', '03_SG', '04_primitives']
all_data_mat_loc = os.path.join(str(cwd.parent), 'subjs_data/Group_data/WHB_res')
ROI_loc = os.path.join(str(cwd.parent), 'my_ROIs/my_parcels')
rois = glob.glob(f"{ROI_loc}/*.nii.gz")

vlt = []
lt = []
it = []
st = []
w = []
# get conditions means in each ROI
cnt = 0
roi_types_img = np.zeros(nii_img.shape)
for roi in rois:
    pattern = "my_ROIs/(.*?).nii.gz"
    roi_name = re.search(pattern, roi).group(1)
    print(roi_name)
    roi_img = nib.load(roi)
    roi_data = roi_img.get_fdata()
    flat_roi_inds = np.flatnonzero(roi_data).astype(int)  # inds of roi in data
    nvxls = np.size(flat_roi_inds)
    if nvxls > 10:
        cnt += 1
        sig, asts, ss_isc, ss_z = get_roi_stats(conds, all_data_mat_loc, n_subj, flat_roi_inds)

        # elocate ROI to hierarchy type
        means = np.mean(ss_isc, axis=1)
        roi_type = get_roi_type(means, sig)

        if roi_type == 'Very Long TRW':
            vlt.append(roi_name)
            label = 1
        elif roi_type == 'Long TRW':
            lt.append(roi_name)
            label = 2
        elif roi_type == 'Intermid TRW':
            it.append(roi_name)
            label = 3
        elif roi_type == 'Short TRW':
            st.append(roi_name)
            label = 4
        elif roi_type == 'Wierd':
            w.append(roi_name)
            label = 5
        roi_types_img.ravel()[flat_roi_inds] = label
        # plot isc bars with significance marking
        plot_roi_bars(asts, ss_isc, n_subj, roi_name, nvxls, conds, means, roi_type)
print(p.unique(roi_types_img))
'''my_dict = dict(Very_Long_TRW=vlt, Long_TRW=lt, Intermid_TRW=it, Short_TRW=st, Wierd=w)
df = pd.DataFrame.from_dict(my_dict, orient='index')
df = df.transpose()
out_p = os.path.join(str(cwd.parent), 'my_ROIs/rois_types.xlsx')
df.to_excel(out_p)'''

roi_types_img = roi_types_img.astype(int)
new_img = nib.Nifti1Image(roi_types_img, nii_img.affine, nii_img.header)  # write mat to nifti
out_name = cwd.parent / 'my_ROIs/roi_types_res_map.nii.gz'
nib.save(new_img, out_name)
print(cnt)
