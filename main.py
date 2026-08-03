from src.class_mod import EnrollmentData
from src.input import load_enroll_data, load_prev_data
from src.populations import get_state_populations, merge_population, merge_prevalence, state_mapping
from src.bayes_model import run_model
from src.output import compute_performance, excel_output, html_output
from src.zip_codes import clean_zip, zip_conversion

def main():
    
    data = EnrollmentData()
    
    # Load
    load_enroll_data(data, "data/merged_enroll_rate.xlsx")
    load_prev_data(data, "data/stomach_cancer_prev.xlsx")

    # Clean
    clean_zip(data)
    zip_conversion(data)
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

    compute_performance(
        data, 
        csv_path1= "results/site_performance_stomach.csv", 
        csv_path2= "results/study_performance_stomach.csv"
        )
    excel_output(
        data, 
        excel_path= "results/performance_stomach.xlsx"
        )
    html_output(
        data,
        html_path= "results/interactive_heatmap_stomach.html"
        )

if __name__ == "__main__":
    main()
