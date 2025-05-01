import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os
from dotenv import load_dotenv  # Import dotenv to handle environment variables
from datetime import datetime
import time
import sys

# Load environment variables from a .env file
load_dotenv()

# Configurations (Environment Variables)
BASE_URL = os.getenv("BASE_URL", "https://www.jobs.nhs.uk/api/v1/search_xml")  # Default value for BASE_URL
API_KEY = os.getenv("API_KEY")  # Optional, in case the API requires a key in the future

# Check if required environment variables are set
if not BASE_URL:
    print("Error: The BASE_URL environment variable is not set.")
    sys.exit(1)

# Employer names for Nottingham region
TARGET_EMPLOYERS = [
    "Nottingham University Hospitals NHS Trust",
    "Nottinghamshire Healthcare NHS Foundation Trust",
    "Sherwood Forest Hospitals NHS Foundation Trust",
    "Nottingham CityCare Partnership CIC",
    "NHS Nottingham and Nottinghamshire Integrated Care Board"
]

# Other configurations
MAX_PAGES = 2000  # Increased maximum page limit to ensure all pages are fetched
VERBOSE = True  # Verbosity flag to control debug output
MAX_RETRIES = 3  # Maximum number of retries for failed requests

# Function to fetch job adverts from NHS Jobs API
def fetch_job_data():
    all_jobs = []
    unique_jobs = set()  # To track unique Job Reference and Vacancy IDs to avoid duplicates
    page = 1
    total_pages = None
    total_vacancies_reported = 0  # Track total number of vacancies reported by the API

    # Prepare target employers for case-insensitive substring matching
    target_employers_lower = [employer.lower() for employer in TARGET_EMPLOYERS]

    # Collect unique employer names for debugging
    all_employer_names = set()

    while page <= (total_pages if total_pages else MAX_PAGES):
        params = {
            "page": page
        }
        retries = 0
        while retries < MAX_RETRIES:
            try:
                # Add API Key to the request headers (if required by the API)
                headers = {}
                if API_KEY:
                    headers["Authorization"] = f"Bearer {API_KEY}"

                response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)  # Adding a timeout to prevent hanging requests
                if response.status_code == 200:
                    break
                else:
                    print(f"Failed to fetch data for page {page}, Status Code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Network error occurred: {e}")
               
            retries += 1
            wait_time = 2 ** retries  # Exponential backoff
            print(f"Retrying page {page} in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"Max retries exceeded for page {page}. Skipping.")
            page += 1
            continue
       
        # Debugging output
        if VERBOSE:
            print(f"Request URL: {response.url}")
            print(f"Status Code: {response.status_code}")
       
        # Validate if response content is not empty before parsing
        if not response.content.strip():
            print(f"Empty response content for page {page}.")
            break
       
        # Parse XML
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            print(f"Invalid XML response for page {page}. Error: {e}")
            break
       
        if VERBOSE and page == 1:
            print(response.content.decode('utf-8'))  # Print XML content for the first page to verify structure
       
        if total_pages is None:
            # Retrieve total number of pages from the first response
            total_pages_elem = root.find(".//totalPages")
            if total_pages_elem is None or not total_pages_elem.text.isdigit():
                print("Total pages could not be determined. Setting a default limit.")
                total_pages = MAX_PAGES
            else:
                total_pages = int(total_pages_elem.text)
                if VERBOSE:
                    print(f"Total Pages Available: {total_pages}")

            # Retrieve total number of results
            total_results_elem = root.find(".//totalResults")
            if total_results_elem is not None and total_results_elem.text.isdigit():
                total_vacancies_reported = int(total_results_elem.text)
                print(f"Total Vacancies Reported by API: {total_vacancies_reported}")

        vacancy_details = root.findall(".//vacancyDetails")
        if not vacancy_details:
            print(f"No vacancies found on page {page}. Inspecting XML structure...")
            if VERBOSE:
                print(response.content.decode('utf-8'))  # To check if the structure is as expected
            break  # No more data

        # Process each vacancy
        for vacancy in vacancy_details:
            employer_name = vacancy.find("employer").text if vacancy.find("employer") is not None else ""
            employer_name_lower = employer_name.lower()
            location = ", ".join([loc.text for loc in vacancy.findall("locations/location")])
            job_reference = vacancy.find("reference").text if vacancy.find("reference") is not None else None
            vacancy_id = vacancy.find("id").text if vacancy.find("id") is not None else None

            # Collect unique employer names for debugging
            all_employer_names.add(employer_name)

            # Check if employer name contains any target employer name (case-insensitive substring match)
            if any(target_employer in employer_name_lower for target_employer in target_employers_lower):
                # Avoid adding duplicate jobs by checking Job Reference and Vacancy ID
                if (job_reference, vacancy_id) not in unique_jobs:
                    job = {
                        "Job Title": vacancy.find("title").text if vacancy.find("title") is not None else None,
                        "Employer": employer_name,
                        "Location": location,
                        "Salary Range": vacancy.find("salary").text if vacancy.find("salary") is not None else None,
                        "Job Reference": job_reference,
                        "Contract Type": vacancy.find("type").text if vacancy.find("type") is not None else None,
                        "Closing Date": vacancy.find("closeDate").text if vacancy.find("closeDate") is not None else None,
                        "Post Date": vacancy.find("postDate").text if vacancy.find("postDate") is not None else None,
                        "Vacancy ID": vacancy_id,
                        "URL": vacancy.find("url").text if vacancy.find("url") is not None else None,
                    }
                    all_jobs.append(job)
                    unique_jobs.add((job_reference, vacancy_id))
                else:
                    print(f"Duplicate job found: Job Reference {job_reference}, Vacancy ID {vacancy_id}. Skipping.")

        page += 1
        if page > total_pages:
            break

    # Print all unique employer names found
    print("Unique employer names found in the data:")
    for name in sorted(all_employer_names):
        print(f"- {name}")

    # Verify if we captured all vacancies reported
    if total_vacancies_reported > 0:
        if len(all_jobs) == total_vacancies_reported:
            print(f"Success: Retrieved all {len(all_jobs)} vacancies as reported by the API.")
        else:
            print(f"Warning: Retrieved jobs ({len(all_jobs)}) do not match the total reported vacancies ({total_vacancies_reported}).")
    else:
        print("Warning: Could not verify total vacancies as no valid count was reported by the API.")

    return all_jobs

# Function to generate CSV report and save to specified output path
def generate_csv(job_data):
    # Specify the output directory for the local drive
    output_dir = ""
    os.makedirs(output_dir, exist_ok=True)
   
    # Create the full file path
    filename = os.path.join(output_dir, f"nhs_jobs_report_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv")
   
    # Save the data to the file
    df = pd.DataFrame(job_data)
    df.to_csv(filename, index=False)
    print(f"CSV report generated: {filename}")
    return filename

# Main flow
def main():
    print("Script started")
    job_data = fetch_job_data()
    if job_data:
        generate_csv(job_data)
    else:
        print("No job data found.")

if __name__ == "__main__":
    main()
