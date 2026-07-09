from src.class_mod import EnrollmentData
from src.input import load_enroll_data, load_prev_data
from src.populations import get_state_populations, merge_population, merge_prevalence
from src.bayes_model import run_model
from src.output import compute_performance, excel_output, png_output

def main():
    data = EnrollmentData()
    
    # Load
    load_enroll_data(data, "data/dummy_data.xlsx")
    load_prev_data(data, "data/pancreatic_cancer_prev.xlsx")

    # Clean
    get_state_populations(data, 2023)
    print(data.df_pop.head(10))
    merge_population(data)
    merge_prevalence(data)
    print(data.df.head(10))

    # Model
    run_model(data)

    # Output
    compute_performance(data)
    excel_output(data)
    png_output(data)


if __name__ == "__main__":
    main()
