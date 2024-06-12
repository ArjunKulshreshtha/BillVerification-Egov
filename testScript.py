import requests
import pandas as pd
from datetime import datetime

# Define the Flask app URL
FLASK_APP_URL = "http://127.0.0.1:5000/verify_document"

# Define test cases
test_cases = [ #Text, date, email, integer, decimal
    {
        "field_name": "Name",
        "field_value": "Vijay Laxman Mahajan",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },
    {
        "field_name": "Name",
        "field_value": "John Doe",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },
    {
        "field_name": "Bill Date",
        "field_value": "10/02/2020",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },
    {
        "field_name": "Bill Date",
        "field_value": "22/04/2020",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },
    {
        "field_name": "Bill Amount",
        "field_value": "Rs. 2500",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },
    {
        "field_name": "Bill Amount",
        "field_value": "Rs. 2000",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },
    {
        "field_name": "Consumption",
        "field_value": "274.8 units",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },
    {
        "field_name": "Consumption",
        "field_value": "274.2 units",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },

    {
        "field_name": "email",
        "field_value": "vijay@mahajan.com",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },
    {
        "field_name": "email",
        "field_value": "john@doe.org",
        "doc_path": "imgs/testingTypes.jpg",
        "user_choice": "gpt",
    },

    # Add more test cases as needed
]


# Function to run tests and log results
def run_tests(test_cases, iterations):
    results = []
    for i, test in enumerate(test_cases):
        for _ in range(iterations):  # Loop to run the test cases 100 times
            response = requests.post(FLASK_APP_URL, json=test)
            if response.status_code == 200:
                try:
                    result_data = response.json()
                    extracted_values = result_data.get("extracted_values", ["N/A"])[0]
                    verification_result = result_data.get("verification_result", "N/A")
                    match_result = (
                        verification_result.split(", ")[0]
                        if verification_result != "N/A"
                        else "N/A"
                    )
                    confidence_score = (
                        verification_result.split(", ")[1].replace("%", "")
                        if verification_result != "N/A"
                        else "N/A"
                    )

                    results.append(
                        {
                            "Test Case": i + 1,
                            "Field Name": test["field_name"],
                            "Expected Value": test["field_value"],
                            "Extracted Values": extracted_values,
                            "Match Result": match_result,
                            "Confidence Score": confidence_score,
                            "Status": "Success",
                        }
                    )
                except (ValueError, IndexError, AttributeError) as e:
                    results.append(
                        {
                            "Test Case": i + 1,
                            "Field Name": test["field_name"],
                            "Expected Value": test["field_value"],
                            "Status": "Failed",
                            "Error": str(e),
                        }
                    )
            else:
                try:
                    error_message = response.json().get("error", "Unknown Error")
                except ValueError:
                    error_message = response.text

                results.append(
                    {
                        "Test Case": i + 1,
                        "Field Name": test["field_name"],
                        "Expected Value": test["field_value"],
                        "Status": "Failed",
                        "Error": error_message,
                    }
                )

    return results


# Run the tests and get results
iterations = 5
test_results = run_tests(test_cases, iterations)

# Create a DataFrame and save to Excel
df = pd.DataFrame(test_results)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
excel_filename = (
    f'test_results/test_results_{timestamp}_{test_cases[0].get("user_choice")}.xlsx'
)
df.to_excel(excel_filename, index=False)

print(f"Test results saved to {excel_filename}")

# if __name__ == '__main__':
#     run_tests(test_cases)
