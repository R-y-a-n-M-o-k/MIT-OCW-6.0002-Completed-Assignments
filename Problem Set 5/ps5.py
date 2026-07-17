# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    p_vals = []
    #for each model degree, fit model to data
    for deg in degs:
        p = pylab.polyfit(x, y, deg)
        p_vals.append(p)
    return p_vals


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mean = pylab.sum(y)/len(y)
    sum_residuals_squared = pylab.sum((y - estimated)**2)
    sum_dist_from_mean_squared = pylab.sum((y - mean)**2)
    
    #compute r-squared value
    return 1 - sum_residuals_squared/sum_dist_from_mean_squared

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for i in range(len(models)):
        #intialise and plot original data
        pylab.figure()
        pylab.plot(x, y, '.', markersize=3, color='blue')
        pylab.xlabel('Time (years)')
        pylab.ylabel(f'Temperature ($^o C$)')

        #get statistics of given model, plot estimate of model
        p_vals = models[i] #an array
        deg = len(p_vals)-1
        estimated = pylab.polyval(p_vals, x)
        r2 = r_squared(y, estimated)

        if deg == 1:
            se_div_m = se_over_slope(x, y, estimated, p_vals)
            pylab.title('Temperature against Time' + 
                        "\n" + 
                        f'Deg = {deg}, $r^2$={r2:.4f}, SE/m = {se_div_m:.4f})')
            pylab.plot(x, 
                       estimated, 
                       color='red')
        else:
            pylab.title('Temperature against Time' + 
                        "\n" + 
                        f'Deg = {deg}, $r^2$={r2:.4f}')
            pylab.plot(x, 
                       estimated, 
                       color='red')
        
        #pylab.legend()
        pylab.show()
    

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    #iterate get avg temp in a year for multiple cities
    years_temp_avg = []
    for year in years:
        year_length = len(climate.get_yearly_temp(multi_cities[0], year))

        #compute avg
        temp_sum = pylab.zeros(shape=year_length)
        for city in multi_cities:
            temp_sum += climate.get_yearly_temp(city, year)
        temp_avg = temp_sum/len(multi_cities) #avg temp each day array
        year_temp_avg = pylab.sum(temp_avg)/year_length #avg temp for the year, single value
        years_temp_avg.append(year_temp_avg)

    return years_temp_avg

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_avg = []
    #loop to compute moving avgs
    for i in range(len(y)):
        #first few only use prior values that do exist
        if i < window_length:
            avg = pylab.sum(y[0:i+1])/(i+1)
            moving_avg.append(avg)
        #sliding window for other averages
        else:
            avg = pylab.sum(y[i-window_length+1:i+1])/window_length
            moving_avg.append(avg)
    return pylab.array(moving_avg)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    num_values = len(y)
    residuals_squared_sum = pylab.sum((y - estimated)**2)
    rmse_value = pylab.sqrt(residuals_squared_sum/num_values)
    
    return rmse_value

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    #iterate to get stdev over each year
    stdev_years = []
    for year in years:
        year_length = len(climate.get_yearly_temp(multi_cities[0], year))

        #compute avg
        temp_sum = pylab.zeros(shape=year_length)
        for city in multi_cities:
            temp_sum += climate.get_yearly_temp(city, year)
        temp_avg = temp_sum/len(multi_cities) #avg temp each day array
        year_temp_avg = pylab.sum(temp_avg)/year_length #avg temp for the year, single value

        #compute stdev
        stdev = pylab.sqrt(pylab.sum((temp_avg - year_temp_avg)**2)/len(temp_avg))
        stdev_years.append(stdev)
    
    return stdev_years

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #for each model, plot test data and estimated
    for model in models:
        estimated = pylab.polyval(model, x)
        model_rmse = rmse(y, estimated) #compute rmse 
        deg = len(model)-1

        pylab.figure()
        pylab.title('Temperature against Time' + 
                    "\n" + 
                     f'Deg = {deg}, RMSE={model_rmse:.4f}')
        pylab.plot(x,
                   y,
                   '.', 
                   color='blue')
        pylab.plot(x, 
                   estimated, 
                   color='red')
        
        pylab.show()

if __name__ == '__main__':

    pass 

    # Part A.4
    # Part A4 I (Jan 10th temperatures)
    climate_data = Climate('data.csv') #get sample data
    sample_years = pylab.array(range(1961, 2010))
    sample_temp = pylab.array([climate_data.get_daily_temp('NEW YORK', 1, 10, year) 
                   for year in sample_years])
    
    #fit jan 10th temperatures to linear time model and plot
    jan_10_model = generate_models(sample_years, sample_temp, [1])
    evaluate_models_on_training(sample_years, sample_temp, jan_10_model)

    # Part A4 II (Annual temperatures)
    #get avg yearly temps
    avg_yearly_temps = []
    for year in sample_years:
        yearly_temps = climate_data.get_yearly_temp('NEW YORK', year)
        avg_temp = pylab.sum(yearly_temps)/len(yearly_temps)
        avg_yearly_temps.append(avg_temp)
    avg_yearly_temps = pylab.array(avg_yearly_temps)
    
    #fit avg yearly temps to time model and plot
    avg_year_temp_model = generate_models(sample_years, avg_yearly_temps, [1])
    evaluate_models_on_training(sample_years, avg_yearly_temps, avg_year_temp_model)   


    # Part B 
    # annual temps averages over multiple cities (national temp)
    avg_national_temp = gen_cities_avg(climate_data, CITIES, sample_years)
    avg_national_temp_model = generate_models(sample_years, avg_national_temp, [1])
    evaluate_models_on_training(sample_years, avg_national_temp, avg_national_temp_model)


    # Part C
    # model moving averages of the national temp instead
    moving_avg_temp = moving_average(avg_national_temp, 5)
    moving_avg_temp_model = generate_models(sample_years, moving_avg_temp, [1])
    evaluate_models_on_training(sample_years, moving_avg_temp, moving_avg_temp_model)

    # Part D.2
    moving_avg_temp_models = generate_models(sample_years, moving_avg_temp, [1,2,20])
    evaluate_models_on_training(sample_years, moving_avg_temp, moving_avg_temp_models)

    #create testing set 
    test_years = pylab.array(range(2010, 2016))
    test_avg_national_temp = gen_cities_avg(climate_data, CITIES, test_years)
    test_moving_avg_temp = moving_average(test_avg_national_temp, 5)
    evaluate_models_on_testing(test_years, test_moving_avg_temp, moving_avg_temp_models)

    # Part E
    std_devs = gen_std_devs(climate_data, CITIES, sample_years)
    std_devs_moving_avg = moving_average(std_devs, 5)
    std_dev_models = generate_models(sample_years, std_devs_moving_avg, [1])
    evaluate_models_on_training(sample_years, std_devs_moving_avg, std_dev_models)
