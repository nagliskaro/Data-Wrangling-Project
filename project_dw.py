import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def read_process_data(data_dir):
    # reading and cleaning PM 2.5 CSV
    dir_pm25 = "PM2.5-impact_premature_deaths.csv"
    data_pm25 = pd.read_csv(data_dir+dir_pm25)
    data_pm25 = data_pm25.drop(columns=["City Boundary Specification (LAU/grid)", 'City', 'City Code', 'Health Risk Scenario'])
    print(data_pm25.head())

    # reading and cleaning O3 CSV
    dir_O3 = "O3-impact_premature_deaths.csv"
    data_O3 = pd.read_csv(data_dir+dir_O3)
    data_O3 = data_O3.drop(columns=["City Boundary Specification (LAU/grid)", 'City', 'City Code', 'Health Risk Scenario'])
    print(data_O3.head())

    # reading and cleaning N02 CSV
    dir_N02 = "N02-impact_premature_deaths.csv"
    data_N02 = pd.read_csv(data_dir+dir_N02)
    data_N02 = data_N02.drop(columns=["City Boundary Specification (LAU/grid)", 'City', 'City Code', 'Health Risk Scenario'])
    print(data_N02.head())
    
    # combining the different polluants in a df
    polluants_df = pd.concat([data_pm25, data_O3, data_N02], ignore_index=True)
    polluants_df = polluants_df.sort_values(["Year", "Air Pollutant", "Country Or Territory"])
    polluants_df.to_csv("combines_polluants.csv", encoding='utf-8', index=False)
    print(polluants_df.head())
    
    # Reading in CSV for total deaths attributed to air quality
    total_airqual_deaths = "total_deaths_attributed_to_air_quality.csv"
    
    df_airqual_deaths = pd.read_csv(data_dir+total_airqual_deaths)
    df_airqual_deaths = df_airqual_deaths.drop(['IndicatorCode', 'Indicator', 'ValueType', 'ParentLocationCode', 'ParentLocation', 'Location type', 
                'SpatialDimValueCode', 'IsLatestYear', 'Dim1 type', 'Dim1ValueCode', 'Dim2 type', 'Dim2', 'Dim2ValueCode',
                'Dim3 type', 'Dim3', 'Dim3ValueCode', 'DataSourceDimValueCode', 'DataSource', 'FactValueNumericPrefix',
                'FactValueUoM', 'FactValueNumericLowPrefix', 'FactValueNumericLow', 'FactValueNumericHighPrefix',
                'FactValueNumericHigh', 'FactValueTranslationID', 'FactComments', "DateModified", "Language", "Period type"], axis=1)
    df_airqual_deaths.to_csv("air_quality_attributed_deaths.csv", encoding='utf-8', index=False)



def analyze_data():
    pass


def main():
    # data_dir = "data_sets/"
    # read_process_data(data_dir)
    analyze_data()


if __name__ == "__main__":
    main()
