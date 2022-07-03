import pathlib
import os
import nibabel as nib
import numpy as np
import pandas as pd

# get unique labels of ROIs mask
cwd = pathlib.Path().resolve()
mask_name = os.path.join(str(cwd.parent), 'my_ROIs/atlas116_in_localizer.nii.gz')
img = nib.load(mask_name)
img_data = img.get_fdata()
shape = img.shape
unique_labels, counts = np.unique(img_data, return_counts=True)
unique_labels = np.asarray(unique_labels)
pd.DataFrame(unique_labels).to_csv(os.path.join(str(cwd.parent), 'my_ROIs/unique_labels'), header=False, index=False)
print(counts)



