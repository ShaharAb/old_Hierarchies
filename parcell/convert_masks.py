import os
import pathlib
import numpy as np
import nibabel as nib

# this scripts uses builtin fsl functions such as flirt to transform maps to different resolution (1mm to 2mm)
# but encountered a problem when loading the images

# from wb_cmd import convert_vol_to_pial

cwd = pathlib.Path().resolve()
HMAT_dir = cwd / 'new_hmat'
out_path = cwd / 'my_motor_withMNi_mask'
mni_brain = 'MNI152_T1_2mm_brain'
mni_mask = 'MNI152_T1_2mm_brain_mask'
# os.mkdir(out_path)
cnt = 0
filelist = HMAT_dir.glob('**/*.nii')
for file in filelist:
    old_file = str(file)
    old_name = str(file.stem)
    if old_name.startswith('HMAT_'):
        cnt += 1

        out_mask_path = os.path.join(out_path, f"{cnt}_{old_name}_2mm.nii.gz")
        # generate vol ROI
        # out_vol_file = pathlib.Path(out_mask_path + '.nii.gz')
        if pathlib.Path(out_mask_path).exists():
            print('done vol')
        else:
            # convert to different map resolution (1mm to 2mm)
            temp_path = os.path.join(out_path, 'temp' + old_name + '_2mm')
            cmd_1mm_to_2mm = f"flirt -in {old_file} -ref {mni_mask} -applyxfm -out {temp_path}"
            print(cmd_1mm_to_2mm)
            # os.system(cmd_1mm_to_2mm)

            '''cmd_applyisoxfm = f"flirt -in {old_file} -ref {mni_brain} -out {temp_path} -applyisoxfm 2 "
            os.system(cmd_applyisoxfm)'''
'''
            # use fslmaths to threshold and binarize the masks
            bin_path = os.path.join(out_path, 'bin_' + old_name + '_2mm.nii.gz')
            # cmd_binarize = f"fslmaths {temp_path} -thr 0.3 -bin -mul {cnt} {bin_path} "
            cmd_binarize = f"fslmaths {temp_path} -bin {bin_path} "
            os.system(cmd_binarize)
'''
'''
                # conjunct with MNI152_mask
                cmd_conj = f"fslmaths {mni_mask} -mul {bin_path} {out_mask_path} "
                os.system(cmd_conj)

                # delete the temps
                os.system(f"rm {temp_path}")
                os.system(f"rm {bin_path}")
'''
'''
flist = out_path.glob('**/*.nii.gz')
nifti_out_path = os.path.join(out_path, 'motor_ROIs')
# gen zero mat for all roi masks
mni_img = nib.load(mni_mask)
mni_shape = mni_img.shape
mni_dtype = mni_img.get_data_dtype()
general_motor_mat = np.zeros(mni_shape, mni_dtype)
cnt = 0
# combine maps as matrices
for f in flist:
    roi_file = str(f)
    if "HMAT" in roi_file:
        img = nib.load(roi_file)
        cnt += 1
        if cnt == 1:
            general_motor_mat = img.get_fdata()
        else:
            img_data = img.get_fdata()
            # add this region to the general matrix
            general_motor_mat = general_motor_mat + img_data
            general_motor_mat = np.ceil(general_motor_mat)

# write general motor martix to nifti map
new_img = nib.Nifti1Image(general_motor_mat, img.affine, img.header)
nib.save(new_img, nifti_out_path)

# generate HMAT map in pial
out_path_pial_name = out_mask_path
map_to_render_path = out_vol_file
convert_vol_to_pial(pwd, map_to_render_path, out_path_pial_name)
'''