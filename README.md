# Clinical Trial Enrollment Analysis Project
## Bayesian Heirarchical Poisson Regression

This project was created as a part of my 2026 internship with Astellas Pharmaceuticals under the R&D Analytics, Insights, and Enablement team. 

The purpose of this project is to make a model that will estimate the expected enrollment rate per site based on population and disease prevalence. Then determine if a site is over or underperforming as more updates occur. The first goal is to have it work with parameters such as population size, past data, duration of study, and be site specific. This is to have a more accurate representation of whether sites are hitting target enrollment or not while accounting for random variables. The second goal, if the first is fulfilled and time allows, is to add in another parameter that breaks down the enrollment goal per site to specific ethnicities. This is to address concerns regarding recruitment of minorities that accurately represents the prevalence of disease for those populations.

## Features
- requirements.txt
    - Lists required libraries that can be installed with
    ```
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

## License

## Set Up
Prior to running the program, the excel file containing enrollment data needs to be merged and cleaned if taken from Veeva like the original files. Veeva provided the subject ID, study, study site, screened date, fiscal year, and country columns. Formulas were used to create a cleaned country column and key containing a unique ID for the study|site|FY. The second sheet of the first file is what pulls the calculated site enrollment rate, SER. A separate Veeva report contains the state for each study site. The two files are merged using a simple python script below or directly through excel:
```
import pandas as pd

df1 = pd.read_excel("ASP_enrollment.xlsx", sheet_name= "SiteLevel")
df2 = pd.read_excel("site_states.xlsx")

merged = df1.merge(
    df2[['Study', 'Study Site', 'State',]],
    on=['Study', 'Study Site'],
    how='left'
)

merged = merged[merged["Country"] == "USA"]
merged.to_excel("merged_enroll_rate.xlsx", index=False)
```
This is what creates "merged_enroll_rate.xlsx", the file needed to input into the program. If done correctly, it should contain: Study, Study Site, Fiscal Year, First Enrolled Date, Last Enrolled Date, Pts per Site, Duration (months), SER, Country, Key, State. 
If issues arise while running, ensure the columns are an exact match to what is written above.
The NIH excel file also had a cleaned State column prior to input and a column "FIPS" that is deleted for a better set up. The line below is the excel formula to add into the added "State (cleaned)" column:
```
=TRIM(LEFT(A2, FIND("(", A2 & "(") - 1))))
```
Cleaning the NIH file is what allows you to use columns B and C easily.