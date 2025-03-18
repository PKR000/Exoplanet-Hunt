import os
import requests
from astroquery.mast import Catalogs, Observations, conf
import warnings
import json

class TESSDataHandler:
    def __init__(self):
        self.data_dir = "data"
        self.data_file = os.path.join(self.data_dir, "stars_timeseries_data.json")
        self.stars_data = {"with_timeseries": set(), "without_timeseries": set()}
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)


    def load_state(filename='saved_state.json'):
        """
        Loads the saved state from a JSON file.

        Args:
            filename (str): The name of the JSON file to load the state from.

        Returns:
            tuple: A tuple containing the temperature range, distance range, and analyzed TIC IDs.
                   If the file does not exist, returns (None, None, []).
        """
        filepath = os.path.join(os.getcwd(), "logs", filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                existing_state = json.load(file)

                existing_temp_range = existing_state['temperature_range']
                existing_dist_range = existing_state['distance_range']
                analyzed_tic_ids = existing_state['analyzed_tic_ids']

                return existing_temp_range, existing_dist_range, analyzed_tic_ids

        else:
            print("No save file found.")
            return None, None, []


    def save_state(temp_range, dist_range, analyzed_tic_ids, filename='saved_state.json'):
        """
        Saves the current state to a JSON file. If the file already exists, it updates the existing state.

        Args:
            temp_range (tuple): The temperature range to save (low, high).
            dist_range (tuple): The distance range to save (low, high).
            analyzed_tic_ids (list): The list of analyzed TIC IDs to save.
            filename (str): The name of the JSON file to save the state to.
        """
        # Initialize state
        state = {
            'temperature_range': temp_range,
            'distance_range': dist_range,
            'analyzed_tic_ids': analyzed_tic_ids
        }
        filepath = os.path.join(os.getcwd(), "logs",filename)
        # Read existing state if the file exists
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                existing_state = json.load(file)

                # Update tested temperature range
                existing_temp_range = existing_state['temperature_range']
                state['temperature_range'] = (
                    min(existing_temp_range[0], temp_range[0]),
                    max(existing_temp_range[1], temp_range[1])
                )

                # Update tested distance range
                existing_dist_range = existing_state['distance_range']
                state['distance_range'] = (
                    min(existing_dist_range[0], dist_range[0]),
                    max(existing_dist_range[1], dist_range[1])
                )

                # Update analyzed TIC IDs
                state['analyzed_tic_ids'] = list(set(existing_state['analyzed_tic_ids']).union(set(analyzed_tic_ids)))

        # Write the updated state to the JSON file
        with open(filepath, 'w') as file:
            json.dump(state, file, indent=4)
        
    def search_tess_targets(self, temp_range, dist_range): 
        """
        Searches the TESS Input Catalog (TIC) and returns a list of stars that match the criteria.
        """
        conf.timeout = 120
        try:
            print("Attempting to fetch TESS data...")
            catalog_data = Catalogs.query_criteria(catalog="TIC", Teff=temp_range, d=dist_range)
            if len(catalog_data) == 0:
                print("No results found. Please expand your search criteria.")
            else:
                print(f"Total number of results: {len(catalog_data)}")
            return catalog_data
        except Exception as e:
            print(f"An error occurred during the search: {e}")
            return None

    def verify_tess_timeseries(self, tic_ids):
        """
        Verifies if TESS timeseries data exists for the given stars and returns a list of stars with and without data.
        """
        stars_with_data = []
        stars_without_data = []
        for tic_id in tic_ids:
            try:
                print(f"Searching for TESS timeseries data for TIC ID: {tic_id}")
                obs_table = Observations.query_criteria(target_name=tic_id, obs_collection="TESS", dataproduct_type="timeseries")
                if len(obs_table) > 0:
                    print(f"{tic_id}: Found {len(obs_table)} timeseries data products. \n")
                    stars_with_data.append(tic_id)
                    self.stars_data["with_timeseries"].add(tic_id)
                else:
                    print(f"{tic_id}: No timeseries data found for TIC ID. \n")
                    stars_without_data.append(tic_id)
                    self.stars_data["without_timeseries"].add(tic_id)
            except Exception as e:
                print(f"An error occurred while searching for TIC ID {tic_id}: {e}")
        return stars_with_data, stars_without_data

    def fetch_timeseries_data(self, tic_id):
        """
        Fetches the TESS timeseries data for a given TIC ID and stores it in a specified folder.
        """
        try:
            print(f"Fetching timeseries data for TIC ID: {tic_id}")
            obs_table = Observations.query_criteria(target_name=int(tic_id), obs_collection="TESS", dataproduct_type="timeseries")
            if len(obs_table) > 0:
                data_products = Observations.get_product_list(obs_table)
                lc_products = Observations.filter_products(data_products, extension="fits", productSubGroupDescription="LC")
                download_dir = os.path.join(self.data_dir, "TESS_Downloads", f"TIC_{tic_id}")
                if len(lc_products) > 0:
                    os.makedirs(download_dir, exist_ok=True)
                    manifest = Observations.download_products(lc_products, download_dir=download_dir)
                    if len(manifest) > 0:
                        print(f"Downloaded lightcurve data for TIC ID {tic_id} to {manifest['Local Path'][0]}")
                        return manifest['Local Path'][0]
                    else:
                        print(f"Failed to download lightcurve data for TIC ID {tic_id}.")
                        return None
                else:
                    print(f"No lightcurve data found for TIC ID {tic_id}.")
                    return None
            else:
                print(f"No timeseries data found for TIC ID {tic_id}.")
                return None
        except Exception as e:
            print(f"An error occurred while fetching timeseries data for TIC ID {tic_id}: {e}")
            return None

    def check_known_exoplanets(self, stars_with_data):
        warnings.warn("check_known_exoplanets is deprecated and will be removed in a future version.", DeprecationWarning)
        """
        Checks against ExoMAST for known exoplanets for a given list of stars with timeseries data.
        """
        stars_with_exoplanets = []
        for tic_id in stars_with_data:
            try:
                print(f"Checking for known exoplanets for TIC ID: {tic_id}")
                response = requests.get(f"https://exo.mast.stsci.edu/api/v0.1/exoplanets/{tic_id}/properties")
                if response.status_code == 200:
                    data = response.json()
                    print(f"Response data for TIC ID {tic_id}: {data}")
                    if data and 'exoplanets' in data and len(data['exoplanets']) > 0:
                        print(f"{tic_id}: HAS EXOPLANETS.\n")
                        stars_with_exoplanets.append(tic_id)
                    else:
                        print(f"{tic_id}: No known exoplanets found.\n")
                else:
                    print(f"{tic_id}: Failed to retrieve data from ExoMAST.\n")
            except Exception as e:
                print(f"An error occurred while checking for exoplanets for TIC ID {tic_id}: {e}")
        return stars_with_exoplanets

    def output_stars_data(self):
        """
        Outputs the stars data to a JSON file.
        """
        with open(self.data_file, "w") as file:
            json.dump({"with_timeseries": list(self.stars_data["with_timeseries"]),
                       "without_timeseries": list(self.stars_data["without_timeseries"])}, file)

#commented out for testing
'''
if __name__ == "__main__":
    # Example usage
    handler = TESSDataHandler()
    
    # Test search_tess_targets method
    test_temp = (5991, 5993)
    test_dist = (18, 19)
    test_target = handler.search_tess_targets(test_temp, test_dist)
    print(test_target)
    
    if test_target:
        # Test fetch_timeseries_data method
        handler.fetch_timeseries_data(test_target['ID'][0])
        
        # Test verify_tess_timeseries method
        stars_with_data, stars_without_data = handler.verify_tess_timeseries(test_target['ID'])
        print(f"Stars with data: {stars_with_data}")
        print(f"Stars without data: {stars_without_data}")
        
        # Test check_known_exoplanets method
        # stars_with_exoplanets = handler.check_known_exoplanets(stars_with_data)
        # print(f"Stars with known exoplanets: {stars_with_exoplanets}")
        
        # Test output_stars_data method
        handler.output_stars_data()  # Example of using the public method to output stars data
'''



#im keeping a to-do list here for now
        
    #to-do: we need a score function that tells us the chance we found an exoplanet.
    #to-do: we need a function that increments through temp/dist ranges and downloads relevant data.
#this is possibly done: we need to log tested stars, and ranges we have gone through.
    #to-do: we might consider saving graphs of processed data, once we have confidence in the output.
