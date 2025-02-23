import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np

'''
# Search and download all available target pixel files for the given target and quarter
pixelfiles = lk.search_targetpixelfile('KIC 6922244', quarter=4).download_all()

# Check if there are any pixel files downloaded
if pixelfiles:
    # Get the last TargetPixelFile object
    last_pixelfile = pixelfiles[-1]
    
    # Convert the last target pixel file to a light curve
    lc = last_pixelfile.to_lightcurve(aperture_mask=last_pixelfile.pipeline_mask)
    
    # flattens the light curve to be more readable; normalizes the data
    flat_lc = lc.flatten(window_length=401) #dunno where window length comes from?
    #flat_lc.plot() 
    
    #periodograms solve for the transit period
    periodogram = flat_lc.to_periodogram(method='bls', period=np.arange(.3, 10, 0.001), duration=.2)
    best_fit = periodogram.period_at_max_power
    print('Best fit period: {:.5f}'.format(best_fit))

    #folds the light curve to show the transit
    folded_lc = flat_lc.fold(period=best_fit)
    folded_lc.plot()

    #binning averages surrounding data points to make the light curve more readable
    binned_lc = folded_lc.bin(binsize=5)
    binned_lc.plot()
    
    #Can do all of the previous functions at once with a single messy line:
    lc.remove_nans().flatten(window_length=401).fold(period=best_fit).bin(binsize=5).plot()

    plt.show()
else:
    print("No pixel files found.")  
'''


search_result = lk.search_targetpixelfile('Pi Mensae', mission='TESS',sector=1)
tpf = search_result.download(quality_bitmask='default')
aperture_mask = tpf.create_threshold_mask(threshold=10)
lc = tpf.to_lightcurve(aperture_mask=aperture_mask)

flat_lc = lc.flatten(window_length=1001)
flat_lc.errorbar()

mask = (flat_lc.time < 1346) | (flat_lc.time > 1350)
masked_lc = flat_lc[mask]
masked_lc.errorbar()

masked_lc.plot()
plt.show()