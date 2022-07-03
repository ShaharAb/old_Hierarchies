import matplotlib
matplotlib.use('TkAgg')


def plot_isc_bars(roi_name, nvxls, conds, means, se):
    import matplotlib.pyplot as plt
    # bar plot
    fig, ax = plt.subplots()
    ax.set_title(f"{roi_name} nvxls:{nvxls}")
    plt.bar(conds, means, tick_label=conds)  ##Bar plot
    plt.errorbar(conds, means, yerr=se, fmt='o', color='Black', elinewidth=3, capthick=3, errorevery=1, alpha=1, ms=4,
                 capsize=5)
    plt.xlabel('Condition')  ## Label on X axis
    plt.ylabel('ISC')  ##Label on Y axis
    plt.show()


def get_roi_type(means, sig):
    intact = means[0]
    h_goal = means[1]
    s_goal = means[2]
    prim = means[3]

    if sig[2]:  # prim is significantly different from intact
        if prim < intact:
            if sig[1]:  # SG is significantly different from intact
                if s_goal < intact:
                    if sig[0]:  # HG is significantly different from intact
                        if h_goal < intact:
                            roi_type = 'Very Long TRW'
                        else:
                            roi_type = 'Wierd'
                    else:
                        roi_type = 'Long TRW'
                else:
                    roi_type = 'Wierd'
            elif sig[0]:
                roi_type = 'Wierd'
            else:
                roi_type = 'Intermid TRW'
    elif sum(sig) > 0:
        roi_type = 'Wierd'
    else:
        roi_type = 'Short TRW'

    return roi_type


def get_roi_stats(conds, all_data_mat_loc, n_subj, flat_roi_inds):
    from scipy import stats
    import pathlib
    import os
    import nibabel as nib
    import numpy as np

    ss_isc = np.zeros([len(conds), n_subj], float)
    ss_z = ss_isc
    for c in conds:
        c_name = c.split('_')
        nc = int(c_name[0][-1])
        cond_dir = os.path.join(all_data_mat_loc, f"{c}_isc")
        # read all nii maps of subjects
        filelist = pathlib.Path(cond_dir).glob('**/*.nii')
        for idx, s_file in enumerate(filelist):
            isc_img = nib.load(s_file)
            s_data = isc_img.get_fdata()
            s_data_in_roi = s_data.ravel()[flat_roi_inds]
            s_data_in_roi[s_data_in_roi < 0] = 0  # how to deal with negative isc?
            s_mean_in_roi = np.mean(s_data_in_roi)
            if np.isnan(s_mean_in_roi):
                print(f"{s_file} is nan")
            # get mat of subjs X ROI of isc
            ss_isc[nc - 1, idx] = s_mean_in_roi
            # transform isc to fisher z
            z_s_roi = np.arctanh(s_mean_in_roi)
            # get mat of subjs X ROI of fisher z
            ss_z[nc - 1, idx] = z_s_roi

        # for each ROI - calculate ttest between condition based on all subjects' distribution of fisher z values
    res_hg = stats.ttest_rel(ss_z[0, :], ss_z[1, :])
    res_sg = stats.ttest_rel(ss_z[0, :], ss_z[2, :])
    res_prim = stats.ttest_rel(ss_z[0, :], ss_z[3, :])
    sigs = [res_hg.pvalue, res_sg.pvalue, res_prim.pvalue]
    sigs = np.array(sigs)
    asts = [' ', ' ', ' ']
    a01 = sigs <= 0.01
    a05 = sigs <= 0.05
    sig = np.zeros(3)
    for ind, i in enumerate(a05):
        if i:
            asts[ind] = '*'
            sig[ind] = 1
        elif a01[ind]:
            asts[ind] = '**'
            sig[ind] = 1
    return sig, asts, ss_isc, ss_z


def plot_roi_bars(asts, ss_isc, n_subj, roi_name, nvxls, conds, means, roi_type):
    import matplotlib.pyplot as plt
    import numpy as np

    astsToplot = [' ', asts[0], asts[1], asts[2]]
    se = np.std(ss_isc, axis=1) / np.sqrt(n_subj)
    # plot_isc_bars(roi_name, np.size(flat_roi_inds), conds, means, se)
    fig, ax = plt.subplots()
    ax.set_title(f"{roi_name} nvxls:{nvxls}\nROI type: {roi_type}")
    plt.bar(conds, means, tick_label=conds)  ##Bar plot
    plt.errorbar(conds, means, yerr=se, fmt='o', color='Black', elinewidth=3, capthick=3, errorevery=1, alpha=1,
                 ms=4,
                 capsize=5)
    plt.xlabel('Condition')  ## Label on X axis
    plt.ylabel('ISC')  ##Label on Y axis
    plt.ylim(0, 0.45)
    for ind, s in enumerate(astsToplot):
        plt.text(ind, 0.4, s, fontsize='xx-large')

    plt.show()

