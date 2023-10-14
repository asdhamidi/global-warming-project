# Climate Data Analysis

This project focuses on a detailed analysis of climate data for the top 20 cities in the United States over a 50-year period. The primary objective is to investigate changes in temperature, extreme temperature events, and other climate-related phenomena. The analysis employs statistical and machine learning techniques to gain insights from the data.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)
    - [Data Preparation](#data-preparation)
    - [Exploratory Data Analysis](#exploratory-data-analysis)
    - [Statistical Analysis](#statistical-analysis)
    - [Machine Learning](#machine-learning)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)

## Features

- In-depth analysis of climate data for 20 major US cities.
- Examination of temperature trends and extreme temperature events.
- Application of statistical and machine learning techniques.

## Getting Started

### Prerequisites

Before running this project, ensure you have the following software and libraries installed on your system:

- Python
- Required Python libraries (NumPy, Matplotlib, Pandas, Scikit-Learn)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/asdhamidi/global-warming-project.git
   ```

2. Navigate to the project directory:

   ```bash
   cd global-warming-project
   ```

3. Install the required Python libraries:

   ```bash
   pip install numpy matplotlib pandas scikit-learn
   ```

## Usage

### Data Preparation

1. Prepare your climate data in the following format:

   ```csv
   CITY,TEMPERATURE,DATE
   SEATTLE,9.7,19610107
   SEATTLE,7.2,19610108
   # Add records for all 20 cities and over 50 years.
   ```

### Exploratory Data Analysis

1. Use the provided Python scripts to load and explore the climate data.
2. Perform data visualization to understand temperature trends, extreme events, and other statistical characteristics.

### Statistical Analysis

1. Employ statistical methods, including linear regression, to establish relationships between variables and identify temperature trends.
2. Calculate relevant statistical metrics to quantify changes in climate parameters.

### Machine Learning

1. Utilize machine learning algorithms for time series analysis and forecasting of temperature trends.
2. Evaluate the performance of machine learning models using statistical measures such as R-squared and root mean square error (RMSE).

## Tech Stack

- Python for data analysis and machine learning.
- NumPy for numerical operations.
- Pandas for data manipulation.
- Matplotlib for data visualization.
- Scikit-Learn for machine learning algorithms.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create a GitHub issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
