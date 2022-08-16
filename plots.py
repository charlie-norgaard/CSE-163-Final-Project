"""
Irti Haq and Charlie Norgaard
CSE 163 Final Project
This file contains functions for generating plots using
the dataframes created in data_processing.py.
"""

import geopandas as gpd
import plotly.express as px


def time_plot(df, var_x, var_y):
    """
    This Function takes in a Dataframe and a Variable for X and for Y
    This function creates interactive scatter plot using the given dataframe
    and variables. The plot includes a slider to adjust the year.
    It then returns a plotly figure
    """
    fig = px.scatter(df, x=var_x, y=var_y, trendline="ols",
                     animation_frame="Year",
                     animation_group='Country',
                     hover_name='Country')
    return fig


def all_country_plot(df, var_x, var_y):
    """
    This Function takes in a Dataframe and a Variable for X and for Y and then
    This function creates a interactive scatter plot using the given dataframe
    and variables. The countries in this plot are color coordinated.
    It then returns a plotly figure
    """
    fig = px.scatter(df, x=var_x, y=var_y,
                     trendline="ols", animation_frame="Year",
                     animation_group='Country', hover_name='Country',
                     color='Country')
    return fig


def select_country_plot(df, var_x, var_y):
    """
    This Function takes in a Dataframe and a Variable for X and for Y and then
    This function creates interactive scatter plot using the given dataframe
    and variables.
    The countries in this plot are color coordinated and can be included/
    removed from the plot at the users discretion.
    It then returns a plotly figure
    """
    fig = px.scatter(df, x=var_x, y=var_y,
                     trendline="ols", hover_name='Year', color='Country')
    return fig


def corr_plot(df):
    """
    This Function takes in a Dataframe with R^2 values and then
    This function creates a plot depicting the correlation between variables
    according the the calculated R^2 value by country.
    It then returns a plotly figure
    """
    fig = px.bar(df, x="Country", y="R Square", color='Correlation',
                 hover_name='Country')
    return fig


def map_dataset(df, var_size, var_color, countries_shp):
    """
    Takes in a Dataframe, a variable to be encode to size of the points on the
    plot, a variable to encoded to the color of the points on the plot, and a
    shape file with the shapes of the countries and then in
    This function creates a geopandas dataframe plot using the given dataframe
    and shape file.
    The size of the points are dictated by the given variables var_size and
    color by var_color. It then returns and tupple with the a new geodataframe,
    a mask labeling positive and negetive var_size values, var_size, and
    var_color
    """
    net_df_geo = df.merge(countries_shp,
                          left_on='iso3',
                          right_on='iso3',
                          how='left')

    net_df_geo = gpd.GeoDataFrame(net_df_geo, geometry='geometry')

    net_df_geo['geometry'] = net_df_geo['geometry'].representative_point()

    mask = net_df_geo[var_size] < 0
    net_df_geo[var_size] = abs(net_df_geo[var_size])

    net_df_geo['lon'] = net_df_geo['geometry'].x
    net_df_geo['lat'] = net_df_geo['geometry'].y

    return (net_df_geo, mask, var_size, var_color)


def plot_map(df, var_color, var_size):
    """
    This function takes in a dataframe, a variable to be encode to size of the
    points on the plot, a variable to encoded to the color of the points
    on the plot. It then creates an interactive map plot using the
    dataframe generated from map_dataset and returns a plotly figure
    """
    px.set_mapbox_access_token("pk.eyJ1IjoiaXJ0aSIsImEiOiJjbDN0aGd0dGkwOWQ4M2JxcHd5eThjMzNxIn0.pOpdYEBWEtOuCB5WrwkjiA")
    map = px.scatter_mapbox(df,
                            lat="lat",
                            lon="lon",
                            color=var_color,
                            size=var_size,
                            color_continuous_scale=px.colors.sequential.Plasma,
                            zoom=1,
                            mapbox_style='satellite-streets',
                            custom_data=[var_color, var_size, 'Country'])

    return map


# should be in main method of test file
def plot_decr_map(df_mask):
    """
    This funtion takes in a tupple with a geodataframe, a mask, var_color,
    var_size and it then filters the df based on the mask and returns
    a tuple with the filtered dataframe, var_color, and var_size
    """
    map_df, mask, var_size, var_color = df_mask

    map_df = map_df.loc[mask, ['Country', var_color, var_size, 'lon', 'lat']]
    return plot_map(map_df, var_color, var_size)


def plot_no_decr_map(df_mask):
    """
    This funtion takes in a tupple with a geodataframe, a mask, var_color,
    var_size and it then filters the df based vals not on the mask and returns
    a tuple with the filtered dataframe, var_color, and var_size
    """
    map_df, mask, var_size, var_color = df_mask

    map_df = map_df.loc[~mask, ['Country', var_color, var_size, 'lon', 'lat']]
    return plot_map(map_df, var_color, var_size)
