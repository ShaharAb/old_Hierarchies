import os
import pathlib
import nibabel as nib
import numpy as np
import glob
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import re
from scipy import stats



cwd = pathlib.Path().resolve()
# load all condition's isc maps
isc_loc = os.path.join(str(cwd.parent), 'subjs_data/Group_corr_maps/WHB_maps')
intact = nib.load(os.path.join(isc_loc, 'WHB_01_intact.nii'))
intact_data = intact.get_fdata()
intact_data = np.nan_to_num(intact_data, nan=0)
# intact_data[intact_data < 0] = 0

HG = nib.load(os.path.join(isc_loc, 'WHB_02_HG.nii'))
HG_data = HG.get_fdata()
HG_data = np.nan_to_num(HG_data, nan=0)
# HG_data[HG_data < 0] = 0

SG = nib.load(os.path.join(isc_loc, 'WHB_03_SG.nii'))
SG_data = SG.get_fdata()
SG_data = np.nan_to_num(SG_data, nan=0)
# SG_data[SG_data < 0] = 0

primitives = nib.load(os.path.join(isc_loc, 'WHB_04_primitives.nii'))
primitives_data = primitives.get_fdata()
primitives_data = np.nan_to_num(primitives_data, nan=0)
# primitives_data[primitives_data < 0] = 0

ROI_loc = os.path.join(str(cwd.parent), 'my_ROIs')
cnt = 0
conds = ['01_intact', '02_HG', '03_SG', '04_primitives']
rois = glob.glob(f"{ROI_loc}/*.nii.gz")
for roi in rois:
    cnt += 1
    if cnt >= 0:
        pattern = "my_ROIs/(.*?).nii.gz"
        roi_name = re.search(pattern, roi).group(1)
        print(roi_name)
        roi_img = nib.load(roi)
        roi_data = roi_img.get_fdata()
        flat_roi_inds = np.flatnonzero(roi_data).astype(int)  # inds of roi in data
        if np.size(flat_roi_inds) > 10:  # n of vxls > 10
            intact_isc = intact_data.ravel()[flat_roi_inds]
            HG_isc = HG_data.ravel()[flat_roi_inds]
            SG_isc = SG_data.ravel()[flat_roi_inds]
            primitives_isc = primitives_data.ravel()[flat_roi_inds]

            conds_isc = np.column_stack((intact_isc,HG_isc,SG_isc,primitives_isc))
            # pd.DataFrame(conds_isc).to_excel(os.path.join(str(cwd.parent), 'my_ROIs/test_roi_isc.xlsx'), header=False)
            m = np.mean(conds_isc, axis=0)
            se = np.std(conds_isc, axis=0) / np.sqrt(np.size(flat_roi_inds))
            shapiro_val = stats.shapiro(intact_isc)
            # plt.hist(intact_isc)
            res_HG = stats.ttest_rel(intact_isc, HG_isc)
            res_SG = stats.ttest_rel(intact_isc, SG_isc)
            res_prim = stats.ttest_rel(primitives_isc, HG_isc)

            # bar plot

            fig, ax = plt.subplots()
            ax.set_title(f"{roi_name} nvxls:{np.size(flat_roi_inds)}")
            plt.bar(conds, m, tick_label=conds)  ##Bar plot
            plt.errorbar(conds, m, yerr=se, fmt='o', color='Black', elinewidth=3, capthick=3, errorevery=1, alpha=1, ms=4,
                         capsize=5)
            plt.xlabel('Condition')  ## Label on X axis
            plt.ylabel('ISC')  ##Label on Y axis
            # plt.show()
