# NHS Vacancy Data Automation

This repository provides a Python-based automation tool developed to streamline the collection of vacancy data from NHS Jobs and other public data sources, all via the NHS Jobs API. It was designed for Integrated Care Systems (ICS) and Trusts to reduce the time spent on manual gathering of job vacancy posts data from multiple websites, improve data consistency, and support workforce planning analysis. This is sometimes helpful as at any point in time there could be over 2000 jobs posted on the NHS Jobs site to scan through.

---

## 🔍 What It Does

- Automatically extracts vacancy data across selected NHS organisations
- Consolidates the data into a single structured CSV file
- (Optional) Sends the output via email to configured recipients
- Can be scheduled to run automatically via Task Scheduler or a Remote Server

---

## ⚙️ Setup Instructions

1. **Clone or download the repository**
2. Ensure Python 3.9+ is installed
3. Install the dependencies using:

```
pip install -r requirements.txt
```

4. Configure your parameters in `main.py` (such as the list of employer names and output directory)
5. Run `main.py` manually or schedule via Windows Task Scheduler

---

## 📂 Repository Structure

```
nhs-vacancy-data-automation/
│
├── scripts/
│   ├── main.py
│   └── email_report.py  # Optional
│
├── outputs/
│   └── sample_output.csv
│
├── docs/
│   └── user_guide.md
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## ✅ Benefits for NHS Teams

- Reduces repetitive admin work
- Standardises vacancy reporting across organisations
- Adaptable for wider ICS or regional use
- Demonstrates an alternative approach to RPA by using scripted process automation

---

## 🧾 Licensing

This project is released under the MIT License – you are free to reuse, modify and distribute with appropriate credit.

---

## 🙋🏽‍♂️ Author

**Temitope Akingbala**  
Principal Data Analyst – Strategic Workforce  
Nottingham & Nottinghamshire Integrated Care System  
Feel free to contact me for collaboration or adaptation within your ICS.
