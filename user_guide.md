# NHS Vacancy Data Automation – User Guide

This script is used weekly to automatically extract vacancy listings from NHS Jobs using the XML API and generate a CSV report for workforce planning. It has been developed for ICS-wide use and supports organisations regardless of whether they use Trac or other systems.

---

## 🔍 What This Does

1. **Data Retrieval:** Connects to the NHS Jobs API and pulls vacancy listings.
2. **Data Processing:** Filters based on a list of employer names (in `main.py`) to keep the data ICS-relevant.
3. **Reporting:** Generates a structured CSV report with role, salary, post date, close date, and more.
4. **Automation:** Can be scheduled via Task Scheduler. Output saved to a synced SharePoint folder.
5. **Notification (Optional):** Once the file syncs, a SharePoint alert or Power Automate workflow can notify recipients.

---

## 🧰 Setup Requirements

- Python 3.9+
- Libraries: `requests`, `pandas`
- Internet access to reach the NHS Jobs API

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

1. In `main.py`, check the `TARGET_EMPLOYERS` list and update it if needed.
2. Update the output directory path to match your machine or mapped network location (e.g., SharePoint sync path).
3. Optional: if you want to email the file after it's saved, use the `email_report.py` script.

---

## 🖥️ Running the Script

From command line or terminal:
```bash
python main.py
```

---

## ⏱️ Setting Up Scheduled Runs (Windows Task Scheduler)

1. Open Task Scheduler and create a new basic task.
2. Set the trigger to “Weekly” and pick your preferred day/time.
3. Set the action to “Start a Program” and browse to:
   ```
   C:\Path\To\python.exe
   ```
   and in arguments:
   ```
   C:\Path\To\main.py
   ```

4. Make sure the user account has access to the output directory and that Python is properly installed.

---

## 🔁 Integration with SharePoint/OneDrive

The script outputs directly to a folder synced with SharePoint via OneDrive. Once the file is generated, SharePoint’s built-in notification system (or Power Automate) can be used to trigger alerts or emails to stakeholders.

---

## 🔄 Updating the Script

As the NHS Jobs API may evolve, it's good practice to:
- Monitor if the XML structure changes
- Add or remove organisations as required
- Log output or errors in a `.log` file (for advanced setups)

---

## 📞 Support

If you need any clarification adapting this for your ICB or provider geography, or would like a walkthrough, contact:

**Temitope Akingbala**  
Principal Data Analyst – Strategic Workforce  
Nottingham & Nottinghamshire ICS
