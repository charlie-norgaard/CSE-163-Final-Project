"""
Irti Haq and Charlie Norgaard
CSE 163 Final Project
This file contains basic tests to check the validity of our calculations
and plots from data_processing.py and plots.py.
"""

import geopandas as gpd
import wbgapi as wb
import data_processing as process
import plots as plot
import cse163_utils as utils


def test_correlation(gdp_forest, gdp_elect, elect_forest):
    """
    This function checks the calculated R^2 values for the
    selected countries.
    """

    # COUNTRY MASKS
    afg_mask = gdp_forest['Country'] == 'Afghanistan'
    yemen_mask = gdp_forest['Country'] == 'Yemen, Rep.'
    somalia_mask = gdp_forest['Country'] == 'Somalia'
    sudan_mask = gdp_forest['Country'] == 'Sudan'

    # ASSERT EQUALS FOR GDP_FOREST DATAFRAME
    utils.assert_equals(0.0, gdp_forest[afg_mask]['R Square'])
    utils.assert_equals(0.0, gdp_forest[yemen_mask]['R Square'])
    utils.assert_equals(0.974293, gdp_forest[somalia_mask]['R Square'])
    utils.assert_equals(0.392113, gdp_forest[sudan_mask]['R Square'])

    # ASSERT EQUALS FOR GDP_FOREST DATAFRAME
    utils.assert_equals(0.903613, gdp_elect[afg_mask]['R Square'])
    utils.assert_equals(0.003374, gdp_elect[yemen_mask]['R Square'])
    utils.assert_equals(0.390884, gdp_elect[somalia_mask]['R Square'])
    utils.assert_equals(0.057297, gdp_elect[sudan_mask]['R Square'])

    # ASSERT EQUALS FOR GDP_FOREST DATAFRAME
    utils.assert_equals(0.000000, elect_forest[afg_mask]['R Square'])
    utils.assert_equals(0.000000, elect_forest[yemen_mask]['R Square'])
    utils.assert_equals(0.826237, elect_forest[somalia_mask]['R Square'])
    utils.assert_equals(0.050978, elect_forest[sudan_mask]['R Square'])


def test_net_change(gdp_forest, gdp_elect, elect_forest):
    """
    This function checks the calculated net change values for the
    selected countries.
    """

    # COUNTRY MASKS
    afg_mask = gdp_forest['Country'] == 'Afghanistan'
    yemen_mask = gdp_forest['Country'] == 'Yemen, Rep.'
    somalia_mask = gdp_forest['Country'] == 'Somalia'
    sudan_mask = gdp_forest['Country'] == 'Sudan'

    # ASSERT EQUALS FOR GDP_FOREST DATAFRAME
    utils.assert_equals(0.000000, gdp_forest[afg_mask]['Forest Coverage'])
    utils.assert_equals(0.000000, gdp_forest[yemen_mask]['Forest Coverage'])
    utils.assert_equals(-5.958388, gdp_forest[somalia_mask]['Forest Coverage'])
    utils.assert_equals(23.829260, gdp_forest[sudan_mask]['Forest Coverage'])

    # ASSERT EQUALS FOR GDP_FOREST DATAFRAME
    utils.assert_equals(562.889406, gdp_elect[afg_mask]['Elect. Access'])
    utils.assert_equals(26.048910, gdp_elect[yemen_mask]['Elect. Access'])
    utils.assert_equals(-4.081667, gdp_elect[somalia_mask]['Elect. Access'])
    utils.assert_equals(134.619738, gdp_elect[sudan_mask]['Elect. Access'])

    # ASSERT EQUALS FOR GDP_FOREST DATAFRAME
    utils.assert_equals(0.000000, elect_forest[afg_mask]['Forest Coverage'])
    utils.assert_equals(0.000000, elect_forest[yemen_mask]['Forest Coverage'])
    utils.assert_equals(-18.572917,
                        elect_forest[somalia_mask]['Forest Coverage'])
    utils.assert_equals(23.829260, elect_forest[sudan_mask]['Forest Coverage'])


def test_time_plots(gdp_forest, gdp_elect, elect_forest):
    """
    This function generates plots using a reduced dataframe to
    check the validity of our final plots.
    """

    # REDUCE DATASETS FOR SMALLER PLOT
    gdp_forest_test = gdp_forest.head(5)
    gdp_elect_test = gdp_elect.head(5)
    elect_forest_test = elect_forest.head(5)

    # SAVE TEST PLOTS
    gdp_forest_test_plt = plot.time_plot(gdp_forest_test,
                                         'GDP', 'Forest Coverage')
    gdp_elect_test_plt = plot.time_plot(gdp_elect_test, 'GDP', 'Elect. Access')
    elect_forest_test_plt = plot.time_plot(elect_forest_test, 'Elect. Access',
                                           'Forest Coverage')

    test_plot_path = 'Test HTML'

    gdp_forest_test_plt.write_html(test_plot_path +
                                   "/gdp_forest_chng_corr_plot.html")
    gdp_elect_test_plt.write_html(test_plot_path +
                                  "/gdp_elect_chng_corr_plot.html")
    elect_forest_test_plt.write_html(test_plot_path +
                                     "/elect_forest_chng_corr_plot.html")


def main():

    # ----- DATA FRAMES FOR TESTS ------ #

    # Import data frames
    gdp_df = wb.data.DataFrame('NY.GDP.MKTP.KD', time=range(1999, 2020),
                               economy=wb.region.members('LDC'), labels=True)
    forest_df = wb.data.DataFrame('AG.LND.FRST.ZS', time=range(1999, 2020),
                                  economy=wb.region.members('LDC'),
                                  labels=True)
    elect_df = wb.data.DataFrame('EG.ELC.ACCS.ZS', time=range(1990, 2020),
                                 economy=wb.region.members('LDC'), labels=True)

    # Read Shapefile
    countries_shp = gpd.read_file('shape_files/world-administrative-boundaries.shp')
    countries_shp = countries_shp[['iso3', 'geometry']]

    # Reshape each data frame
    gdp_reshp = process.reshape_data(gdp_df, 'GDP')
    forest_reshp = process.reshape_data(forest_df, 'Forest Coverage')
    elect_reshp = process.reshape_data(elect_df, 'Elect. Access')

    # Merge data frames
    gdp_forest = process.merge_data(gdp_reshp, forest_reshp)
    gdp_elect = process.merge_data(gdp_reshp, elect_reshp)
    elect_forest = process.merge_data(elect_reshp, forest_reshp)

    # Get iso codes for each country
    iso_codes = process.get_iso_codes(gdp_df)

    # Calculate variable correlation for each country
    gdp_forest_corr = process.correlate(gdp_forest, 'GDP', 'Forest Coverage')
    gdp_elect_corr = process.correlate(gdp_elect, 'GDP', 'Elect. Access')
    elect_forest_corr = process.correlate(elect_forest,
                                          'Elect. Access',
                                          'Forest Coverage')

    # Calculate variable change correlation for each country
    gdp_forest_chng_corr = process.correlate(gdp_forest, 'GDP change',
                                             'Forest Coverage change')
    print(gdp_forest_chng_corr)
    gdp_elect_chng_corr = process.correlate(gdp_elect, 'GDP change',
                                            'Elect. Access change')
    print(gdp_elect_chng_corr)
    elect_forest_chng_corr = process.correlate(elect_forest,
                                               'Elect. Access change',
                                               'Forest Coverage change')
    print(elect_forest_chng_corr)

    # Calculate Net Change for Each Country
    gdp_forest_net_change = process.df_net_change(gdp_forest,
                                                  iso_codes, 'GDP',
                                                  'Forest Coverage')
    gdp_elect_net_change = process.df_net_change(gdp_elect, iso_codes,
                                                 'GDP', 'Elect. Access')
    elect_forest_net_change = process.df_net_change(elect_forest, iso_codes,
                                                    'Elect. Access',
                                                    'Forest Coverage')

    # ----- UNIT TESTS -----#

    test_correlation(gdp_forest_corr, gdp_elect_corr, elect_forest_corr)
    test_net_change(gdp_forest_net_change, gdp_elect_net_change,
                    elect_forest_net_change)
    test_time_plots(gdp_forest, gdp_elect, elect_forest)


if __name__ == "__main__":
    main()
