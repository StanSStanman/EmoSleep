import xarray as xr
from statsmodels.stats.multitest import fdrcorrection


def fdr_correction(summary, method='indep'):
    pvals = summary.pvalue.values.flatten()
    rej_pv, corr_pv = fdrcorrection(pvals=pvals,
                                    alpha=.05,
                                    method=method,
                                    is_sorted=False)
    
    rej_pv = rej_pv.reshape(summary.pvalue.shape)
    
    corr_pv = xr.DataArray(corr_pv.reshape(summary.pvalue.shape),
                           coords=summary.pvalue.coords,
                           dims=summary.pvalue.dims,
                           name='corr_pval')
    
    summary = xr.merge([summary, corr_pv])
    
    return summary, rej_pv
