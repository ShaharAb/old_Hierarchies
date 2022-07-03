def convert_mask_voxel2mm():
    import pathlib
    import nibabel as nib
    import numpy as np

    # this script converts a map in one resolution to another (1mm to 2mm) by transforming from the voxel to mm space

    cwd = pathlib.Path().resolve()
    data_fname_ref = cwd / 'MNI152_T1_2mm_brain.nii.gz'
    data_fname_target = cwd / 'new_hmat/HMAT.nii'
    out_name = cwd / 'my_motor/HMAT_2mm_brain.nii.gz'
    '''atlas116 = cwd / 'WFU_PickAtlas_3/WFU_PickAtlas_3.0.5b/wfu_pickatlas/MNI_atlas_templates/atlas116.nii'
    atlas116_img = nib.load(atlas116)
    shape_a116 = atlas116_img.shape'''

    ref_img = nib.load(data_fname_ref)
    ref_img_data = ref_img.get_fdata()
    shape_ref = ref_img.shape
    dtype = ref_img.get_data_dtype()
    # gen out matrix
    out_mat = np.zeros(shape_ref, dtype)
    target_img = nib.load(data_fname_target)
    target_img_data = target_img.get_fdata()
    data = target_img_data.astype(dtype)
    # iterate over row,col,mat dimensions of the image to get its x,y,z mm coords in mni
    for i in range(shape_ref[0]):
        for j in range(shape_ref[1]):
            for m in range(shape_ref[2]):
                ref_val = ref_img_data[i, j, m]
                if ref_val != 0 or np.isnan(ref_val):
                    # get the voxel location in the other image according to the mni coords
                    out_pt = nib.affines.apply_affine(ref_img.affine, [i, j, m])  # mni loc
                    # Going from mm to voxel coordinates
                    vxl = nib.affines.apply_affine(np.linalg.inv(target_img.affine), out_pt)
                    vxl = vxl.astype(dtype)
                    # get the value of that voxel and assign it to the i,j,m voxel location in the out matrix
                    val = data[vxl[0], vxl[1], vxl[2]]
                    out_mat[i, j, m] = val

    out_shape = out_mat.shape
    new_img = nib.Nifti1Image(out_mat, ref_img.affine, ref_img.header)  # write mat to nifti
    nib.save(new_img, out_name)




