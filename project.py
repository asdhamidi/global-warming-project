from audioop import mul
from cProfile import label
from math import sqrt
import pylab
import re

# Cities in our weather data
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


class Climate(object):
    """
    Utility class for saving and processing the weather data points.
    """

    def __init__(self, filename):
        """
        Initializes a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.
        """
        self.rawdata = {}

        f = open(filename, 'r')

        header = f.readline().strip().split(',')  # Holds headers of the data
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)',
                            items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])

            # Creating a dict for the city
            if city not in self.rawdata:
                self.rawdata[city] = {}

            # Creating a dict for year of the city
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}

            # Creating a dict for month of the year
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}

            # Adding day key with the temperature value to the month dict.
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_yearly_temp(self, city, year):
        """
        Gets the daily temperatures for the given year and city.
        """
        temperatures = []

        # Safety Check
        if not city in self.rawdata or not year in self.rawdata[city]:
            raise Exception("Data Not Available")

        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])

        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Returns the daily temperature for the given city and time.
        """

        # Provided city is not available
        check1 = city in self.rawdata
        # Provided year is not available
        check2 = year in self.rawdata[city]
        # Provided month is not available
        check3 = month in self.rawdata[city][year]
        # Provided day is not available
        check4 = day in self.rawdata[city][year][month]

        checks = check1 and check2 and check3 and check4

        if checks:
            return self.rawdata[city][year][month][day]


def generate_models(x, y, degs):
    """
    Generates regression models by fitting a polynomial for each degree in degs
    to points (x, y).
    """
    models = []
    for degree in degs:
        models.append(pylab.polyfit(x, y, degree))

    return models


def r_squared(y, estimated):
    """
    Calculates the R-squared error term.

    R^2 = 1 - ((Σ yi - fi) ^ 2) / (Σ yi - Ȳ) ^ 2) 

    R^2 is the proportion of the variation in the dependent variable that is predictable from the independent variable.
    """
    numerator = sum((y - estimated) ** 2)
    mean = pylab.mean(y)
    denominator = sum((y - mean) ** 2)

    return 1 - (numerator / denominator)


def evaluate_models_on_training(x, y, models, message="", filename=""):
    """
    Plots data points as blue dots and estimated data as a red line with plot function.
    """
    for model in models:
        yEstimates = pylab.polyval(model, x)
        modelDetails = str(len(model) - 1)
        modelR2 = str(r_squared(y, yEstimates))

        pylab.plot(x, y, "b.", label="Measured data")
        pylab.plot(x, yEstimates, "r-", label="Model")
        pylab.xlabel("Years")
        pylab.ylabel("Temperature")
        pylab.title(message+"\nModel, Degree "+modelDetails+"\nR^2: "+modelR2)
        pylab.legend(loc="best")
        pylab.savefig(filename, dpi=1+500)
        pylab.show()


def gen_cities_avg(climate, multi_cities, years):
    """
    Computes the average annual temperature over multiple cities.
    """

    totalYearlyAvg = []
    for year in years:
        totalYearlyData = []

        for city in multi_cities:
            yearlyData = climate.get_yearly_temp(city, year)
            totalYearlyData.append(yearlyData)

        totalYearlyData = pylab.array(totalYearlyData)
        totalYearlyAvg.append(totalYearlyData.mean())

    return pylab.array(totalYearlyAvg)


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Moving average = {y1/1, (y1+y2)/2, (y1+y2+y3)/3,..., (yn-2, yn-1, yn)/window_lenght}
    """
    movingAvgs = []
    i = 1
    while i <= len(y):
        if i <= window_length:
            movingAvgs.append(sum(y[0:i]) / i)
        else:
            movingAvgs.append(sum(y[i-window_length:i]) / window_length)
        i += 1

    return pylab.array(movingAvgs)


def rmse(y, estimated):
    """
    Calculate the root mean square error term for actual values and estimated values.

    RMSE = √(Σ(yi - fi) ^ 2) / n)
    """
    return sqrt(sum((y - estimated) ** 2) / len(y))


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
    annualStdDev = []
    for year in years:
        allCitiesYearlyTemp = []
        for city in multi_cities:
            yearlyTemp = climate.get_yearly_temp(city, year)
            allCitiesYearlyTemp.append(yearlyTemp)
        # converting list to an array.
        allCitiesYearlyTemp = pylab.array(allCitiesYearlyTemp)
        # calculating mean for each day from all the city arrays.
        dailyMean = allCitiesYearlyTemp.mean(axis=0)
        # calculating standard deviation across the year.
        stdDev = pylab.std(dailyMean)
        annualStdDev.append(stdDev)
    # converting list to an array.
    annualStdDev = pylab.array(annualStdDev)
    return annualStdDev


def evaluate_models_on_testing(x, y, models, message="", filename=""):
    """
    For each regression model, computes the RMSE for this model and plot the
    test data along with the model’s estimation.
    """
    for model in models:
        yEstimates = pylab.polyval(model, x)
        modelDetails = str(len(model) - 1)
        modelR2 = str(rmse(y, yEstimates))

        pylab.plot(x, y, "b.", label="Measured data")
        pylab.plot(x, yEstimates, "r-", label="Model")
        pylab.xlabel("Years")
        pylab.ylabel("Temperature")
        pylab.title(message+"\nModel, Degree " +
                    modelDetails+"\nRMSE: "+modelR2)
        pylab.legend(loc="best")
        pylab.savefig(filename, dpi=1+500)
        pylab.show()


if __name__ == '__main__':
    data = Climate("data.csv")
    xData = pylab.array(TRAINING_INTERVAL)
    xDataTest = pylab.array(TESTING_INTERVAL)

    # Part 1 - Getting Data of New York, 1961-2009, creating its model, and plotting it.
    dailyData = []
    messageDaily = "New York: Jan 10th, 1961-2009"

    for year in TRAINING_INTERVAL:
        dailyData.append(data.get_daily_temp("NEW YORK", 1, 10, year))

    yDataDaily = pylab.array(dailyData)

    modelDaily = generate_models(xData, yDataDaily, [1])
    evaluate_models_on_training(
        xData, yDataDaily, modelDaily, messageDaily, "A4-1.png")

    # Getting Average of Data of New York, 1961-2009, creating its model, and plotting it.
    avgData = []
    messageAvg = "New York: Average Temperature(1961-2009)"

    for year in TRAINING_INTERVAL:
        yearlyData = data.get_yearly_temp("NEW YORK", year)
        yearlyMean = yearlyData.sum() / len(yearlyData)
        avgData.append(yearlyMean)

    yDataAvg = pylab.array(avgData)

    modelAvg = generate_models(xData, yDataAvg, [1])
    evaluate_models_on_training(
        xData, yDataAvg, modelAvg, messageAvg, "A4-2.png")

    # Getting Average of data of all cities, 1961-2009, creating its model, and plotting it.
    nationalAvgData = gen_cities_avg(data, CITIES, TRAINING_INTERVAL)
    messageNationalAvg = "All Cities Yearly Average (1961-2009)"

    modelCityAvg = generate_models(xData, nationalAvgData, [1])
    evaluate_models_on_training(
        xData, nationalAvgData, modelCityAvg, messageNationalAvg, "B.png")

    # Getting Moving average of data of all cities, 1961-2009, creating its model, and plotting it.
    movingAvgData = moving_average(nationalAvgData, 5)
    messageMovingAvg = "All Cities: Yearly Moving Average (1961-2009)"

    modelMovingAvg = generate_models(xData, movingAvgData, [1, 2, 20])
    evaluate_models_on_training(xData, movingAvgData, [
                                modelMovingAvg[0]], messageMovingAvg, "D1-1.png")
    evaluate_models_on_training(xData, movingAvgData, [
                                modelMovingAvg[1]], messageMovingAvg, "D1-2.png")
    evaluate_models_on_training(xData, movingAvgData, [
                                modelMovingAvg[2]], messageMovingAvg, "D1-3.png")

    # Using the models above and testing the model using RMSE.
    nationalAvgDataTest = gen_cities_avg(data, CITIES, TESTING_INTERVAL)
    movingAvgDataTest = moving_average(nationalAvgDataTest, 5)
    evaluate_models_on_testing(xDataTest, movingAvgDataTest, [
                               modelMovingAvg[0]], "Model vs Testing Data (2010-2016)", "D2-1.png")
    evaluate_models_on_testing(xDataTest, movingAvgDataTest, [
                               modelMovingAvg[1]], "Model vs Testing Data (2010-2016)", "D2-2.png")
    evaluate_models_on_testing(xDataTest, movingAvgDataTest, [
                               modelMovingAvg[2]], "Model vs Testing Data (2010-2016)", "D2-3.png")

    # Getting S of data of all cities, 1961-2009, creating its model, and plotting it.
    stdDevData = gen_std_devs(data, CITIES, TRAINING_INTERVAL)
    stdDevMoving = moving_average(stdDevData, 5)
    stdDevModel = generate_models(xData, stdDevMoving, [1])
    evaluate_models_on_training(
        xData, stdDevMoving, stdDevModel, "Extreme Temp Variation Trend (1961-2009)", "E.png")
