import xarray as xr


def get_data_condition(data, condition):
    conditions = {'negative': 1, 'neutral': 2, 'positive': 3}
    if isinstance(condition, str):
        condition = conditions[condition]
    if isinstance(condition, int):
        assert 1 <= condition <= 3, ValueError('condition must be 1, 2 or 3')
        
    return data.sel({'trials': data.condition == condition})


def stats_two_conditions(x, y, statfunc):
    res = statfunc(x.values, y.values, axis=-1)
    stat = xr.DataArray(res.statistic, coords=[x.roi.values, x.time.values],
                        dims=['roi', 'time'], name='statistic')
    pval = xr.DataArray(res.pvalue, coords=[x.roi.values, x.time.values],
                        dims=['roi', 'time'], name='pvalue')
    
    summary = xr.merge([stat, pval])
    
    return summary


if __name__ == '__main__':
    import scipy
    import os.path as op
    import matplotlib.pyplot as plt
    from emosleep.visualization.vis_rois import plot_rois
    # data_fname = '/media/jerry/ruggero/EmoSleep/mne/ltc/label_tc.nc'
    # data = xr.load_dataarray(data_fname)
    # x = get_data_condition(data, 1)
    # y = get_data_condition(data, 2)
    # summary = stats_two_conditions(x, y, scipy.stats.ttest_ind)
    # print(summary)
    
    datapath = '/Disk2/EmoSleep/derivatives/'
    subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 
                'sub-06', 'sub-07', 'sub-10', 'sub-11', 'sub-12', 
                'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-19', 
                'sub-22', 'sub-23', 'sub-24', 'sub-25', 'sub-26', 
                'sub-27', 'sub-28', 'sub-29', 'sub-30', 'sub-32']
    subjects = ['sub-03']
    ses = '01'

    dest_dir = '/Disk2/EmoSleep/derivatives/results/statistics'

    ltc_fname = op.join(datapath, '{0}', 'mne', 'ltc', '{0}_ses-{1}_ltc.nc')
    
    all_sbjs = []
    for sbj in subjects:
        data_fname = ltc_fname.format(sbj, ses)
        data = xr.load_dataarray(data_fname)
        data = data.sel({'times': slice(-.25, .25)})
        all_sbjs.append(data)
    all_sbjs = xr.concat(all_sbjs, 'trials')
    # all_sbjs = all_sbjs.rename({'time': 'times'})
    x = get_data_condition(all_sbjs, 1)
    y = get_data_condition(all_sbjs, 2)
    summary = stats_two_conditions(x, y, scipy.stats.ttest_ind)
    summary = summary.rename({'time': 'times'})
    
    fig = plot_rois(summary.statistic, cmap='viridis')
    plt.savefig(op.join(dest_dir, 'subjects_statistics'), format='png')
    
    fig = plot_rois(summary.pvalue)
    plt.savefig(op.join(dest_dir, 'subjects_pvals'), format='png')
