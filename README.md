# Amazon Sales Analytics Pipeline

A comprehensive data pipeline and analytics dashboard for processing and visualizing sales data. This project demonstrates end-to-end data engineering and business intelligence skills.

---

## Key Features

- **Data Standardization**: Cleans and transforms raw sales data
- **ETL Pipeline**: Automated extraction, transformation, and loading processes
- **Interactive Dashboard**: Streamlit-based analytics with Plotly visualizations
- **SQL Database Integration**: Simulated data warehouse loading

---

## 🛠️ Technical Stack

- **Python 3.14+**
- **Pandas** - Data processing and transformation
- **Streamlit** - Interactive web dashboard
- **Plotly** - Data visualization
- **SQLAlchemy** - Database operations
- **SQLite** - Data warehouse simulation

---

## 📁 Project Structure

```bash
ecommerce-sales-pipeline/
├── data/
│ ├── amazon.csv # Original dataset
│ └── standardized_sales.csv # Cleaned data
├── src/
│ ├── etl.py # Data cleaning and transformation
│ ├── load_to_db.py # Database integration
│ ├── dashboard.py # Streamlit analytics dashboard
│ └── main.py # Pipeline orchestrator
├── docs/ # Documentation and reports
├── requirements.txt # Project dependencies
└── README.md
```

### Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/amazon-sales-analytics.git
cd amazon-sales-analytics
```

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Prepare your data
Place your `amazon.csv` file in the `data/` directory.

Run the complete pipeline

```bash
python main.py
```

Launch the dashboard

```bash
streamlit run src/dashboard.py
```
