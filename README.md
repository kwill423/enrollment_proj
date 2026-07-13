# Clinical Trial Enrollment Analysis Project
## Bayesian Heirarchical Poisson Regression

This project was created as a part of my 2026 internship with Astellas Pharmaceuticals under the R&D Analytics, Insights, and Enablement team. 

The purpose of this project is to make a model that will estimate the expected enrollment rate per site based on population and disease prevalence. Then determine if a site is over or underperforming as more updates occur. The first goal is to have it work with parameters such as population size, past data, duration of study, and be site specific. This is to have a more accurate representation of whether sites are hitting target enrollment or not while accounting for random variables. The second goal, if the first is fulfilled and time allows, is to add in another parameter that breaks down the enrollment goal per site to specific ethnicities. This is to address concerns regarding recruitment of minorities that accurately represents the prevalence of disease for those populations.

## Features
- requirements.txt
    - Lists required libraries that can be installed with: 
    ```
    .venv/Scripts/activate
    pip install -r requirements.txt
    ```
- input.py
    - Reads in 2 required excel files. The first excel file contains the prior enrollment rate per site, a key column that is used as a unique identifier per site, and the state each site is located in. The second excel file contains the current prevalence of the disease of interest by state. This file is obtained through the NIH State Cancer Profile webtool in the following link: https://statecancerprofiles.cancer.gov/map/ 
    - NIH SCP file set to match to state abbreviations dictionary
    - get_state_populations(): Gathers the current state populations from census data for the year of interest; current or year prior is recommended

- clean.py
    - Merges data frames created from both excel files based on the correct state
    - Cleans data: ensures values are numeric and drops rows that have missing values
    - Encodes sites with a unique identifier
- bayes_model.py
    - Sets correct values to corresponding variables for the model
    - Maps out the model including coefficients, likelihoods, and random effects
    - Prepares site performance numbers for output.py module
- output.py
    - Writes results per site out to sys.stout
    - Contains color code for performance values
    - Writes heatmap out to new output file: site_performance_heatmap.png

## Installation

Clone the repo:

## Resolving Common Errors

- If you experience issues with fitting the model to the data such as high rhat values or low ess values, a good starting point is to check the summary statistics:
    ```
    summary = az.summary(self.trace)
    print(summary.sort_values("r_hat", ascending=False))
    print(summary.sort_values("ess_bulk"))
    ```
