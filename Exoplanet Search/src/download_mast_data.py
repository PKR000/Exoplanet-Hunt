

import os
import requests
from astroquery.mast import Catalogs, Observations, conf


#tested and working
def search_tess_targets(temp_range, dist_range):
    """
    Searches the TESS Input Catalog (TIC) and returns a list of stars that match the criteria.

    Parameters:
    temp_range (tuple): A tuple containing the minimum and maximum temperature range in Kelvin (e.g., (3000, 3100)).
    dist_range (tuple): A tuple containing the minimum and maximum distance range in parsecs (e.g., (0, 10)).

    Returns:
    Table: A table containing the catalog data of stars that match the criteria.
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


#tested and working, possibly redundant and not needed. Could likely be combined with search_tess_targets or fetch_timeseries_data
def search_tess_timeseries(tic_ids):
    """
    Verifies if TESS timeseries data exists for the given stars and returns a list of stars with and without data.

    Parameters:
    tic_ids (list): A list of TIC IDs to search for timeseries data.

    Returns:
    tuple: A tuple containing two lists - stars_with_data and stars_without_data.
    """
    stars_with_data = []
    stars_without_data = []

    if os.path.exists("stars_no_timeseries.txt"):
        with open("stars_no_timeseries.txt", "r") as file:
            dataless_stars = set(line.strip() for line in file)
    else:
        dataless_stars = set()

    for tic_id in tic_ids:
        try:
            print(f"Searching for TESS timeseries data for TIC ID: {tic_id}")
            obs_table = Observations.query_criteria(target_name=tic_id, obs_collection="TESS", dataproduct_type="timeseries")
            
            if len(obs_table) > 0:
                print(f"{tic_id}: Found {len(obs_table)} timeseries data products. \n")
                stars_with_data.append(tic_id)
            else:
                print(f"{tic_id}: No timeseries data found for TIC ID. \n")
                stars_without_data.append(tic_id)
            
                if tic_id not in dataless_stars:
                    with open("stars_no_timeseries.txt", "a") as file:
                        file.write(f"{tic_id}\n")
                    dataless_stars.add(tic_id)

        except Exception as e:
            print(f"An error occurred while searching for TIC ID {tic_id}: {e}")
    
    return stars_with_data, stars_without_data


#this one doesnt work yet
def check_known_exoplanets(stars_with_data):
    """
    Checks against ExoMAST for known exoplanets for a given list of stars with timeseries data.

    Parameters:
    stars_with_data (list): A list of TIC IDs of stars with timeseries data.

    Returns:
    list: A list of TIC IDs of stars with known exoplanets.
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


#working in its current state, tested with parameters search_tess_targets((5991,5993),(18,19)) for one star.
def fetch_timeseries_data(tic_id):
    """
    Fetches the TESS timeseries data for a given TIC ID and stores it in a specified folder.

    Parameters:
    tic_id (str): The TIC ID of the star to fetch timeseries data for.

    Returns:
    str: The path to the file containing the timeseries data.
    """
    try:
        print(f"Fetching timeseries data for TIC ID: {tic_id}")
        obs_table = Observations.query_criteria(target_name=int(tic_id), obs_collection="TESS", dataproduct_type="timeseries")

        if len(obs_table) > 0:
            data_products = Observations.get_product_list(obs_table)
            lc_products = Observations.filter_products(data_products, extension="fits", productSubGroupDescription="LC")
            download_dir = os.path.join("Downloaded Data", f"TIC {tic_id}")

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





test_target = search_tess_targets((5991,5993),(18,19))
print(test_target)
fetch_timeseries_data(test_target['ID'][0])








