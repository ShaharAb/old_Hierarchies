def convert_vol_to_surf(map_to_render_path, out_path_name, surf_type):
    import os
    import pathlib

    pwd = str(pathlib.Path().resolve())
    hems = ['R', 'L']
    rh = '_' + hems[0]
    lh = '_' + hems[1]
    map_name = os.path.split(map_to_render_path)[1]
    is_rh = rh in map_name
    is_lh = lh in map_name
    all_hems = [is_rh, is_lh]
    wb_command = 'D:\\workbench\\bin_windows64\\wb_command'
    wb_command = 'wb_command'

    for i, hem in enumerate(hems):
        if not any(all_hems):
            out = f"{out_path_name}_{hem}_{surf_type}.shape.gii"
            if not os.path.isfile(out):
                map_template = os.path.join(pwd, 'HCP_WB_Tutorial_1.5_Pr_kN3mg',
                                            f"Q1-Q6_R440.{hem}.{surf_type}.32k_fs_LR.surf.gii")
                print(f"{wb_command} -volume-to-surface-mapping {map_to_render_path} {map_template} {out} -trilinear")
                os.system(f"{wb_command} -volume-to-surface-mapping {map_to_render_path} {map_template} {out} -trilinear")
        elif all_hems[i]:
            out = f"{out_path_name}_{surf_type}.shape.gii"
            if not os.path.isfile(out):
                map_template = os.path.join(pwd, 'HCP_WB_Tutorial_1.5_Pr_kN3mg',
                                            f"Q1-Q6_R440.{hem}.{surf_type}.32k_fs_LR.surf.gii")
                print(f"{wb_command} -volume-to-surface-mapping {map_to_render_path} {map_template} {out} -trilinear")
                os.system(f"{wb_command} -volume-to-surface-mapping {map_to_render_path} {map_template} {out} -trilinear")


def convert_mask_voxel2mm(data_fname_ref, data_fname_target, out_name):
    import nibabel as nib
    import numpy as np

    # this function converts a map in one resolution to another (1mm to 2mm) by transforming from the voxel to mm space
    ref_img = nib.load(data_fname_ref)
    ref_img_data = ref_img.get_fdata()
    shape_ref = ref_img.shape
    data_type = ref_img.get_data_dtype()
    # gen out matrix
    out_mat = np.zeros(shape_ref, int)
    target_img = nib.load(data_fname_target)
    target_img_data = target_img.get_fdata()
    data = target_img_data.astype(int)
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
                    vxl = vxl.astype(int)
                    # get the value of that voxel and assign it to the i,j,m voxel location in the out matrix
                    val = data[vxl[0], vxl[1], vxl[2]]
                    out_mat[i, j, m] = val
    new_img = nib.Nifti1Image(out_mat, ref_img.affine, ref_img.header)  # write mat to nifti
    nib.save(new_img, out_name)


def premotor_in_atlas(atlas_name, out_name):
    import os
    import pathlib
    import nibabel as nib
    import numpy as np
    '''
    KEY in HMAT
    Right_M1	1
    Left_M1		2
    Right_S1	3
    Left_S1		4
    Right_SMA	5
    Left_SMA	6
    Right_preSMA	7
    Left_preSMA	8
    Right_PMd	9
    Left_PMd	10
    Right_PMv	11
    Left_PMv	12
    '''

    cwd = pathlib.Path().resolve()
    '''atlas_dir = os.path.join(str(cwd.parent), 'my_ROIs/new_atlas')'''
    # load hmat and atlas maps
    hmat = nib.load(os.path.join(cwd.parent, 'HMAT_2mm.nii.gz'))
    hmat_data = hmat.get_fdata()
    hmat_data = hmat_data.astype(int)
    atlas = nib.load(atlas_name)
    atlas_data = atlas.get_fdata()
    new_data = np.zeros(atlas.shape)
    flat_nonzero_atals = np.flatnonzero(atlas_data)
    new_data.ravel()[flat_nonzero_atals] = atlas_data.ravel()[flat_nonzero_atals]

    premotor_regions_lbl = [9, 10, 11, 12]
    for lbl in premotor_regions_lbl:
        inds_in_HMAT = hmat_data == lbl
        inds_in_HMAT = inds_in_HMAT.astype(int)
        # flattening the mat and assigning according to its linear index
        flat_ind_HMAT = np.flatnonzero(inds_in_HMAT)
        new_data.ravel()[flat_ind_HMAT] = 300+lbl

        # remove cerebellum regions
        cerebel_regions = range(91, 117)
        for lbl in cerebel_regions:
            new_data[new_data == lbl] = 0

    '''out_name = os.path.join(atlas_dir, 'my_genersl_atlas.nii.gz')'''
    atlas_img = nib.Nifti1Image(new_data, atlas.affine, atlas.header)  # write mat to nifti
    nib.save(atlas_img, out_name)


def wb_convert(map_to_conv, out_name, surf_type):
    import os
    import pathlib

    wb_command = 'D:\workbench\bin_windows64\wb_command'

    cwd = pathlib.Path().resolve().parent
    left_surf = os.path.join(cwd, f"HCP_WB_Tutorial_1.5_Pr_kN3mg/Q1-Q6_R440.L.{surf_type}.32k_fs_LR.surf.gii")
    right_surf = os.path.join(cwd, f"HCP_WB_Tutorial_1.5_Pr_kN3mg/Q1-Q6_R440.R.{surf_type}.32k_fs_LR.surf.gii")

    out_left = f"{out_name}_{surf_type}_L.shape.gii"
    out_right = f"{out_name}_{surf_type}_R.shape.gii"

    os.system(f"{wb_command} -volume-to-surface-mapping {map_to_conv} {left_surf} {out_left} -trilinear")
    os.system(f"{wb_command} -volume-to-surface-mapping {map_to_conv} {right_surf} {out_right} -trilinear")


def conj_maps(map1_p, map2_p, out_name):
    import numpy as np
    import nibabel as nib
    # outputs map1 only where map2>0
    map1 = nib.load(map1_p)
    map2 = nib.load(map2_p)
    map1_data = map1.get_fdata().astype(int)
    map2_data = map2.get_fdata().astype(int)
    conj_mat = np.zeros(map1.shape, int)
    # flattening the mat and assigning according to its linear index
    map2_flat_nonzinds = np.flatnonzero(map2_data).astype(int)
    conj_mat.ravel()[map2_flat_nonzinds] = map1_data.ravel()[map2_flat_nonzinds]
    img = nib.Nifti1Image(conj_mat, map1.affine, map1.header)  # write mat to nifti
    nib.save(img, out_name)






















