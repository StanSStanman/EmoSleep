import xarray as xr
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as ss
from emosleep.visualization.utils import load_aparc, scaling


def plot_rois(data, pvals=None, threshold=.05, time=None, contrast=.05,
              cmap='hot_r', title=None, vlines=None, brain=False):
    
    # check that data is a 2D DataArray with the correct name of dims
    if isinstance(data, xr.DataArray):
        data_dims = data.coords._names
        assert ('roi' in data_dims and 'times' in data_dims), AssertionError(
            "DataArray must contain two dimensions with dims names "
            "'roi' and 'times'.")
    else:
        ValueError('data should be in xarray.DataArray format.')

    if data.dims == ('times', 'roi'):
        data = data.transpose('roi', 'times')

    # check if pvalues is None or a 2D DataArray with the correct dims
    if isinstance(pvals, xr.DataArray):
        pval_dims = pvals.coords._names
        assert ('roi' in pval_dims and 'times' in pval_dims), AssertionError(
            "DataArray must contain two dimensions with dims names "
            "'roi' and 'times'.")
        if pvals.dims == ('times', 'roi'):
            pvals = pvals.transpose('roi', 'times')

    else:
        assert pvals is None, ValueError('pvalues can be of type None or '
                                         'xarray.DataArray')

    # play with rois
    # standardizing names
    rois = []
    for _r in data.roi.values:
        if _r.startswith('Left-'):
            _r.replace('Left-', '')
            _r += '-lh'
        elif _r.startswith('Right-'):
            _r.replace('Right-', '')
            _r += '-rh'
        rois.append(_r)
    data['roi'] = rois

    # check if one or both hemispheres are considered
    lh_r, rh_r = [], []
    for _r in rois:
        if _r.endswith('-lh'):
            lh_r.append(_r)
        elif _r.endswith('-rh'):
            rh_r.append(_r)
        else:
            lh_r.append(_r)

    mode = 'single'
    if len(lh_r) != 0 and len(rh_r) != 0:
        mode = 'double'
        _lh = [_r.replace('-lh', '') for _r in lh_r]
        _rh = [_r.replace('-rh', '') for _r in rh_r]
        if len(lh_r) != len(rh_r):
            mode = 'bordel'
            # list of rois in lh but not in rh
            lh_uniq = list(set(lh_r) - set(rh_r))
            # list of rois in rh but not in lh
            rh_uniq = list(set(rh_r) - set(lh_r))
            # add missing right regions
            for u in lh_uniq:
                _d = xr.DataArray(np.full((1, len(data.times)), np.nan),
                                  coords=[[u.replace('-lh', '-rh')],
                                          data.times],
                                  dims=['roi', 'times'])
                data = xr.concat([data, _d], 'roi')
                if pvals is not None:
                    pvals = xr.concat([pvals, _d])
            # add missing left regions
            for u in rh_uniq:
                _d = xr.DataArray(np.full((1, len(data.times)), np.nan),
                                  coords=[[u.replace('-rh', '-lh')],
                                          data.times],
                                  dims=['roi', 'times'])
                data = xr.concat([data, _d], 'roi')
                if pvals is not None:
                    pvals = xr.concat([pvals, _d])
            # sort DataArrays by rois name
            data.sortby('roi')
            if pvals is not None:
                pvals.sortby('roi')
            # reinitialize rois lists
            _lh = [_r.replace('-lh', '') for _r in data.roi
                   if _r.endswith('-lh')]
            _rh = [_r.replace('-rh', '') for _r in data.roi
                   if _r.endswith('-rh')]

    #
    ordered_labels = load_aparc(_lh)

    # crop time window
    if time is not None:
        data = data.sel({'times': slice(time[0], time[1])})
        if pvals is not None:
            pvals = pvals.sel({'times': slice(time[0], time[1])})

    # picking data on p-values threshold
    if pvals is not None:
        pvals = pvals.fillna(1.)
        data = xr.where(pvals >= threshold, np.nan, data)

    # get colorbar limits
    if isinstance(contrast, float):
        vmin = data.quantile(contrast, skipna=True).values
        vmax = data.quantile(1 - contrast, skipna=True).values
    elif isinstance(contrast, (tuple, list)) and (len(contrast) == 2):
        vmin, vmax = contrast
    else:
        vmin, vmax = data.min(skipna=True), data.max(skipna=True)
    kwargs = dict(cmap=cmap, vmin=vmin, vmax=vmax)

    # plot specs
    if vlines is None:
        vlines = {0.: dict(color='k', linewidth=1)}
    title = '' if not isinstance(title, str) else title

    times = data.times.values.round(5)
    tp = np.hstack((np.flip(np.arange(0, times.min(), -.2)),
                    np.arange(0, times.max(), .2)))
    tp = np.unique(tp.round(3))
    time_ticks = np.where(np.isin(times, tp))[0]

    # design plots
    if mode == 'single':
        h, w = len(data.roi), 9
        if brain is True:
            fig, [lbr, lh] = plt.subplots(2, 1, figsize=(w, scaling(h)),
                                          gridspec_kw={'height_ratios':
                                                       [scaling(h), h]})
            # TODO vep plot of right hemisphere
            # TODO put a small colorbar aside
            # ma_brain = plot_vep_brain(data, ax=lbr)

            lh.pcolormesh(data.times, data.roi, data)
        else:
            fig, lh = plt.subplots(1, 1, figsize=(w, scaling(h)))

    elif mode == 'double' or mode == 'bordel':
        h, w = len(data.roi), 14
        if brain is True:
            fig, [lbr, lh, rbr, rh] = \
                plt.subplots(2, 2, figsize=(w, scaling(h)), gridspec_kw={
                    'height_ratios': [scaling(h), h, scaling(h), h]},
                             sharey=True)

            # TODO vep plot of right hemisphere
            # TODO put a small colorbar aside
            # ma_brain = plot_vep_brain(data, ax=rbr)

        else:
            fig, [lh, rh] = plt.subplots(1, 2, figsize=(w, scaling(h)))
            # fig, [lh, rh] = plt.subplots(1, 2, figsize=(14, 20))

        _data = data.sel({'roi': lh_r})
        _data['roi'] = _lh
        _data = _data.sel({'roi': ordered_labels['roi']})
        _data['roi'] = ordered_labels['label']

        if mode == 'single':
            ss.heatmap(_data.to_pandas(), yticklabels=True, xticklabels=False,
                       vmin=vmin, vmax=vmax, cmap=cmap, ax=lh,
                       zorder=0)

            for k, kw in vlines.items():
                _k = np.where(data.times.values == k)[0][0]
                lh.axvline(_k, **kw)

            lh.set_xticks(time_ticks)
            lh.set_xticklabels(tp, rotation='horizontal')
            lh.tick_params(axis='y', which='major', labelsize=10)
            lh.tick_params(axis='y', which='minor', labelsize=10)
            lh.yaxis.set_label_text('')
            plt.tight_layout()

        elif mode == 'double' or mode == 'bordel':
            ss.heatmap(_data.to_pandas(), yticklabels=True, xticklabels=False,
                       vmin=vmin, vmax=vmax, cmap=cmap, ax=lh,
                       cbar=False, zorder=0)

            for k, kw in vlines.items():
                _k = np.where(data.times.values == k)[0][0]
                lh.axvline(_k, **kw)

            lh.set_xticks(time_ticks)
            lh.set_xticklabels(tp, rotation='horizontal')

            ylabs = [item.get_text() for item in lh.get_yticklabels()]
            lh.set_yticklabels(['' for yl in ylabs])
            lh.tick_params(axis='y', bottom=True, top=False, left=False,
                           right=True, direction="out", length=3, width=1.5)
            lh.yaxis.set_label_text('')

            _data = data.sel({'roi': rh_r})
            _data['roi'] = _rh
            _data = _data.sel({'roi': ordered_labels['roi']})
            _data['roi'] = ordered_labels['label']

            ss.heatmap(_data.to_pandas(), yticklabels=True, xticklabels=False,
                       vmin=vmin, vmax=vmax, cmap=cmap, ax=rh,
                       cbar=False, zorder=0)

            for k, kw in vlines.items():
                _k = np.where(data.times.values == k)[0][0]
                rh.axvline(_k, **kw)

            rh.set_xticks(time_ticks)
            rh.set_xticklabels(tp, rotation='horizontal')
            rh.set_yticklabels(_data.roi.values, ha='center',
                               position=(-.17, -.50))
            rh.tick_params(axis='y', which='major', labelsize=9)
            rh.tick_params(axis='y', which='minor', labelsize=9)
            rh.tick_params(axis='y', bottom=True, top=False, left=True,
                           right=False, direction="out", length=3, width=1.5)
            rh.yaxis.set_label_text('')

            for ytl, col in zip(rh.get_yticklabels(), ordered_labels['color']):
                ytl.set_color(col)

            cbar = fig.add_axes([.3, .05, .4, .015])
            norm = mpl.colors.Normalize(vmin=kwargs['vmin'],
                                        vmax=kwargs['vmax'])
            cb_cmap = mpl.colormaps.get_cmap(kwargs['cmap'])
            mpl.colorbar.ColorbarBase(cbar, cmap=cb_cmap, norm=norm,
                                      orientation='horizontal')
            cbar.tick_params(labelsize=10)

            fig.tight_layout()
            fig.subplots_adjust(bottom=0.1)

    # plt.text(-45, -60, title)
    plt.figtext(0.06, 0.04, title, ha="center", fontsize=16,
                bbox={"facecolor": "white", "alpha": 0.5, "pad": 5})
    plt.show()

    return fig


if __name__ == '__main__':

    data_fname = '/media/jerry/ruggero/EmoSleep/mne/ltc/label_tc.nc'
    
    data = xr.load_dataarray(data_fname)
    data = data.rename({'time': 'times'})
    data = data.mean('trials')
    
    plot_rois(data, cmap='RdBu_r')
