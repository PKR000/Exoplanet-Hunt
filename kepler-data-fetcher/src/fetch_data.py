

import os
import requests
# Description: This script fetches data from the MAST archive using the astroquery library.
from astroquery.mast import Catalogs, Observations, conf


#This searches the TESS Input Catalog (TIC) and returns a list of stars that match the criteria
def search_tess_targets(temp_range, dist_range):
    conf.timeout = 120  # Set the timeout to 120 seconds

    try:
        print("Attempting to fetch TESS data...")
        #search for stars in the TIC within temperature range and distance
        catalog_data = Catalogs.query_criteria(catalog="TIC", Teff=temp_range, d=dist_range)
        
        if len(catalog_data) == 0:
            print("No results found. Please expand your search criteria.")
        else:
            print(f"Total number of results: {len(catalog_data)}")
                
        return catalog_data
    
    except Exception as e:
        print(f"An error occurred during the search: {e}")
        return None


#Verifies TESS timeseries data for the given stars, returns a list of stars with and without data
def search_tess_timeseries(tic_ids):
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
            # Search for TESS observations for the given TIC ID
            obs_table = Observations.query_criteria(target_name=tic_id, obs_collection="TESS", dataproduct_type="timeseries")
            
            if len(obs_table) > 0:
                print(f"{tic_id}: Found {len(obs_table)} timeseries data products. \n")
                stars_with_data.append(tic_id)
            else:
                print(f"{tic_id}: No timeseries data found for TIC ID. \n")
                stars_without_data.append(tic_id)
            
                # Log the star to the file if it's not already logged
                if tic_id not in dataless_stars:
                    with open("stars_no_timeseries.txt", "a") as file:
                        file.write(f"{tic_id}\n")
                    dataless_stars.add(tic_id)

        except Exception as e:
            print(f"An error occurred while searching for TIC ID {tic_id}: {e}")
    
    return stars_with_data, stars_without_data


#given a list of stars with timeseries data, checks against exo.MAST for known exoplanets
def check_known_exoplanets(stars_with_data):
    stars_with_exoplanets = []
    for tic_id in stars_with_data:
        try:
            print(f"Checking for known exoplanets for TIC ID: {tic_id}")
            response = requests.get(f"https://exo.mast.stsci.edu/api/v0.1/exoplanets/{tic_id}/properties")
            if response.status_code == 200:
                data = response.json()
                if data and 'exoplanets' in data and len(data['exoplanets']) > 0:
                    print(f"{tic_id}: HAS EXOPLANETS.\n")
                    stars_with_exoplanets.append(tic_id)
                else:
                    print(f"{tic_id}: No known exoplanets found.\n")
            else:
                print(f"{tic_id}: Failed to retrieve data from ExoMAST.")
        except Exception as e:
            print(f"An error occurred while checking for exoplanets for TIC ID {tic_id}: {e}")
    
    return stars_with_exoplanets


'''
filteredStarList = search_tess_targets(temp_range=(3000, 3100), dist_range=(0, 10))

if filteredStarList is not None:
    tic_ids = filteredStarList['ID']
    stars_with_data, stars_without_data = search_tess_timeseries(tic_ids)
    
    print("Stars with timeseries data:")
    print(stars_with_data)
    
    print("Stars without timeseries data:")
    print(stars_without_data)
    
    stars_with_exoplanets = check_known_exoplanets(stars_with_data)
    print("Stars with known exoplanets:")
    print(stars_with_exoplanets)

'''

stars_with_planets = [12723961,180695581,116242971]
list = check_known_exoplanets(stars_with_planets)
print(list)










