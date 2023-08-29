import mne
from mne.beamformer import (make_lcmv, apply_lcmv_epochs)
import xarray as xr
import numpy as np


def compute_lcmv_sources(epo_fname, bln_fname, fwd_fname, events=None):
    # epo_fname = op.join(prep_dir.format(subject, session),
    #                     '{0}_{1}-epo.fif'.format(subject, event))
    epochs = mne.read_epochs(epo_fname, preload=True)
    epochs_ev = epochs.copy()
    if events is not None:
        assert isinstance(events, list)
        eve_pick = []
        for e in events:
            eve_pick.append(np.where(epochs_ev.events[:, -1] == e)[0])
        eve_pick = np.sort(np.concatenate((eve_pick)))
        epochs_ev = epochs_ev[eve_pick]
    epochs_ev.pick_types(eeg=True)
    # epochs_ev = apply_artifact_rejection(epochs_ev, subject, session,
    #                                      event, reject='trials')
    
    bln_epo = mne.read_epochs(bln_fname, preload=True)
    bln_epo.pick_types(eeg=True)

    # fwd_fname = op.join('/media/jerry/data_drive/data/db_mne/meg_causal',
    #                     '{0}/vep/{0}-fwd.fif'.format(subject))
    fwd = mne.read_forward_solution(fwd_fname)
    # fwd = mne.forward.convert_forward_solution(fwd, surf_ori=True,
    #                                            force_fixed=True,
    #                                            use_cps=True)
    fwd = mne.forward.convert_forward_solution(fwd, surf_ori=True,
                                               force_fixed=False,
                                               use_cps=True)
    
    # To apply a beamformer to EEG data is mandatory to have a reference 
    # projection, ww can create this by doing:
    epochs_ev = epochs_ev.set_eeg_reference(ref_channels='average',
                                            projection=True, forward=None)
    bln_epo = bln_epo.set_eeg_reference(ref_channels='average',
                                        projection=True, forward=None)
    # This is a classical method, but one can also use a REST reference, 
    # for which the forwrd model is needed in order to compute the noise 
    # outside the brain 
    # (to test, see: https://doi.org/10.1088/0967-3334/22/4/305)
    # epochs_ev = epochs_ev.set_eeg_reference(ref_channels='REST',
    #                                         projection=False, forward=fwd)
    # bln_epo = bln_epo.set_eeg_reference(ref_channels='REST',
    #                                     projection=False, forward=fwd)

    # epochs_ev = epochs_ev.filter(0.5, 20.)
    # epochs_ev.crop(-10, 1)

    # noise_cov = mne.make_ad_hoc_cov(bln_epo.info)
    # covariance = mne.compute_covariance(epochs_ev, keep_sample_mean=False,
    #                                     method='empirical', cv=10, n_jobs=-1)
    # noise_cov = mne.compute_covariance(bln_epo, method='empirical', cv=3,
    #                                    rank=None, n_jobs=-1)
    covariance = mne.compute_covariance(epochs_ev, keep_sample_mean=True,
                                        method=['shrunk', 'diagonal_fixed',
                                                'empirical'],
                                        rank=None,
                                        cv=3, n_jobs=-1)
    covariance = mne.cov.regularize(covariance, epochs_ev.info, eeg=0.1)
    noise_cov = mne.compute_covariance(bln_epo, method=['shrunk', 
                                                        'diagonal_fixed',
                                                        'empirical'],
                                       cv=3, rank=None, n_jobs=-1)
    noise_cov = mne.cov.regularize(noise_cov, epochs_ev.info, eeg=0.1)
    # covariance = mne.compute_covariance(bln_epo, keep_sample_mean=True,
    #                                     method='auto', cv=3, n_jobs=-1)
    # filters = make_lcmv(epochs_ev.info, fwd, data_cov=noise_cov,
    #                     noise_cov=None, reg=0.05, pick_ori='normal',
    #                     reduce_rank=False, inversion='matrix')
    filters = make_lcmv(epochs_ev.info, fwd, data_cov=covariance,
                        noise_cov=noise_cov, reg=0.05, pick_ori='normal',
                        weight_norm='unit-noise-gain', reduce_rank=False,
                        depth=.8, inversion='matrix')

    epochs_stcs = apply_lcmv_epochs(epochs_ev, filters, return_generator=True)

    return epochs_stcs


def compute_inverse_sources(epo_fname, bln_fname, fwd_fname):
    
    # epo_fname = op.join(prep_dir.format(subject, session),
    #                     '{0}_{1}-epo.fif'.format(subject, event))
    epochs = mne.read_epochs(epo_fname, preload=True)
    epochs_ev = epochs.copy()
    epochs_ev.pick_types(eeg=True)
    # epochs_ev = epochs_ev.apply_baseline((-.5, .5))
    # epochs_ev = apply_artifact_rejection(epochs_ev, subject, session,
    #                                      event, reject='trials')
    
    bln_epo = mne.read_epochs(bln_fname, preload=True)
    bln_epo.pick_types(eeg=True)

    # fwd_fname = op.join('/media/jerry/data_drive/data/db_mne/meg_causal',
    #                     '{0}/vep/{0}-fwd.fif'.format(subject))
    fwd = mne.read_forward_solution(fwd_fname)
    # fwd = mne.forward.convert_forward_solution(fwd, surf_ori=True,
    #                                            force_fixed=True,
    #                                            use_cps=True)
    fwd = mne.forward.convert_forward_solution(fwd, surf_ori=True,
                                               force_fixed=False,
                                               use_cps=True)
    
    # To apply a beamformer to EEG data is mandatory to have a reference 
    # projection, ww can create this by doing:
    epochs_ev = epochs_ev.set_eeg_reference(ref_channels='average',
                                            projection=True, forward=None)
    bln_epo = bln_epo.set_eeg_reference(ref_channels='average',
                                        projection=True, forward=None)
    # This is a classical method, but one can also use a REST reference, 
    # for which the forwrd model is needed in order to compute the noise 
    # outside the brain 
    # (to test, see: https://doi.org/10.1088/0967-3334/22/4/305)
    # epochs_ev = epochs_ev.set_eeg_reference(ref_channels='REST',
    #                                         projection=False, forward=fwd)
    # bln_epo = bln_epo.set_eeg_reference(ref_channels='REST',
    #                                     projection=False, forward=fwd)

    # epochs_ev = epochs_ev.filter(0.5, 20.)
    # epochs_ev.crop(-10, 1)

    # noise_cov = mne.make_ad_hoc_cov(epochs_ev.info)
    # covariance = mne.compute_covariance(epochs_ev, keep_sample_mean=False,
    #                                     method='empirical', cv=10, n_jobs=-1)
    # noise_cov = mne.compute_covariance(bln_epo, method='empirical', cv=3,
    #                                    rank=None, n_jobs=-1)
    covariance = mne.compute_covariance(epochs_ev, keep_sample_mean=True,
                                        method=['shrunk', 'diagonal_fixed',
                                                'empirical'], cv=3, n_jobs=-1)
    covariance = mne.cov.regularize(covariance, epochs_ev.info, eeg=0.1)
    # noise_cov = mne.compute_covariance(bln_epo, method=['shrunk',
    #                                                     'diagonal_fixed',
    #                                                     'empirical'],
    #                                    cv=3, rank=None, n_jobs=-1)
    # noise_cov = mne.cov.regularize(noise_cov, epochs_ev.info, eeg=0.1)
    # noise_cov = mne.compute_covariance(bln_epo, method='auto', cv=3,
    #                                    rank=None, n_jobs=-1)
    # covariance = mne.compute_covariance(bln_epo, keep_sample_mean=True,
    #                                     method='auto', cv=3, n_jobs=-1)
    # filters = make_lcmv(epochs_ev.info, fwd, data_cov=covariance,
    #                     noise_cov=noise_cov, reg=0.05, pick_ori='normal',
    #                     reduce_rank=False, inversion='matrix')
    
    inverse_operator = mne.minimum_norm.make_inverse_operator(epochs_ev.info,
                                                              fwd, covariance,
                                                              fixed=False,
                                                              loose=1.,
                                                              depth=.8)
    
    # Signal to noise ratio, one should assume an SNR of 3 for averaged and 1 
    # for non-averaged data
    snr = 1.
    lambda2 = 1. / snr ** 2
    
    epochs_stcs = mne.minimum_norm.apply_inverse_epochs(epochs_ev,
                                                        inverse_operator,
                                                        lambda2=lambda2,
                                                        method='dSPM',
                                                        label=None,
                                                        nave=1,
                                                        pick_ori='normal',
                                                        return_generator=True,
                                                        prepared=False,
                                                        method_params=None,
                                                        use_cps=True,
                                                        verbose=None)

    # epochs_stcs = apply_lcmv_epochs(epochs_ev, filters, return_generator=True)

    return epochs_stcs


def labeling(subject, subjects_dir, epochs_stcs, src_fname, ltc_fname, 
             events=None):
    labels = mne.read_labels_from_annot(subject=subject, parc='aparc',
                                        hemi='both', surf_name='white',
                                        subjects_dir=subjects_dir)
    # at least 3 vertices are needed to define an area
    lone_vertices = []
    for i, l in enumerate(labels):
        if len(l.vertices) < 3:
            lone_vertices.append(i)
    if len(lone_vertices) >= 1:
        for i in sorted(lone_vertices, reverse=True):
            del labels[i]
    
    l_name = [l.name for l in labels]
    
    sources = mne.read_source_spaces(src_fname)
    
    epo_tc = []
    for ep in epochs_stcs:
        labels_tc = ep.extract_label_time_course(labels, sources,
                                                 mode='mean_flip')
        epo_tc.append(labels_tc)
        
    epo_tc = np.stack(tuple(epo_tc), axis=-1)
    epo_label_tc = xr.DataArray(epo_tc,
                                coords=[l_name, ep.times,
                                        range(epo_tc.shape[-1])],
                                dims=['roi', 'time', 'trials'])
    
    if events is not None:
        epo_label_tc = epo_label_tc.assign_coords(condition=('trials', events))
    
    epo_label_tc.to_netcdf(ltc_fname)
    print('Labels time course saved at ', ltc_fname)
    
    return epo_label_tc
    

if __name__ == '__main__':
    subject = 'fsaverage'
    subjects_dir = '/home/jerry/freesurfer/EmoSleep'
    epo_fname = '/media/jerry/ruggero/EmoSleep/mne/epo/epochs-epo.fif'
    bln_fname = '/media/jerry/ruggero/EmoSleep/mne/epo/baseline-epo.fif'
    fwd_fname = '/media/jerry/ruggero/EmoSleep/mne/fwd/forward-fwd.fif'
    src_fname = '/media/jerry/ruggero/EmoSleep/mne/src/sources-src.fif'
    ltc_fname = '/media/jerry/ruggero/EmoSleep/mne/ltc/label_tc.nc'
    events = mne.read_epochs(epo_fname).events[:, -1]
    
    # stc = compute_lcmv_sources(epo_fname, bln_fname, fwd_fname, events=None)
    stc = compute_inverse_sources(epo_fname, bln_fname, fwd_fname)
    
    labeling(subject, subjects_dir, stc, src_fname, ltc_fname, events)
    
    # subject = 'fsaverage'
    # subjects_dir = '/home/jerry/freesurfer/EmoSleep'
    # for t in sse:
    #     stse = t
    #     break
    
    # stse.data = stse.data / 1000
    
    # stse.plot(subject=subject, surface='pial', colormap='RdBu_r', hemi='both', 
    #           subjects_dir=subjects_dir)
