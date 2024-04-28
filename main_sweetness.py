#!/usr/bin/env python
import numpy as np
import math
from itertools import permutations
import pdb

import resources.common as cmn
import resources.logging_config as lrh_logging
log = lrh_logging.get_logger("cli", json=False)


def main():
    lrh = cmn.linear_regression_helper()
    '''Define the data file and the x and y labels for the linear regression here'''
    lrh.read_data('data/sweetness.txt', is_csv=False)
    x_label = 'Pectin_(parts_per_million)'
    y_label = 'Sweetness_index'
    
    # Print statistics
    df_stats = cmn.get_stats(lrh.dataset, x_label, y_label)
    cmn.print_stat(df_stats, x_label, y_label)
    
    # Run linear regression
    m, b, X = lrh.run_linear_regression(lrh.dataset[x_label], 
                                        lrh.dataset[y_label])
    log.info(f"Coef (slope): {m}, Intercept: {b}")
    
    # Visualize the data
    lrh.scatter_plot_w_fit_line(lrh.dataset[x_label], 
                                lrh.dataset[y_label], 
                                m[0], 
                                b,
                                'Homework #3 Part II: Sleep and Cancer - 500 Cities Data')
    
                
    
            
        

if __name__ == "__main__": main()
