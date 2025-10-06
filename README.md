# 📊 Superstore Dashboard (Streamlit)

An interactive **Superstore Dashboard** built with **Streamlit**.
This app allows users to explore sales, profit, and customer data from the **Sample Superstore dataset**, with features such as **data download** and **email confirmation upon report export**.

---

## 🚀 Features

* **Interactive Filters**: Drill down by region, category, sub-category, and dates.
* **KPIs**: Quick glance at Sales, Profit, and Quantity Sold.
* **Charts**: Line, bar, and pie charts for visual exploration.
* **Download Data**: Export filtered data as CSV.
* **Email Confirmation**: Automatically sends a confirmation email when data is downloaded.
* **Logging**: All activities logged under `logs/` for tracking.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** – for dashboard UI
* **Pandas** – for data processing
* **Plotly / Matplotlib** – visualizations
* **smtplib / email.mime** – email confirmation
* **Power Query** – data cleaned before ingestion

---

## 📂 Project Structure

```
├── .devcontainer/             # Development container setup
├── logs/                      # Log files (download + app activity)
├── .gitignore                 # Git ignored files (e.g. credentials, streamlit config)
├── Sample - Superstore.xls    # Dataset
├── app.py                     # Main Streamlit application
├── ingestion.py               # Data ingestion and preprocessing logic
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## ⚙️ Setup & Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/superstore-dashboard.git
   cd superstore-dashboard
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure email credentials for confirmation mails.
   Add your details in environment variables or `.env` file:

   ```
   EMAIL_USER=your_email@example.com
   EMAIL_PASS=your_app_password
   ```

5. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

---

## 📸 Screenshots

*(Add dashboard screenshots and email confirmation screenshot here)*

---

## 📊 Example Use Cases

* Track top-performing categories and regions
* Monitor profitability trends
* Identify underperforming subcategories
* Export filtered reports and receive confirmation via email

---
