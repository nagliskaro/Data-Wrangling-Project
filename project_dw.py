import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


# RQ: What is the impact of these polluants (N02, O3, PM 2.5) on prematures deaths in Sassari (sardegna, Italya) and Milan (Lombardy, Italy)? And how do they compare ?
# (sub questions) What is the impact of other particles like N02 and O3 compared to PM 2.5 ? What is the trend over the years?


def read_process_data(data_dir):
    # reading and cleaning PM 2.5 CSV
    dir_pm25 = "PM2.5-impact_premature_deaths.csv"
    data_pm25 = pd.read_csv(data_dir+dir_pm25)
    data_pm25 = data_pm25.drop(columns=["City Boundary Specification (LAU/grid)", 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])

    # reading and cleaning O3 CSV
    dir_O3 = "O3-impact_premature_deaths.csv"
    data_O3 = pd.read_csv(data_dir+dir_O3)
    data_O3 = data_O3.drop(columns=["City Boundary Specification (LAU/grid)", 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])

    # reading and cleaning N02 CSV
    dir_N02 = "N02-impact_premature_deaths.csv"
    data_N02 = pd.read_csv(data_dir+dir_N02)
    data_N02 = data_N02.drop(columns=["City Boundary Specification (LAU/grid)", 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])
    
    # combining the different polluants in a df
    polluants_df = pd.concat([data_pm25, data_O3, data_N02], ignore_index=True)
    polluants_df = polluants_df.sort_values(["Year", "Air Pollutant", "Country Or Territory"])
    polluants_df.to_csv("cleaned_data/combines_polluants.csv", encoding='utf-8', index=False)
    
    # read in Milan data
    dir_milan = "milan.csv"
    df_milan = pd.read_csv(data_dir+dir_milan)
    df_milan = df_milan.drop(columns=["City Boundary Specification (LAU/grid)", 'Country Or Territory', 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])
    df_milan.to_csv("cleaned_data/milan.csv", encoding='utf-8', index=False)

    # read in Sassari data
    dir_sassar = "sassari.csv"
    df_sassari = pd.read_csv(data_dir+dir_sassar)
    df_sassari = df_sassari.drop(columns=["City Boundary Specification (LAU/grid)", 'Country Or Territory', 'City', 'City Code', 'Health Risk Scenario', 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])
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
    
    dir_italy = "Italy_deaths_pm25.csv"
    data_italy = pd.read_csv(data_dir+dir_italy)
    data_italy_filt = data_italy.drop(['Country Or Territory', 'Degree Of Urbanisation',
           'Air Pollutant', 'Health Risk Scenario', 'Population',
           'Populated Area [km2]', 'Air Pollution Average [ug/m3]',
           'Air Pollution Population Weighted Average [ug/m3]',
           'Premature Deaths - lower CI', 'Premature Deaths - upper CI',
           'Years Of Life Lost', 'Years Of Life Lost - lower CI',
           'Years Of Life Lost - upper CI'], axis=1)
    data_italy_filt.to_csv("cleaned_data/italy_deaths_pm25.csv", encoding='utf-8', index=False)
    
    
    # cleaning european main cities data sets
    dir_list = ["milan", "berlin", "paris", "warsaw", "amsterdam", "dublin", "ljubljana", "stockholm", "zagreb", "helsinki"]
    
    for i in dir_list:
        df_city = pd.read_csv(data_dir+"europe_cities_pm25/"+i+".csv")
        df_city = df_city.drop(columns=["City Boundary Specification (LAU/grid)", 'Country Or Territory', 'City Code', 'Health Risk Scenario', "Air Pollution Average [ug/m3]", 'Premature Deaths - lower CI', 'Premature Deaths - upper CI', 'Years Of Life Lost', 'Years Of Life Lost - lower CI', 'Years Of Life Lost - upper CI'])
        df_city.to_csv("cleaned_data/europe_cities_pm25/"+i+".csv", encoding='utf-8', index=False)

    # merging european cities csv's
    dir_list = ["milan", "berlin", "paris", "warsaw", "amsterdam", "dublin", "ljubljana", "stockholm", "zagreb", "helsinki"]
    all_cities_df = []
    for city in dir_list:
        df_city = pd.read_csv("cleaned_data/europe_cities_pm25/"+city+".csv")
        df_city['City'] = city 
        all_cities_df.append(df_city)
        
    merged_df = pd.concat(all_cities_df, ignore_index=True)
    merged_df.to_csv("cleaned_data/merged_european_cities_data.csv", index=False)
        


def analyze_data():
    df_polution = pd.read_csv("cleaned_data/combines_polluants.csv").dropna()
    df_milan = pd.read_csv("cleaned_data/milan.csv").dropna()
    df_sassari = pd.read_csv("cleaned_data/sassari.csv").dropna()
    
    sassari_group_mean = df_sassari.groupby("Air Pollutant").mean()
    #print(sassari_group_mean)
    
    milan_group_mean = df_milan.groupby("Air Pollutant").mean()
    #print(milan_group_mean)
    
    sassari_group_polluant_year = df_sassari.groupby(["Air Pollutant", 'Year'])[["Air Pollution Population Weighted Average [ug/m3]", "Premature Deaths"]].mean()
    #print(sassari_group_polluant_year)

    # plotting Sassari Air Pollutants and Number of Premature Deaths
    pollutants = df_sassari['Air Pollutant'].unique()
    n_pollutants = len(pollutants)
    
    #milan
    milan_group_polluant_year = df_milan.groupby(["Air Pollutant", 'Year'])[["Air Pollution Population Weighted Average [ug/m3]", "Premature Deaths"]].mean()
    pollutants_milan = df_milan['Air Pollutant'].unique()
    n_pollutants_milan = len(pollutants_milan)
    

    #Sum of premature deaths: Milan, Sassari, Italy


    # Milan
    
    pm25_deaths_italy = pd.read_csv("cleaned_data/italy_deaths_pm25.csv")
    pm25_italy_done = pm25_deaths_italy.groupby('Year')["Premature Deaths"].sum()
    
    pm25_deaths_milan = df_milan[df_milan['Air Pollutant'] == 'PM2.5'].groupby('Year')['Premature Deaths'].sum()
    
    pm25_deaths_sassari = df_sassari[df_sassari['Air Pollutant'] == 'PM2.5'].groupby('Year')['Premature Deaths'].sum()
    #print(pm25_deaths_sassari)
    
    
    
    plt.figure(figsize=(10, 6))
    plt.plot(pm25_deaths_milan.index, pm25_deaths_milan, color='red', zorder=5)
    plt.fill_between(pm25_deaths_milan.index, pm25_deaths_milan, color="red", zorder=5)
    
    plt.plot(pm25_deaths_sassari.index, pm25_deaths_sassari, color="green")
    plt.fill_between(pm25_deaths_sassari.index, pm25_deaths_sassari, color="green", zorder=3)
    
    plt.plot(pm25_italy_done.index, pm25_italy_done, color="blue")
    plt.fill_between(pm25_italy_done.index, pm25_italy_done, color="blue")
    
    plt.title('Progression of Premature Deaths Due to PM2.5 Over the Years in Milan and Italy')
    plt.xlabel('Year')
    plt.ylabel('Sum of Premature Deaths')
    plt.grid(True)  # Add grid for better readability
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    
    plt.show()
    
    plt.figure(figsize=(12, 4 * n_pollutants))
    for i, pollutant in enumerate(pollutants, 1):
        plt.subplot(n_pollutants_milan, 1, i)
        subset_milan = milan_group_polluant_year.loc[pollutant]
        #print(subset_milan)

        plt.plot(subset_milan.index, subset_milan['Air Pollution Population Weighted Average [ug/m3]'], label='Air Pollution')
        plt.plot(subset_milan.index, subset_milan['Premature Deaths'], label='Premature Deaths', linestyle='--')

        plt.title(f'Trends for {pollutant} Milan')
        plt.xlabel('Year')
        plt.ylabel('Values')
        plt.legend()
        plt.tight_layout()
    
    plt.figure(figsize=(12, 4 * n_pollutants))

    for i, pollutant in enumerate(pollutants, 1):
        plt.subplot(n_pollutants, 1, i)
        subset = sassari_group_polluant_year.loc[pollutant]
        #print(subset)

        plt.plot(subset.index, subset['Air Pollution Population Weighted Average [ug/m3]'], label='Air Pollution')
        plt.plot(subset.index, subset['Premature Deaths'], label='Premature Deaths', linestyle='--')
        
        # added a correlation coefficient
        correlation_coefficient = subset['Air Pollution Population Weighted Average [ug/m3]'].corr(subset['Premature Deaths'])
        plt.text(0.5, 0.9, f'Correlation: {correlation_coefficient:.2f}', transform=plt.gca().transAxes, fontsize=12, ha='center')

        plt.title(f'Trends for {pollutant} Sassari')
        plt.xlabel('Year')
        plt.ylabel('Values')
        plt.legend()
        plt.tight_layout()        
        
    # linear regression for all pollutants:
        
    plt.figure(figsize=(12, 4 * n_pollutants))
    
    for i, pollutant in enumerate(pollutants, 1):
        plt.subplot(len(pollutants), 1, i)
        
        pollutant_data_sassari = df_sassari[df_sassari['Air Pollutant'] == pollutant][['Year', 'Air Pollution Population Weighted Average [ug/m3]', 'Premature Deaths']]
        X = pollutant_data_sassari[['Air Pollution Population Weighted Average [ug/m3]']]
        y = pollutant_data_sassari['Premature Deaths']
        
        model = LinearRegression()
        model.fit(X, y)
        
        predictions = model.predict(X)
        
        plt.scatter(X, y, label='Actual Data', color='blue')
        plt.plot(X, predictions, label='Linear Regression', color='red')
        plt.title(f'Linear Regression: {pollutant} vs. Premature Deaths in Sassari')
        plt.xlabel(f'{pollutant} Air Pollution Average [ug/m3]')
        plt.ylabel('Premature Deaths')
        plt.legend()
        plt.tight_layout()
    plt.show()

    # Plotting Milan info: Air Pollutants and Premature Deaths
    


    
    # plotting main european cities
    
    
    # Plotting Milan info: Air Pollutants and Premature Deaths
    

def main():
    data_dir = "data_sets/"
    read_process_data(data_dir)
    analyze_data()


if __name__ == "__main__":
    main()
    
    