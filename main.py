from src.class_mod import EnrollmentData
from src.input import load_enroll_data, load_prev_data
from src.populations import get_state_populations, merge_population, merge_prevalence, state_mapping
from src.bayes_model import run_model
from src.output import compute_performance, excel_output, png_output

def main():
    data = EnrollmentData()
    
    # Load
    load_enroll_data(data, "data/dummy_data.xlsx")
    load_prev_data(data, "data/pancreatic_cancer_prev.xlsx")
 
    # Clean
    get_state_populations(data, 2023)
    state_mapping(data)
    merge_population(data)
    merge_prevalence(data)

    # Model
    
    try:
        print("Starting model")
        run_model(data)
        print("Model finished")
    except Exception as e:
        print("Model error:", repr(e))
        raise


    # Output
    '''
    compute_performance(data)
    print(data.site_performance)
    print(data.study_performance)
    excel_output(data)
    png_output(data)
    '''

if __name__ == "__main__":
    main()
