import os
import pathlib
import nibabel as nib
import numpy as np
import glob
import matplotlib
import re


cwd = pathlib.Path().resolve()
# load example img for reshape
sub_func_loc = os.path.join(str(cwd.parent), 'subjs_data')
exmp_func = os.path.join(sub_func_loc, '/sub_02/deriv/WHB_24n/sub_02_run2_data.mat')

ROI_loc = os.path.join(str(cwd.parent), 'my_ROIs/my_parcels')
rois = glob.glob(f"{ROI_loc}/*.nii.gz")
#  for each ROI
for roi in rois:
    pattern = "my_ROIs/(.*?).nii.gz"
    roi_name = re.search(pattern, roi).group(1)
    print(roi_name)
    roi_img = nib.load(roi)
    roi_data = roi_img.get_fdata()
    flat_roi_inds = np.flatnonzero(roi_data).astype(int)  # inds of roi in data
    nvxls = np.size(flat_roi_inds)
    if nvxls > 10:
        #  gen figure with 4 subplots (per each condition)
        # get ROI map
        #  for each subject
        # get log file and func dir
        # for each condition
        # load func data of condition
        # reshape roi map to func shape
        # get this subect's condition average time curse across all roi voxels
        # plot the time curse in the relevant subplot

