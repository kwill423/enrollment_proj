from module import EnrollmentData
from input import load_enroll_data, load_prev_data
from populations import get_state_populations, merge_population
from bayes_model import run_model
from output import compute_performance, excel_output, png_output

def main():
    data = EnrollmentData()
    
    # Load
    data.load_enroll_data("enrollment_proj/data/dummy_data.xlsx")
    data.load_prev_data("enrollment_proj/data/pancreatic_cancer_prev.xlsx")

    # Clean
    data.get_state_populations(2025)
    data.merge_population()

    # Model
    data.run_model()

    # Output
    data.compute_performance()
    data.excel_output()
    data.png_output()


if __name__ == "__main__":
    main()
