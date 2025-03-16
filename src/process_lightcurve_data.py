import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

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

'''
search_result = lk.search_targetpixelfile('261136679').download()

tpf = search_result.download(quality_bitmask='default')

aperture_mask = tpf.create_threshold_mask(threshold=10)
lc = tpf.to_lightcurve(aperture_mask=aperture_mask)

flat_lc = lc.flatten(window_length=1001)
flat_lc.errorbar()

mask = (flat_lc.time < 1346) | (flat_lc.time > 1350)
masked_lc = flat_lc[mask]
masked_lc.errorbar()

masked_lc.plot()
plt.show()'
'''


#a function needs to be written that propogates through downloaded lightcurves for stars
#it will probably have to remember which stars have been analyzed by keeping a log


#needs error handling for cases where ID does not exist, tic
def create_fits_path_list(tic_id):
    """
    Given a TIC ID, returns a list of file paths to all FITS files for that star.

    Parameters:
    tic_id (str): The TIC ID of the star. Ensure this is only the number, as TIC is appended to the beginning of the ID.

    Returns:
    list: A list of file paths to all FITS files for the star.
    """
    try:
        star_directory = f"TIC {tic_id}"
        base_dir = os.path.join(os.getcwd(), "Downloaded data", star_directory)
        fits_files = glob.glob(os.path.join(base_dir, '**', '*_lc.fits'), recursive=True)

        if len(fits_files) == 0:
            print(f"No FITS files found for TIC {tic_id}. There may be no appropriate data downloaded for this star, or a typo was made when entering.")
            return None
        else:
            return fits_files

    except Exception as e:
        print(f"An error occurred while creating the FITS file path list: {e}")
    
def lightcurve_analysis(tic_id):
    """
    Analyzes the light curves for a given TIC ID.

    Parameters:
    tic_id (str): The TIC ID of the star.
    """
    fits_files_list = create_fits_path_list(tic_id)
    if fits_files_list is None:
            return

    for file in fits_files_list:
        try:
            lc = lk.read(file)
            if isinstance(lc, lk.lightcurve.TessLightCurve):
                print("Lightcurve found.")            
                lc.plot()
                plt.show()
            else:
                print(f"Error: The file provided at {file} is not a TESS lightcurve file.")
                return None
        except Exception as e:
            print(f"An error occurred while processing the file {file}: {e}")


'''
file_path = os.path.join(os.getcwd(), "Downloaded data", "TIC 261136679","mastDownload","TESS",
                         "tess2018206045859-s0001-0000000261136679-0120-s",
                         "tess2018206045859-s0001-0000000261136679-0120-s_lc.fits")
print(file_path)

lc = lk.read(file_path)
print(type(lc))

lc.plot()
plt.show()
'''


# print(create_fits_path_list("261136679"))
lightcurve_analysis(261136679)