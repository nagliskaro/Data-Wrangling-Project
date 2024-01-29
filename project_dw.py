import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# RQ: What is the impact of these polluants (N02, O3, PM 2.5) on prematures deaths in Sassari (sardegna, Italya) and Milan (Lombardy, Italy)? And how do they compare ?
# (sub questions) What is the impact of other particles like N02 and O3 compared to PM 2.5 ? What is the trend over the years?



def read_process_data(data_dir):
    # reading and cleaning PM 2.5 CSV
    dir_pm25 = "PM2.5-impact_premature_deaths.csv"
    data_pm25 = pd.read_csv(data_dir+dir_pm25)
    data_pm25 = data_pm25.drop(columns=["City Boundary Specification (LAU/grid)", 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])
    # print(data_pm25.head())

    # reading and cleaning O3 CSV
    dir_O3 = "O3-impact_premature_deaths.csv"
    data_O3 = pd.read_csv(data_dir+dir_O3)
    data_O3 = data_O3.drop(columns=["City Boundary Specification (LAU/grid)", 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])
    # print(data_O3.head())

    # reading and cleaning N02 CSV
    dir_N02 = "N02-impact_premature_deaths.csv"
    data_N02 = pd.read_csv(data_dir+dir_N02)
    data_N02 = data_N02.drop(columns=["City Boundary Specification (LAU/grid)", 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])
    # print(data_N02.head())
    
    # combining the different polluants in a df
    polluants_df = pd.concat([data_pm25, data_O3, data_N02], ignore_index=True)
    polluants_df = polluants_df.sort_values(["Year", "Air Pollutant", "Country Or Territory"])
    polluants_df.to_csv("cleaned_data/combines_polluants.csv", encoding='utf-8', index=False)
    # print(polluants_df.head())
    
    # read in Milan data
    dir_milan = "milan.csv"
    df_milan = pd.read_csv(data_dir+dir_milan)
    df_milan = df_milan.drop(columns=["City Boundary Specification (LAU/grid)", 'Country Or Territory', 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])
    print(df_milan.head())
    df_milan.to_csv("cleaned_data/milan.csv", encoding='utf-8', index=False)

    # read in Sassari data
    dir_sassar = "sassari.csv"
    df_sassari = pd.read_csv(data_dir+dir_sassar)
    df_sassari = df_sassari.drop(columns=["City Boundary Specification (LAU/grid)", 'Country Or Territory', 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])
    print(df_sassari.head())
    df_sassari.to_csv("cleaned_data/sassari.csv", encoding='utf-8', index=False)
    
    # Reading in CSV for total deaths attributed to air quality
    total_airqual_deaths = "total_deaths_attributed_to_air_quality.csv"
    
    df_airqual_deaths = pd.read_csv(data_dir+total_airqual_deaths)
    df_airqual_deaths = df_airqual_deaths.drop(['IndicatorCode', 'Indicator', 'ValueType', 'ParentLocationCode', 'ParentLocation', 'Location type', 
                'SpatialDimValueCode', 'IsLatestYear', 'Dim1 type', 'Dim1ValueCode', 'Dim2 type', 'Dim2', 'Dim2ValueCode',
                'Dim3 type', 'Dim3', 'Dim3ValueCode', 'DataSourceDimValueCode', 'DataSource', 'FactValueNumericPrefix',
                'FactValueUoM', 'FactValueNumericLowPrefix', 'FactValueNumericLow', 'FactValueNumericHighPrefix',
                'FactValueNumericHigh', 'FactValueTranslationID', 'FactComments', "DateModified", "Language", "Period type"], axis=1)
    df_airqual_deaths.to_csv("cleaned_data/air_quality_attributed_deaths.csv", encoding='utf-8', index=False)


def analyze_data():
    df_polution = pd.read_csv("cleaned_data/combines_polluants.csv").dropna()
    df_milan = pd.read_csv("cleaned_data/milan.csv").dropna()
    df_sassari = pd.read_csv("cleaned_data/sassari.csv").dropna()
    
    sassari_group_mean = df_sassari.groupby("Air Pollutant").mean()
    print(sassari_group_mean)

    milan_group_mean = df_milan.groupby("Air Pollutant").mean()
    print(milan_group_mean)
    
    sassari_group_polluant_year = df_sassari.groupby(["Air Pollutant", 'Year'])[["Air Pollution Average [ug/m3]", "Premature Deaths"]].mean()
    print(sassari_group_polluant_year)

    # plotting
    pollutants = df_sassari['Air Pollutant'].unique()
    n_pollutants = len(pollutants)

    plt.figure(figsize=(12, 4 * n_pollutants))

    for i, pollutant in enumerate(pollutants, 1):
        plt.subplot(n_pollutants, 1, i)
        subset = sassari_group_polluant_year.loc[pollutant]

        plt.plot(subset.index, subset['Air Pollution Average [ug/m3]'], label='Air Pollution')
        plt.plot(subset.index, subset['Premature Deaths'], label='Premature Deaths', linestyle='--')

        plt.title(f'Trends for {pollutant}')
        plt.xlabel('Year')
        plt.ylabel('Values')
        plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    data_dir = "data_sets/"
    read_process_data(data_dir)
    
    analyze_data()


if __name__ == "__main__":
    main()
