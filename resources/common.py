#!/usr/bin/env python
import pdb
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from typing import Tuple, Any
import time



import resources.logging_config as lrh_logging
log = lrh_logging.get_logger("cli", json=False)

class linear_regression_helper:
    def __init__(self, df=None):
        self.dataset = df
    
    
    def get_means(self, data: pd.DataFrame) -> pd.Series:
        """
        Compute and return the means for columns.

        Parameters:
        - data (pd.DataFrame): The DataFrame containing the data.

        Returns:
        - pd.Series: A Series containing the mean values of each column.
        """        
        return data.mean()
    
    def get_stdd(self, data: pd.DataFrame) -> pd.Series:
        """
        Compute and return the standard deviations for columns.

        Parameters:
        - data (pd.DataFrame): The DataFrame containing the data.

        Returns:
        - pd.Series: A Series containing the standard deviations of each column.
        """
        return data.std()
    
    def get_variance(self, data: pd.DataFrame) -> pd.Series:
        """
        Compute and return the variances for columns.

        Parameters:
        - data (pd.DataFrame): The DataFrame containing the data.

        Returns:
        - pd.Series: A Series containing the variances of each column.
        """
        return data.var()        
    
    def run_linear_regression(self, independent_var: pd.Series, dependent_var: pd.Series) -> Tuple[Any, float, pd.DataFrame]:
        """
        Rum linear regression given a DataFrame and the name of the dependent variable.

        Parameters:
        - data (pd.DataFrame): The DataFrame containing all variables.
        - dependent_var (str): The column name of the dependent variable in the DataFrame.

        Returns:
        - Tuple[np.ndarray, float, pd.Series]: A tuple containing the coefficients array, the intercept of the regression model, and the DataFrame of independent variables.
        """
        X = independent_var.values.reshape(-1, 1)
        y = dependent_var
        model = LinearRegression().fit(X, y)
        
        return model.coef_, model.intercept_, independent_var
        
    def scatter_plot_w_fit_line(self, x: pd.Series, 
                                y: pd.Series, 
                                slope: float, 
                                intercept: float, 
                                plot_title: str) -> None:
        """
        Plot a scatter plot with the regression line.

        Parameters:
        - x (pd.Series): The independent variable.
        - y (pd.Series): The dependent variable.
        - slope (float): The slope of the regression line.
        - intercept (float): The intercept of the regression line.
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='blue', label='Data Points')
        plt.plot(x, slope*x + intercept, color='orange', label='Fitted Line')
        plt.xlabel(f'{x.name.replace("_", " ")} X')
        plt.ylabel(f'{y.name.replace("_", " ")} Y')
        plt.title(plot_title)
        plt.legend()
        plt.show()
        time.sleep(5)
        
    def read_data(self, file_path: str, is_csv=True) -> pd.DataFrame:
        """
        Read a CSV file and return a DataFrame.

        Parameters:
        - file_path (str): The path to the CSV file.
        - is_csv (bool): A flag to indicate if the file is a typical CSV file. For now, it will take a space-separated data if it isn't a typical CSV file.

        Returns:
        - pd.DataFrame: The DataFrame containing the data.
        """
        if not is_csv:
            self.dataset = pd.read_csv(file_path, delimiter=" ")
            return self.dataset
        self.dataset = pd.read_csv(file_path)
        return self.dataset
        

def get_stats(data: pd.DataFrame, var1: str, var2: str) -> pd.DataFrame:
    """
    Compute sample variance, standard deviation, covariance, correlation coefficient, and correlation coefficient squared.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing the data.
    - var1 (str): The column name of the first variable.
    - var2 (str): The column name of the second variable.

    Returns:
    - pd.DataFrame: A DataFrame containing the computed statistics.
    """
    
    # Sample mean, variance, and standard deviation per column
    means = data.mean()
    variances = data.var()
    stdds = data.std()
    data = data.fillna(data.mean())
    
    # Sample covariance and correlation matrices
    covariance_matrix = data.cov()
    correlation_matrix = data.corr()

    # Sample covariance and correlation     
    covariance_xy = covariance_matrix.loc[var1, var2]
    correlation_xy = correlation_matrix.loc[var1, var2]
    
    corr_squared = correlation_xy ** 2
    
    results =  pd.DataFrame({
        'Mean': means,
        'Variance': variances,
        'Standard Deviation': stdds,
        'Covariance XY': covariance_xy,
        'Correlation XY': correlation_xy,
        'Correlation XY Squared': corr_squared
        # var1 + '-' + var2 + ' Covariance': covariance_xy,
        # var1 + '-' + var2 + ' Correlation': correlation_xy,
        # var1 + '-' + var2 + ' Correlation Squared': corr_squared
    }).rename_axis('Stats').reset_index()
    
    results = results.round(4).set_index('Stats').T
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print( results[[var1, var2]])
                
    return results
    
    
def print_stat(results: pd.DataFrame, var1, var2) -> None:
    # Replace underscores in column headers with spaces
    results = results[[var1, var2]]
    results.columns = results.columns.str.replace('_', ' ')
    
    # if 'Run' in results.columns:
    #     results = results.drop('Run', axis=1)


    # Create a new figure and set its size
    fig, ax = plt.subplots(figsize=(10, 4)) 

    # Hide axes
    ax.axis('off')

    # Create a table and add it to the figure
    table = plt.table(cellText=results.values, 
                    colLabels=results.columns, 
                    rowLabels=results.index, 
                    cellLoc = 'center', 
                    loc='center')

    # Set the font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Set the column widths
    table.auto_set_column_width(col=list(range(len(results.columns))))

    plt.show()
    time.sleep(5)
    
    
    

            
    