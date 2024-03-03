import glob
import pandas as pd



def cycle_generator(df_path, head, foot, colnames, year):
    """
    Function to parse a df_path containing an AAMC table.
    Supply the row number for the header (contains "State and Medical School"), footer (row number of the "Totals"), column names, and year.
    Returns a cleaned AAMC table A-1 or B-8 df or a totals df.
    """
    # Reading in the excel file, assigning column names, and cutting the footer off
    df = pd.read_excel(df_path, header=head - 1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    df.columns = colnames
    df = df.iloc[0:foot - head, ]
    df["state"] = df["state"].fillna(method="ffill")

    # Select the totals category that averages up all results
    totals = df[df["state"].str.contains("Total")]
    totals = totals.assign(cycle_year=year)

    # Dropping the totals column, assigning the year, and returning the dfs
    df = df.iloc[0:len(df) - 1, ]
    df = df.assign(cycle_year=year)
    return (df, totals)



def demo_generator(df_path, head, foot, year):
    """Function to parse and clean an A-10 file from the AAMC.

    Args:
        df_path (string): filepath to A-10 xlsx file
        head (int): index for the column names
        foot (int): index for when to stop reading rows
        year (int): year that the data was submitted

    Returns:
        df: df of the main a-10 data
        df_totals: df of the total summarized a-10 data
    """
    # Importing the dfs
    df = pd.read_excel(df_path, header=head)
    
    # Column names
    colnames = ["region", "state", "American Indian or Alaska Native", "Asian", "Black or African American", "Hispanic, Latino, or of Spanish Origin", "Native Hawaiian or Other Pacific Islander", "White", "Other", "Multiple Race/Ethnicity", "Unknown Race/Ethnicity", "Non-U.S. Citizen and Non-Permanent Resident", "Total"]
    df.columns = colnames
    
    # Excluding the footer
    df = df.iloc[0:foot, ]
    
    # Getting the total applicants
    df_totals = df.iloc[len(df) - 1, ]
    df_totals = pd.DataFrame(df_totals).reset_index()
    df_totals = df_totals.transpose()
    df_totals.columns = df_totals.iloc[0]
    df_totals = df_totals.drop(df_totals.index[0])
    df_totals["year"] = year
    
    # Filtering any NA lines in "state" column and tidying with year and APSA State mapping
    df = df[df["state"].notna()]
    df["region"] = df["region"].fillna(method="ffill")
    df = df[df["state"] != "All for the Region"]
    df = df[df["state"] != "Total for the Region"]
    df["year"] = year
    apsa_state_mapping = {
        "Alabama": "South",
        "Alaska": "West",
        "Arizona": "South",
        "Arkansas": "West",
        "California": "West",
        "Colorado": "West",
        "Connecticut": "Northeast",
        "District of Columbia": "Mid-Atlantic",
        "Delaware": "Mid-Atlantic",
        "Florida": "South",
        "Georgia": "South",
        "Hawaii": "West",
        "Idaho": "West",
        "Iowa": "Midwest",
        "Illinois": "Midwest",
        "Indiana": "Midwest",
        "Kansas": "Midwest",
        "Kentucky": "South",
        "Louisiana": "South",
        "Maine": "Northeast",
        "Massachusetts": "Northeast",
        "Maryland": "Mid-Atlantic",
        "Michigan": "Midwest",
        "Minnesota": "Midwest",
        "Missouri": "Midwest",
        "Mississippi": "South",
        "Montana": "West",
        "North Carolina": "South",
        "North Dakota": "Midwest",
        "Nebraska": "Midwest",
        "New Hampshire": "Northeast",
        "New Jersey": "Mid-Atlantic",
        "New Mexico": "West",
        "Nevada": "West",
        "New York": "Northeast",
        "Ohio": "Midwest",
        "Oklahoma": "South",
        "Oregon": "West",
        "Pennsylvania": "Mid-Atlantic",
        "Puerto Rico": "South",
        "Rhode Island": "Northeast",
        "South Carolina": "South",
        "South Dakota": "Midwest",
        "Tennessee": "South",
        "Texas": "South",
        "Utah": "West",
        "Virginia": "Mid-Atlantic",
        "Vermont": "Northeast",
        "Washington": "West",
        "Wisconsin": "Midwest",
        "West Virginia": "Mid-Atlantic",
        "Wyoming": "West"
        }
    df["APSA_region"] = df["state"].map(apsa_state_mapping)
    
    return df, df_totals



def a1_merger(a1_filepath):
    """
    Function to parse a folder of AAMC A-1 tables.
    Provide the filepath to the folder containing all AAMC A-1 tables.
    Returns a merged df of table A1 containing all schools merged according to year and a merged totals df.
    """
    # AAMC A-1 tables file paths for all excel files
    file_list_a1 = glob.glob(a1_filepath)

    # Column names for every excel file
    colnames1 = ["state", "school", "applications", "in state applicants", "out of state applicants",
                 "women applicants", "men applicants", "matriculants", "in state matriculants",
                 "out of state matriculants", "women matriculants", "men matriculants"]
    colnames2 = ["state", "school", "applications", "in state applicants", "out of state applicants", "men applicants",
                 "women applicants", "matriculants", "in state matriculants", "out of state matriculants",
                 "men matriculants", "women matriculants"]  # column names men/women change in 2018

    # Processing all AAMC A-1 Tables
    a1_2012, totals_2012 = cycle_generator(df_path=file_list_a1[0], head=10, foot=148, colnames=colnames1, year=2012)
    a1_2013, totals_2013 = cycle_generator(df_path=file_list_a1[1], head=10, foot=152, colnames=colnames1, year=2013)
    a1_2014, totals_2014 = cycle_generator(df_path=file_list_a1[2], head=10, foot=153, colnames=colnames1, year=2014)
    a1_2015, totals_2015 = cycle_generator(df_path=file_list_a1[3], head=9, foot=153, colnames=colnames1, year=2015)
    a1_2016, totals_2016 = cycle_generator(df_path=file_list_a1[4], head=9, foot=156, colnames=colnames1, year=2016)
    a1_2017, totals_2017 = cycle_generator(df_path=file_list_a1[5], head=9, foot=157, colnames=colnames1, year=2017)
    a1_2018, totals_2018 = cycle_generator(df_path=file_list_a1[6], head=9, foot=161, colnames=colnames2, year=2018)
    a1_2019, totals_2019 = cycle_generator(df_path=file_list_a1[7], head=9, foot=163, colnames=colnames2, year=2019)
    a1_2020, totals_2020 = cycle_generator(df_path=file_list_a1[8], head=9, foot=165, colnames=colnames2, year=2020)
    a1_2021, totals_2021 = cycle_generator(df_path=file_list_a1[9], head=9, foot=165, colnames=colnames2, year=2021)

    # Concatenating the totals per year and cleaning
    totals = pd.concat([totals_2012, totals_2013, totals_2014, totals_2015, totals_2016, totals_2017, totals_2018,
                        totals_2019, totals_2020, totals_2021], axis=0)
    totals = totals.drop(["state", "school"], axis=1).reset_index(drop=True)
    totals["applicants"] = [45266, 48014, 49480, 52550, 53042, 51680, 52777, 53371, 53030, 62443]
    totals["applications"] = [636309, 690281, 731595, 781602, 830016, 816153, 849678, 896819, 906588, 1099486]
    totals["matriculants"] = [19517, 20055, 20343, 20631, 21030, 21338, 21622, 21869, 22239, 22666]
    totals["applications per applicant"] = totals["applications"] / totals["applicants"]
    totals["matriculant applicant percent"] = (totals["matriculants"] / totals["applicants"]) * 100

    # Rearranging columns for readability
    totals = totals[["cycle_year", "applicants", "applications", "in state applicants", "out of state applicants",
                     "women applicants", "men applicants", "matriculants", "in state matriculants",
                     "out of state matriculants", "women matriculants", "men matriculants",
                     "applications per applicant", "matriculant applicant percent"]]

    # Concatenating the A1 school data for each year
    a1 = pd.concat([a1_2012, a1_2013, a1_2014, a1_2015, a1_2016, a1_2017, a1_2018, a1_2019, a1_2020, a1_2021], axis=0)
    a1 = a1.reset_index(drop=True)

    # Getting rid of numbers in the school names and replacing redundant names for med schools that changed their names over time
    schools = []
    for school in a1["school"]:
        new_school = ''.join([i for i in school if not i.isdigit()])
        schools.append(new_school)
    a1["school"] = schools
    a1["school"] = a1["school"].replace(
        {"Alabama-Heersink": "Alabama",
         "Kaiser Permanente-Tyson": "Kaiser Permanente",
         "Central Florida": "UCF",
         "GRU MC Georgia": "MC Georgia Augusta",
         "MC Georgia": "MC Georgia Augusta",
         "Chicago Med-Franklin": "Chicago Med Franklin",
         "Massachusetts-Chan": "Massachusetts",
         "Mayo-Alix": "Mayo",
         "St Louis": "Saint Louis",
         "UMDNJ New Jersey": "Rutgers New Jersey",
         "UMDNJ-RW Johnson": "Rutgers-RW Johnson",
         "SHU-Hackensack Meridian": "Hackensack Meridian",
         "Nevada": "Nevada Reno",
         "Columbia": "Columbia-Vagelos",
         "Yeshiva Einstein": "Einstein",
         "Hofstra North Shore-LIJ": "Zucker Hofstra Northwell",
         "Hofstra Northwell": "Zucker Hofstra Northwell",
         "Stony Brook": "Renaissance Stony Brook",
         "Mount Sinai": "Mount Sinai-Icahn",
         "New York University": "NYU-Grossman",
         "Buffalo": "Buffalo-Jacobs",
         "Case Western": "Case Western Reserve",
         "Jefferson": "Jefferson-Kimmel",
         "Commonwealth": "Geisinger Commonwealth",
         "Temple": "Temple-Katz",
         "South Carolina": "South Carolina Columbia",
         "UT HSC San Antonio": "UT San Antonio-Long",
         "UT Houston": "UT Houston-McGovern",
         "Vermont": "Vermont-Larner"}
    )

    # Rearranging columns for readability
    a1 = a1[["cycle_year", "state", "school", "applications", "in state applicants", "out of state applicants",
             "women applicants", "men applicants", "matriculants", "in state matriculants", "out of state matriculants",
             "women matriculants", "men matriculants"]]

    # Returning a merged df with each year for all schools and a totals df
    return a1, totals



def b8_merger(b8_filepwath):
    """
    Function to parse a folder of AAMC B-8 tables.
    Provide the filepath to the folder containing all AAMC B-8 tables.
    Returns a merged df of table B8 containing all schools merged according to year and a merged totals df.
    """
    # AAMC B-8 tables file paths for all excel files
    file_list_b8 = glob.glob(b8_filepwath)

    # Column names for every excel file
    colnames1 = ["state", "school", "applications", "in state applicants", "out of state applicants",
                 "women applicants", "men applicants", "matriculants", "in state matriculants",
                 "out of state matriculants", "women matriculants", "men matriculants"]
    colnames2 = ["state", "school", "applications", "in state applicants", "out of state applicants", "men applicants",
                 "women applicants", "matriculants", "in state matriculants", "out of state matriculants",
                 "men matriculants", "women matriculants"]  # column names men/women change in 2018

    # Processing all AAMC B-8 Tables
    b8_2012, total_b_2012 = cycle_generator(df_path=file_list_b8[0], head=10, foot=148, colnames=colnames1, year=2012)
    b8_2013, total_b_2013 = cycle_generator(df_path=file_list_b8[1], head=10, foot=152, colnames=colnames1, year=2013)
    b8_2014, total_b_2014 = cycle_generator(df_path=file_list_b8[2], head=10, foot=152, colnames=colnames1, year=2014)
    b8_2015, total_b_2015 = cycle_generator(df_path=file_list_b8[3], head=9, foot=152, colnames=colnames1, year=2015)
    b8_2016, total_b_2016 = cycle_generator(df_path=file_list_b8[4], head=9, foot=155, colnames=colnames1, year=2016)
    b8_2017, total_b_2017 = cycle_generator(df_path=file_list_b8[5], head=9, foot=157, colnames=colnames1, year=2017)
    b8_2018, total_b_2018 = cycle_generator(df_path=file_list_b8[6], head=9, foot=161, colnames=colnames2, year=2018)
    b8_2019, total_b_2019 = cycle_generator(df_path=file_list_b8[7], head=9, foot=163, colnames=colnames2, year=2019)
    b8_2020, total_b_2020 = cycle_generator(df_path=file_list_b8[8], head=9, foot=165, colnames=colnames2, year=2020)
    b8_2021, total_b_2021 = cycle_generator(df_path=file_list_b8[9], head=9, foot=165, colnames=colnames2, year=2021)

    # Concatenating the totals per year
    total_b = pd.concat([total_b_2012, total_b_2013, total_b_2014, total_b_2015, total_b_2016, total_b_2017,
                         total_b_2018, total_b_2019, total_b_2020, total_b_2021], axis=0)
    total_b = total_b.drop(["state", "school"], axis=1).reset_index(drop=True)
    total_b["applicants"] = [1853, 1937, 1891, 1887, 1936, 1858, 1855, 1813, 1855, 2091]
    total_b["applications per applicant"] = total_b["applications"] / total_b["applicants"]
    total_b["matriculant applicant percent"] = (total_b["matriculants"] / total_b["applicants"]) * 100

    # Rearranging columns for readability
    total_b = total_b[["cycle_year", "applicants", "applications", "in state applicants", "out of state applicants",
                       "women applicants", "men applicants", "matriculants", "in state matriculants",
                       "out of state matriculants", "women matriculants", "men matriculants",
                       "applications per applicant", "matriculant applicant percent"]]

    # Concatenating the B8 school data for each year
    b8 = pd.concat([b8_2012, b8_2013, b8_2014, b8_2015, b8_2016, b8_2017, b8_2018, b8_2019, b8_2020, b8_2021], axis=0)
    b8 = b8.reset_index(drop=True)

    # Getting rid of numbers in the school names and replacing redundant names for med schools that changed their names over time
    schools = []
    for school in b8["school"]:
        new_school = ''.join([i for i in school if not i.isdigit()])
        schools.append(new_school)
    b8["school"] = schools
    b8["school"] = b8["school"].replace(
        {"Alabama-Heersink": "Alabama",
         "Kaiser Permanente-Tyson": "Kaiser Permanente",
         "Central Florida": "UCF",
         "GRU MC Georgia": "MC Georgia Augusta",
         "MC Georgia": "MC Georgia Augusta",
         "Chicago Med-Franklin": "Chicago Med Franklin",
         "Massachusetts-Chan": "Massachusetts",
         "Mayo-Alix": "Mayo",
         "St Louis": "Saint Louis",
         "UMDNJ New Jersey": "Rutgers New Jersey",
         "UMDNJ-RW Johnson": "Rutgers-RW Johnson",
         "SHU-Hackensack Meridian": "Hackensack Meridian",
         "Nevada": "Nevada Reno",
         "Columbia": "Columbia-Vagelos",
         "Yeshiva Einstein": "Einstein",
         "Hofstra North Shore-LIJ": "Zucker Hofstra Northwell",
         "Hofstra Northwell": "Zucker Hofstra Northwell",
         "Stony Brook": "Renaissance Stony Brook",
         "Mount Sinai": "Mount Sinai-Icahn",
         "New York University": "NYU-Grossman",
         "Buffalo": "Buffalo-Jacobs",
         "Case Western": "Case Western Reserve",
         "Jefferson": "Jefferson-Kimmel",
         "Commonwealth": "Geisinger Commonwealth",
         "Temple": "Temple-Katz",
         "South Carolina": "South Carolina Columbia",
         "UT HSC San Antonio": "UT San Antonio-Long",
         "UT Houston": "UT Houston-McGovern",
         "Vermont": "Vermont-Larner"}
    )

    # Rearranging columns for readability
    b8 = b8[["cycle_year", "state", "school", "applications", "in state applicants", "out of state applicants",
             "women applicants", "men applicants", "matriculants", "in state matriculants", "out of state matriculants",
             "women matriculants", "men matriculants"]]

    # Returning a merged df with each year for all schools and a totals df
    return b8, total_b



# Setting the main filepath and running the functions to generate dfs.  Then exporting to csv.
if __name__ == "__main__":
    main_dir = "C:/Users/TooFastDan/Documents/MD_PhD Application/Nonprofit"

    # A1 (MD Schools)
    a1, totals_a = a1_merger(a1_filepath=main_dir+"/AAMC Data/A-1/*.xlsx")
    a1.to_csv(main_dir+"/AAMC Data/merged files/AAMC A-1 Merged.csv", index=False)
    totals_a.to_csv(main_dir+"/AAMC Data/merged files/AAMC A-1 Totals Merged.csv", index=False)

    # B8 (MD/PhD Schools)
    b8, totals_b = b8_merger(b8_filepwath=main_dir+"/AAMC Data/B-8/*.xlsx")
    b8.to_csv(main_dir+"/AAMC Data/merged files/AAMC B-8 Merged.csv", index=False)
    totals_b.to_csv(main_dir+"/AAMC Data/merged files/AAMC B-8 Totals Merged.csv", index=False)