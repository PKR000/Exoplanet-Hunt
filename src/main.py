def main():
    print("Welcome to Exoplanet Hunt!")

if __name__ == "__main__":
    main()


'''
Notes for how this ideally should run:
booting the program should check the previous saved state and load the checked ranges (t-eff, d) and individual stars checked vs what is downloaded.
    if something is downloaded and unchecked, start there
    if nothing is available, start at the edge t range and download data.
check new downloaded range for fits files if they exist.
    if they do, start processing.
        update the save state with completed files and stars.
    else, expand the range again.
once that range has been checked, update save state.
'''