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
    - Reads in 2 required excel files. The first excel file contains the site and study IDs, number of enrollments, prior enrollment rate per site, the state each site is located in, and the zip code for the site. The second excel file contains the current prevalence of the disease of interest by state. This file is obtained through the NIH State Cancer Profile webtool in the following link: https://statecancerprofiles.cancer.gov/map/ 
    - NIH SCP file set to match to state abbreviations dictionary
- zip_codes.py
    - Cleans zip codes that have a '-' and 4 additional digits to prevent errors during interactive map generation
    - Converts zip codes to latitude and longitude 
- populations.py
    - Gathers the current state populations from census data for the year of interest; default is the most current data available
    - Merges data frames created from both excel files based on the correct state
    - Ensures values are numeric and drops rows that have missing values
    - Encodes sites with a unique identifier
- bayes_model.py
    - Cleans any NaN or empty columns and saves a new data frame with cleaned data as 'df_model'
    - Site and study indexes are created to ensure correct assigning of performance multiplier to the correct site, regardless of duplicate site and study combination occurring in different years
    - Sets correct values to corresponding variables for the model
    - Maps out the model including coefficients, likelihoods, and random effects
- output.py
    - Runs the learning model to determine site and study effects and then assigns a performance multiplier to each site and study index that shows how well the site is doing or how difficult the study protocol is compared to what the model expects
    - Saves results as a .csv, .xlsx, and an .html file. The CSV file does not include the heatmap to make results simpler for further analysis with additional programs. The excel and html files do include the heatmap.
    - Heatmap is for the performance multiplier values, not the random variables u_site or u_study that are learned from the model. Performance multiplier is determined from this variable by taking: e(u_site) or e(u_study)
    - Writes interactive heatmap, noting site location across US map, out to new output file: interactive_heatmap.html

## Installation

To clone the repository:
```
git clone https://github.com/kwill423/enrollment_proj.git
```
Navigate to the directory:
```
cd enrollment_proj
```
Create your environment:
```
.venv/Scripts/activate
```
Install requirements: 
```
pip install -r requirements.txt
```

## Resolving Common Errors

- When inputting the year in get_state_populations(year), note that state population data may not be available for the year if it is within the last 2 years. To avoid this issue the program will input the most available data if None is passed through the funtion.
- If you experience issues with fitting the model to the data such as high rhat values or low ess values, a good starting point is to check the summary statistics:
    ```
    summary = az.summary(self.trace)
    print(summary.sort_values("r_hat", ascending=False))
    print(summary.sort_values("ess_bulk"))
    ```
