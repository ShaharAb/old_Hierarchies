import os
import pathlib
import glob
from ROI_funcs import convert_vol_to_surf
from ROI_funcs import conj_maps
import nibabel as nib
import numpy as np

cwd = pathlib.Path().resolve()
'''
# change zeros to Nans in map
maps_loc = os.path.join(str(cwd.parent), 'Hierarchies/subjs_data/Group_data/intactq001_in_schaefer200_res/valid')
map_t = 'trw_schaefer200_in_sig_intact_t' 
ext = '.nii'
maps = glob.glob(f"{maps_loc}/{map_t}*{ext}")

for m in maps:
    out_path_name = f"{m[:-len(ext)]}_nans{ext}"
    print(out_path_name)
    map = nib.load(m)
    map_data = map.get_fdata()
    map_data = map_data.astype(float)
    new_data = map_data
    map_data[map_data == 0] = np.nan
    new_img = nib.Nifti1Image(new_data, map.affine, map.header)  # write mat to nifti
    nib.save(new_img, out_path_name)
   '''



# bin map
'''maps_loc = os.path.join(str(cwd.parent), 'Hierarchies/subjs_data/Group_data/intactq001_in_schaefer200_res/valid_lbls')
map_t = 'trw_schaefer200_in_sig_intact_t' 
ext = '.nii'
maps = glob.glob(f"{maps_loc}/{map_t}*{ext}")

for m in maps:
    out_path_name = f"{m[:-len(ext)]}_bin{ext}"
    print(out_path_name)
    map = nib.load(m)
    map_data = map.get_fdata()
    map_data = map_data.astype(float)
    new_data = map_data
    map_data[map_data > 0] = 1
    new_img = nib.Nifti1Image(new_data, map.affine, map.header)  # write mat to nifti
    nib.save(new_img, out_path_name)'''

# convert maps to surf
# maps_loc = os.path.join(all_maps, 'cdf_grad_maps', 'clustered')
maps_loc = os.path.join(str(cwd.parent), 'Hierarchies/subjs_data/Group_data/intactq001_in_schaefer200_res/valid_lbls')
ext = '.nii'
maps = glob.glob(f"{maps_loc}/*{ext}")

surf_type = 'inflated' 
# surf_type = 'pial'
for m in maps:
    out_path_name = m[:-len(ext)]
    convert_vol_to_surf(m, out_path_name, surf_type)


# cluster thresholding the maps

all_maps = os.path.join(str(cwd.parent.parent), 'Hierarchies', 'subjs_data', 'Group_corr_maps', 'WHB_maps')
maps_loc = os.path.join(all_maps, 'cdf_grad_maps', 'inflated_surf')
ext = 'nii'
maps = glob.glob(f"{maps_loc}/*.{ext}")
data_thresh = 0
min_thresh = 44  # in mm^3
out_clust_dir = os.path.join(all_maps, 'cdf_grad_maps', 'clustered')
for m in maps:
    in_vol = m
    f_name = os.path.split(m)[1][:-(len(ext) + 1)]
    temp_out_vol = os.path.join(out_clust_dir, f"{f_name}_{min_thresh}mm.nii")
    if not os.path.isfile(f"{temp_out_vol[:-4]}_binary.nii"):
        os.system(f"wb_command -volume-find-clusters {in_vol} {data_thresh} {min_thresh} {temp_out_vol}")
        c_map = nib.load(temp_out_vol)
        map_data = c_map.get_fdata().astype(int)
        bin_data = map_data > 0
        bin_data = bin_data.astype(int)
        img = nib.Nifti1Image(bin_data, c_map.affine, c_map.header)  # write mat to nifti
        nib.save(img, f"{temp_out_vol[:-4]}_binary.nii")


'''ext = 'gii'
maps = glob.glob(f"{maps_loc}/*.gii")
for m in maps:
    os.remove(m)'''

# conjunct atlas with reliable vxls or mask
# load atlas maps
# map1_p = os.path.join(str(cwd.parent.parent), 'Hierarchies/my_ROIs/HMAT_alas116_combo/combo_atlas.nii.gz')
'''
map1_p = os.path.join(str(cwd.parent.parent),
                      'Hierarchies/my_ROIs/schaefer/intact_reliable_q001/schaefer_200/schaefer200_in_intact_q001.nii')
map2_p = os.path.join(str(cwd.parent.parent),
                      'Hierarchies/subjs_data/Group_data/intactq001_in_schaefer200_res/trw_schaefer200_in_intact_relibl001.nii')
out_name = os.path.join(str(cwd.parent.parent),
                        'Hierarchies/my_ROIs/schaefer/intact_reliable_q001/schaefer_200/schaefer200_in_trws_intact_q001.nii')
if not os.path.isfile(out_name):
    conj_maps(map1_p, map2_p, out_name)
'''

# Gen map only in AON rois of combo116
# in file get_map_in_aon


