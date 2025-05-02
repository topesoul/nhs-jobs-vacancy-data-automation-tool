# NHS Jobs Vacancy Data Automation Tool

This repository provides a Python-based automation tool developed to streamline the collection of vacancy data from NHS Jobs and other public data sources, all via the NHS Jobs API. It was designed for Integrated Care Systems (ICS) and Trusts to reduce the time spent on manual gathering of job vacancy posts data from multiple websites, improve data consistency, and support workforce planning analysis. 

This is especially helpful given that, at any point in time, there could be over 2,000 jobs posted on the NHS Jobs site. The script offers a reliable and repeatable way to extract and standardise relevant vacancy data across a defined list of NHS organisations, including providers that do not publish vacancies on the same job boards e.g., via Trac.

---

## 🔍 What It Does

- Connects to the **NHS Jobs API** to retrieve XML-based job postings
- Automatically filters vacancy data based on a list of named NHS organisations
- Removes duplicate entries using a combination of job reference and vacancy ID
- Saves the extracted data as a structured CSV file to a local directory or a OneDrive/SharePoint synced folder (needs sepearate modification)
- Can be scheduled via **Windows Task Scheduler** or hosted on a **remote Windows server**
- (Optional) Integrates with SharePoint alerting or Power Automate flows for automatic notifications (needs sepearate modification)

---

## ⚙️ Setup Instructions

1. **Clone or download the repository**
2. Ensure Python 3.9+ is installed
3. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

4. Set up environment variables (see below for details)
5. In `main.py`, review the `TARGET_EMPLOYERS` list to reflect your ICS or provider geography
6. Update the `output_dir` path to match your system (e.g., a OneDrive-synced SharePoint folder)
7. Run the script manually or set up automation (see below)

---

## 🌐 Environment Variables

This project uses environment variables to manage configuration such as the API base URL. Create a `.env` file in the root directory of the project and add the following variables:
**Required Variables:**
  - `BASE_URL`: The base URL of the NHS jobs API (default: `https://www.jobs.nhs.uk/api/v1/search_xml`).
  - `API_KEY`: (Optional) If the API requires an authentication key in the future, add it here.

**Example `.env` File:**
```
BASE_URL=https://www.jobs.nhs.uk/api/v1/search_xml
API_KEY=your_api_key_here
```
**Instructions:**
1. Create a .env file in the root directory of the project (same folder as main.py).
2. Add the variables as shown above.
3. If no `API_KEY` is required, leave it blank. The script will still work with the default `BASE_URL`.
---

## 🔁 How Output Delivery Works

- The script generates a `.csv` file with all filtered job listings
- The output file is written to a local directory which is **synced to SharePoint via OneDrive**
- Once the file syncs to SharePoint, you can:
  - Use a **SharePoint alert** to notify users
  - Or trigger a **Power Automate (Flow)** to email stakeholders the report automatically

This removes the need for manual distribution or uploads.

---

## ⏱ Automation Options

- **Windows Task Scheduler**: Run the script automatically on a set schedule (e.g., weekly)
- **Remote Server**: The script can also be hosted on a Windows server with scheduled execution (no user login required)

---

## 📂 Repository Structure

```
nhs-vacancy-data-automation/
│
├── main.py                   # Core script that fetches and saves vacancy data
├── user_guide.md             # End-user documentation for replication
├── sample_output.csv         # Sample CSV for reference
├── requirements.txt          # Python dependencies
├── README.md                 # Overview and setup guide
├── LICENSE                   # MIT License (free to adapt and reuse)
```

---

## ✅ Benefits for NHS Teams

- Reduces the burden of manual vacancy tracking
- Gives consistent, comparable job data across providers
- Flexible for ICS-wide use, including providers that don’t use the same job boards as long as the data is captured on NHS jobs site
- Easily replicable by colleagues with minimal Python knowledge
- Offers a reliable alternative to RPA by using script-based automation

---

## 🧾 Licensing

This project is released under the MIT License – you are free to reuse, modify and distribute it with appropriate credit.

---

## 🙋🏽‍♂️ Author

**Temitope Akingbala**  
Feel free to contact me for collaboration or adaptation discussions

