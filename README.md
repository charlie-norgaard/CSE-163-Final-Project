# CSE 163 Final Project
## Analyzing the Relationship Between National Forest Coverage, Population Access to Electricity, and GDP Growth Rate


### Project Overview

Motivation:
- Access to high quality reliable economic data tracking economic growth and development in developing nations remains a major challenge for policy makers and development agencies. Since access to electricity as a ratio of population and deforestation can act as a rough proxy for economic growth and development. Our plan is to show how we can use data of access to electricity and deforestation as a proxy to estimate economic growth and development in countries. Furthemore, by exploring trends pertaining to national urbanization and industrialization, we can better understand the factors that contribute to high or low national GDPs.

Our analysis was peformed by investigating the following three questions:
- How do trends in deforestation and access to electricity reflect changes in national GDP growth rates?
- How does the rate of deforestation relate to the change in national GDP?
- How does increased access to electricity affect the economic growth rate for countries?

In answering these questions, we used data from the World Bank public database. The datasets used are listed below:
- GDP (current US$) https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
- Forest area (% of land area) https://data.worldbank.org/indicator/AG.LND.FRST.ZS
- Access to Electricity (% of Population) https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS
- World Administratie Boundaries (Shape File) https://datacatalog.worldbank.org/search/dataset/0038272

Through our analysis, we chose to study less developed countries according to the UNs definition and only used data from 2000 - 2019.

### Environment Setup and Configuration

Recommended Python Version: >= 3.8.12

Additional Libaries used:
- pandas
- geopandas
- plotly express
- wbgapi

These libraries can be installed by running the following commands via Command Line (Windows) or terminal (MacOS):
- pip install pandas
- pip install geopandas 
- pip install plotly_express 
- pip install wbgapi 

### Running the Code

The project code is broken up into 3 separate modules: a data processing module (data_processing.py), a data visualization module (plots.py), and a main module for running the functions defined in the previous two code modules (main.py).

- data_processing.py imports the data frames from the world bank database, reshapes/cleans the data, and performs some basic stastics. 
- plots.py creates several plots to visualize our statistical analysis
- main.py includes all functions from data_processing.py and plots.py in the order of which they should be run. To view dataframes and plots from the various functions, just uncomment the print and write_html lines.
- testing.py contains all of the code to test functions. You can run the tests by just runing test.py  

Additional Notes:
- There is no need to manually download the world bank dataframes used in our analysis as we can pull directly from the World Bank database using the wbgapi library. This is performed in the first three lines of main.py.
- This program also saves plots as .html files.

