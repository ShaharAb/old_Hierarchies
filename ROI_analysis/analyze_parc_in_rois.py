import copy
import pandas as pd
import os
import pathlib
import openpyxl as pxl
import numpy as np

# this script
# load xlsx file with rois and parcells
cwd = pathlib.Path().resolve()
xls_file = os.path.join(str(cwd.parent), 'subjs_data/Group_data/intactq001_in_schaefer200_res/final_rois_table_WIN.xlsx')
df_rois = pd.read_excel(xls_file, sheet_name='PARCELS_BY_ROI')
rois_names = list()
parcs = df_rois['final_names']
parc_sizes = df_rois['rois_size']
trw_types = df_rois['final_types']
parc_lbls = df_rois['final_lbls']
# go over parcs
for parc in parcs:
    #  get the roi name
    roi_name = parc.split('_', 1)
    roi_name = roi_name[1]
    #  if exist in rois list, continue, else - push to roi list
    if roi_name not in rois_names:
        rois_names.append(roi_name)
    else:
        continue
print(rois_names)

# gen series of amount of parcs and vxls per each roi
column_names = ['roi_name', 'nparcs_t1', 'nparcs_t2', 'nparcs_t3', 'nparcs_t4','nvxls_t1',
                'nvxls_t2', 'nvxls_t3', 'nvxls_t4']
df = pd.DataFrame([], columns=column_names)

#clmn_names = ['roi_name', 'win_parc', 'parc_type', 'parc_size']
parcs_for_bars = pd.DataFrame([], columns=df_rois.columns)
# go over roi list
for roi in rois_names:
    n_parcs_in_trw = [0] * 4
    roi_vxls_in_trw = [0] * 4
    pairs = [(1, []), (2, []), (3, []), (4, [])]
    parcs_in_trw = {key: value for (key, value) in pairs}
    parcs_n_vxls_in_trw = copy.deepcopy(parcs_in_trw)

    for i, parc in enumerate(parcs):
        # search name in parcs names
        if roi in parc:
            prc_num = int(parc.split('_')[0])
            trw = trw_types[i]
            t_ind = trw - 1
            n_parcs_in_trw[t_ind] += 1
            # get the size of each parc in each trw type
            roi_vxls_in_trw[t_ind] = roi_vxls_in_trw[t_ind] + parc_sizes[i]
            parcs_in_trw[trw].append(prc_num)
            parcs_n_vxls_in_trw[trw].append(parc_sizes[i])
        #  insert number of instances(parcs) of tht roi and the sum of total voxels in all roi's parcs
    df = df.append({'roi_name': roi,
                'nparcs_t1': n_parcs_in_trw[0], 'nparcs_t2': n_parcs_in_trw[1],
                'nparcs_t3': n_parcs_in_trw[2], 'nparcs_t4': n_parcs_in_trw[3],
                'nvxls_t1': roi_vxls_in_trw[0], 'nvxls_t2': roi_vxls_in_trw[1],
                'nvxls_t3': roi_vxls_in_trw[2], 'nvxls_t4': roi_vxls_in_trw[3]}, column_names)

    # get the wining type - the TRW type -  to present for each anatomical ROI
    win_trw = np.argmax(roi_vxls_in_trw) + 1
    win_parcs = parcs_in_trw[win_trw]
    win_parcs_sz = parcs_n_vxls_in_trw[win_trw]
    max_ind = np.argmax(win_parcs_sz)
    win_parc = win_parcs[max_ind]
    win_parc_sz = win_parcs_sz[max_ind]
    win_parc_ind = np.where(parc_lbls == win_parc)
    win_parc_info = df_rois.iloc[win_parc_ind]
    '''parcs_for_bars = parcs_for_bars.append({'roi_name': roi, 'win_parc': win_parc,
                                            'parc_type': win_trw, 'parc_size': win_parc_sz}, clmn_names)'''
    parcs_for_bars = parcs_for_bars.append(win_parc_info)

excel_book = pxl.load_workbook(xls_file)
with pd.ExcelWriter(xls_file, engine='openpyxl') as writer:
    # Your loaded workbook is set as the "base of work"
    writer.book = excel_book
    # Write the new data to the file without overwriting what already exists
    df.to_excel(writer, 'parcs_dist_inROIs', index=False)
    # Save the file
    writer.save()
print(parcs_for_bars)




