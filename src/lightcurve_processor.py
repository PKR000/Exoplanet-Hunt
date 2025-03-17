import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from typing import List

class LightCurveProcessor:
    def __init__(self, tic_id):
        self.tic_id = tic_id
        self.data_dir = "data/TESS_Downloads"
        self.fits_files_list = self.get_fits_files()

    def get_fits_files(self) -> List[str]:
        """
        Find all FITS files for a given TIC ID in the data directory.
        
        Returns:
            List[str]: Sorted list of paths to FITS files for the given TIC ID
        """
        try:
            star_directory = f"TIC_{self.tic_id}"
            base_dir = os.path.join(self.data_dir, star_directory).replace('\\', '/')
            search_pattern = os.path.join(base_dir, '**', '*_lc.fits').replace('\\', '/')
            fits_files = glob.glob(search_pattern, recursive=True)

            if len(fits_files) == 0:
                print(f"No FITS files found for TIC {self.tic_id}. There may be no appropriate data downloaded for this star, or a typo was made when entering.")
                return []
            else:
                print(f"Found {len(fits_files)} FITS files for TIC {self.tic_id}.")
                return fits_files

        except Exception as e:
            print(f"An error occurred while creating the FITS file path list: {e}")
            return []

    def analyze_lightcurves(self):
        """
        Analyzes the light curves for the given TIC ID.
        """
        if not self.fits_files_list:
            return

        for file in self.fits_files_list:
            self.analyze_single_lightcurve(file)

    def analyze_single_lightcurve(self, file: str):
        """
        Analyzes a single light curve file.
        
        Args:
            file (str): Path to the light curve file.
        """
        try:
            lc = lk.read(file)
            if isinstance(lc, lk.lightcurve.TessLightCurve):
                self.process_lightcurve(lc)
            else:
                print(f"Error: The file provided at {file} is not a TESS lightcurve file.")
        except Exception as e:
            print(f"An error occurred while processing the file {file}: {e}")

    def calculate_window_length(self, lc: lk.lightcurve.TessLightCurve, resolution: float = 0.1) -> int:
        """
        Calculate the window length for flattening the lightcurve data.
        
        Args:
            lc (lk.lightcurve.TessLightCurve): The lightcurve data.
            resolution (float): The desired resolution in days. Default is 0.1 days.
        
        Returns:
            int: The calculated window length.
        """
        duration = (lc.time[-1] - lc.time[0]).value  # Convert TimeDelta to days
        window_length = int(duration / resolution)
        return window_length

    def process_lightcurve(self, lc: lk.lightcurve.TessLightCurve):
        """
        Processes a given light curve.
        """
        print(f"Processing light curve for TIC ID {self.tic_id}")
        try:
            lc = lc.remove_nans().remove_outliers(sigma=4)
            lc.plot(title="outliers removed")
            lc.

            # Calculate window length
            window_length = self.calculate_window_length(lc, 0.1)
            print(f"Window length: {window_length}")
            
            # Flatten the light curve
            flat_lc = lc.flatten(window_length=window_length)
            flat_lc.plot(title="flattened")
            plt.show()
            
            # Generate periodogram to determine largest peak (exoplanet period)
            periodogram = flat_lc.to_periodogram(method='bls', period=np.arange(.3, 10, 0.001), duration=.2)
            periodogram.plot()
            best_fit = periodogram.period_at_max_power
            print('Best fit period: {:.5f}'.format(best_fit))

            #Scores the periodogram based on the ratio of the highest peak to the average power
            max_power = periodogram.power.max()
            average_power = np.mean(periodogram.power)
            ratio = max_power / average_power
            print("Periodogram Ratio:", ratio)

            # Fold the light curve to show the transit            
            folded_lc = flat_lc.fold(period=best_fit)
            
            # Bin the light curve using the time bin size
            binned_lc = folded_lc.bin(time_bin_size=0.005)  # Adjust the time bin size as needed
            
            # Plot the processed light curve
            binned_lc.plot(title="processed")
        except Exception as e:
            print(f"An error occurred while processing the light curve: {e}")
            
    def display_raw_lightcurves(self):
        """
        Displays the raw light curves from the FITS files.
        """
        if not self.fits_files_list:
            return

        for file in self.fits_files_list:
            self.display_single_lightcurve(file)

    def display_single_lightcurve(self, file: str):
        """
        Displays a single light curve file.
        
        Args:
            file (str): Path to the light curve file.
        """
        try:
            lc = lk.read(file)
            if isinstance(lc, lk.lightcurve.TessLightCurve):
                print(f"Displaying raw lightcurve for file: {file}")
                lc.plot()
            else:
                print(f"Error: The file provided at {file} is not a TESS lightcurve file.")
        except Exception as e:
            print(f"An error occurred while displaying the file {file}: {e}")

# Example usage
if __name__ == "__main__":
    processor = LightCurveProcessor(261136679)
    if processor.fits_files_list:
        # processor.display_single_lightcurve(processor.fits_files_list[1])
        processor.analyze_single_lightcurve(processor.fits_files_list[1])
        plt.show()
