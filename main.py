'''
Irti Haq and Charlie Norgaard
CSE 163 Final Project
This file is used to run all of the functions from data_processing.py
and plots.py and saves all generated plots to a file path
'''

import geopandas as gpd
import wbgapi as wb
import data_processing as process
import plots as plot


def main():

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

    # Calculate correlation for each country
    gdp_forest_corr = process.correlate(gdp_forest, 'GDP', 'Forest Coverage')
    gdp_elect_corr = process.correlate(gdp_elect, 'GDP', 'Elect. Access')
    elect_forest_corr = process.correlate(elect_forest, 'Elect. Access change',
                                          'Forest Coverage change')

    gdp_forest_chng_corr = process.correlate(gdp_forest, 'GDP change',
                                             'Forest Coverage change')
    gdp_elect_chng_corr = process.correlate(gdp_elect, 'GDP change',
                                            'Elect. Access change')

    # Calculate Net Change for Each Country
    gdp_forest_net_change = process.df_net_change(gdp_forest, iso_codes, 'GDP',
                                                  'Forest Coverage')
    gdp_elect_net_change = process.df_net_change(gdp_elect, iso_codes, 'GDP',
                                                 'Elect. Access')
    elect_forest_net_change = process.df_net_change(elect_forest, iso_codes,
                                                    'Elect. Access',
                                                    'Forest Coverage')

    # ----- PLOTTING ------ #

    # File Path for storing plolty plots
    file_path = 'Plots HTML'

    # Create plotly time plots for each merged data frame
    gdp_forest_time_plt = plot.time_plot(gdp_forest, 'GDP change',
                                         'Forest Coverage change')
    gdp_forest_time_plt.update_layout(
        title='Plot Showing GDP Growth Rate vs Percent Change in'
        ' Forest Coverage for All LEDCs over time')

    gdp_elect_time_plt = plot.time_plot(gdp_elect, 'GDP change',
                                        'Elect. Access change')
    gdp_elect_time_plt.update_layout(
        title='Plot Showing GDP Growth Rate vs Percent Change in'
        ' Electricity Access for All LEDCs over time')

    elect_forest_time_plt = plot.time_plot(elect_forest,
                                           'Elect. Access change',
                                           'Forest Coverage change')
    elect_forest_time_plt.update_layout(
        title='Plot Showing Percent Change in Electricity Access for All LEDCs'
        ' over time vs Percent Change in Forest Coverage for All LEDCs'
        ' over time')

    gdp_forest_time_plt.write_html(file_path + '/gdp_forest_time_plt.html')
    gdp_elect_time_plt.write_html(file_path + '/gdp_elect_time_plt.html')
    elect_forest_time_plt.write_html(file_path + '/elect_forest_time_plt.html')

    # Create plotly plots for all countries
    gdp_forest_all_plt = plot.all_country_plot(gdp_forest, 'GDP',
                                               'Forest Coverage')
    gdp_forest_all_plt.update_layout(
        title='Plot Showing GDP vs Forest Coverage'
        ' for All LEDCs over time')

    gdp_elect_all_plt = plot.all_country_plot(gdp_elect, 'GDP',
                                              'Elect. Access')
    gdp_elect_all_plt.update_layout(
        title='Plot Showing GDP vs Elect. Access for'
        ' All LEDCs over time')

    gdp_forest_all_plt.write_html(file_path + '/gdp_forest_all_plt.html')
    gdp_elect_all_plt.write_html(file_path + '/gdp_elect_all_plt.html')

    # Create plotly plots for selecting countries
    gdp_frst_chng_slct_plt = plot.select_country_plot(gdp_forest,
                                                      'GDP change',
                                                      'Forest Coverage change')
    gdp_frst_chng_slct_plt.update_layout(title=('Plot Showing GDP Growth Rate'
                                                ' vs Percent Change in Forest'
                                                ' Coverage'))

    gdp_forest_select_plt = plot.select_country_plot(gdp_forest,
                                                     'GDP',
                                                     'Forest Coverage')
    gdp_forest_select_plt.update_layout(title=('Plot Showing GDP vs '
                                               'Forest Coverage'))

    gdp_elct_chng_slct_plt = plot.select_country_plot(gdp_elect,
                                                      'GDP change',
                                                      'Elect. Access change')
    gdp_elct_chng_slct_plt.update_layout(title=('Plot Showing GDP Growth vs '
                                                'Percent Change in Electricity'
                                                ' Access'))

    gdp_elect_select_plt = plot.select_country_plot(gdp_elect,
                                                    'GDP',
                                                    'Elect. Access')
    gdp_elect_select_plt.update_layout(title=('Plot Showing GDP vs Percent'
                                              ' Electricity Access'))

    elct_frt_chng_slct_plt = plot.select_country_plot(elect_forest,
                                                      'Elect. Access change',
                                                      'Forest Coverage change')

    elct_frt_chng_slct_plt.update_layout(title=('Plot Showing Percent Change'
                                                ' in Forest Coverage vs'
                                                ' Percent Change Electricity'
                                                ' Access'))

    gdp_forest_select_plt.write_html(file_path + '/gdp_forest_select_plt.html')
    gdp_elect_select_plt.write_html(file_path + '/gdp_elect_select_plt.html')

    gdp_frst_chng_slct_plt.write_html(file_path +
                                      '/gdp_frst_chng_slct_plt.html')
    gdp_elct_chng_slct_plt.write_html(file_path +
                                      '/gdp_elct_chng_slct_plt.html')
    elct_frt_chng_slct_plt.write_html(file_path +
                                      '/elct_frt_chng_slct_plt.html')

    # Create plotly plots for correlation plots
    gdp_forest_corr_plot = plot.corr_plot(gdp_forest_corr)
    gdp_forest_corr_plot.update_layout(title=('Plot Showing The Coefficient of'
                                              ' Determination for GDP vs'
                                              ' Percent Change in Forest'
                                              ' Coverage By Country'))

    gdp_elect_corr_plot = plot.corr_plot(gdp_elect_corr)
    gdp_elect_corr_plot.update_layout(title=('Plot Showing The Coefficient of'
                                             ' Determination for GDP vs '
                                             'Percent Electricity Access By'
                                             ' Country'))

    elect_forest_corr_plot = plot.corr_plot(elect_forest_corr)
    elect_forest_corr_plot.update_layout(title=('Plot Showing The Coefficient'
                                                ' of Determination for Percent'
                                                ' Change in Forest Coverage vs'
                                                ' Percent Change Electricity'
                                                ' Access  By Country'))

    gdp_forest_corr_plot.write_html(file_path + '/gdp_forest_corr_plot.html')
    gdp_elect_corr_plot.write_html(file_path + '/gdp_elect_corr_plot.html')
    elect_forest_corr_plot.write_html(file_path +
                                      '/elect_forest_corr_plot.html')

    gdp_forest_chng_corr_plot = plot.corr_plot(gdp_forest_chng_corr)
    gdp_forest_chng_corr_plot.update_layout(title=('Plot Showing The '
                                                   'Coefficient of Determinati'
                                                   'on for GDP Growth Rate vs '
                                                   'Percent Change in Forest '
                                                   'Coverage By Country'))

    gdp_elect_chng_corr_plot = plot.corr_plot(gdp_elect_chng_corr)
    gdp_elect_chng_corr_plot.update_layout(title=('Plot Showing The Coeffici'
                                                  'ent of Determination for '
                                                  'GDP Growth Rate vs Percent'
                                                  ' Change in Electricity Acc'
                                                  'esse By Country'))

    gdp_forest_chng_corr_plot.write_html(file_path +
                                         '/gdp_forest_chng_corr_plot.html')
    gdp_elect_chng_corr_plot.write_html(file_path +
                                        '/gdp_elect_chng_corr_plot.html')

    # Create map data set
    gpd_forest_map_df = plot.map_dataset(gdp_forest_net_change,
                                         'Forest Coverage', 'GDP',
                                         countries_shp)

    gpd_elect_map_df = plot.map_dataset(gdp_elect_net_change, 'Elect. Access',
                                        'GDP', countries_shp)

    elect_forest_map_df = plot.map_dataset(elect_forest_net_change,
                                           'Elect. Access', 'Forest Coverage',
                                           countries_shp)

    # Plot maps
    gdp_forest_dcr_map_plt = plot.plot_decr_map(gpd_forest_map_df)

    gdp_forest_dcr_map_plt.update_traces(
        hovertemplate='<br>'.join([
            '%{customdata[2]}',
            'Net Change In GDP: %{customdata[0]:.2f}%',
            'Net Change In Forest Coverage: %{customdata[1]:.2f}%',
        ]))

    gdp_forest_dcr_map_plt.update_layout(
        title='Maps Showing Net Change in GDP (%) vs Deforestation (%)'
        ' From 1999 - 2019 <br><sup>Size of Markers is Proportional to Rate'
        ' of Deforestation</sup>')

    gdp_forest_map_plt = plot.plot_no_decr_map(gpd_forest_map_df)

    gdp_forest_map_plt.update_traces(
        hovertemplate='<br>'.join([
            '%{customdata[2]}',
            'Net Change In GDP: %{customdata[0]:.2f}%',
            'Net Change In Forest Coverage: %{customdata[1]:.2f}%',
        ]))

    gdp_forest_map_plt.update_layout(
        title='Maps Showing Net Change in GDP (%) vs Forest Coverage (%)'
        ' From 1999 - 2019 <br><sup>Size of Markers is Proportional to Net'
        ' Change in Forest Coverage</sup>')

    gdp_forest_dcr_map_plt.write_html(file_path+'/gdp_forest_dcr_map_plt.html')
    gdp_forest_map_plt.write_html(file_path+'/gdp_forest_map_plt.html')

    gdp_elect_dcr_map_plt = plot.plot_decr_map(gpd_elect_map_df)
    gdp_elect_dcr_map_plt.update_traces(
        hovertemplate='<br>'.join([
            '%{customdata[2]}',
            'Net Change In GDP: %{customdata[0]:.2f}%',
            'Net Change In Electricity Access: %{customdata[1]:.2f}%',
        ]))

    gdp_elect_dcr_map_plt.update_layout(
                                        title='Maps Showing Net Change in'
                                        ' GDP (%) vs Decrease in Electricity'
                                        ' Access (%) From 1999 - 2'
                                        '019 <br><sup>Size of Markers '
                                        'is Proportional to'
                                        ' Change in Electricity Access</sup>')

    gdp_elect_map_plt = plot.plot_no_decr_map(gpd_elect_map_df)
    gdp_elect_map_plt.update_traces(
                                    hovertemplate='<br>'.join([
                                        '%{customdata[2]}',
                                        'Net Change'
                                        ' In GDP: %{customdata[0]:.2f}%',
                                        'Net'
                                        ' Change In '
                                        'Electricity'
                                        ' Access: %{customdata[1]:.2f}%',
                                    ]))

    gdp_elect_map_plt.update_layout(
                                    title='Maps Showing Net Change in GDP (%)'
                                    ' vs Change in Electricity'
                                    ' Access (%) From 1999 - 2019 <br><sup>Si'
                                    'ze of Markers is Proportional'
                                    ' to Change in Electricity Access</sup>')

    gdp_elect_dcr_map_plt.write_html(file_path + '/gdp_elect_dcr_map_plt.html')
    gdp_elect_map_plt.write_html(file_path + '/gdp_elect_map_plt.html')

    elect_forest_map_plt = plot.plot_no_decr_map(elect_forest_map_df)
    elect_forest_map_plt.update_traces(
                                        hovertemplate='<br>'.join([
                                            '%{customdata[2]}',
                                            'Net Change In Forest'
                                            ' Coverage: %{customdata[0]:.2f}%',
                                            'Net Change In'
                                            ' Electricity'
                                            ' Access: %{customdata[1]:.2f}%',
                                        ]))

    elect_forest_map_plt.update_layout(
                                        title='Maps Showing Net Change in'
                                        ' Forest Coverage (%) vs CHange in'
                                        ' Electricity Access (%) From '
                                        '1999 - 2019 <br><sup>Size of '
                                        'Markers is'
                                        ' Proportional to Change in '
                                        'Electricity Access</sup>')

    elect_forest_map_plt.write_html(file_path + '/elect_forest_map_plt.html')


if __name__ == '__main__':
    main()
