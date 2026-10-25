# Seat Allocation Analysis Portal for Indian Universities/Colleges 

A data analysis portal for exploring JoSAA opening and closing rank trends.

## Features

- Rank-based IIT and branch prediction
- Institute-wise cutoff comparison
- Branch-wise trend analysis
- Category-wise cutoff comparison
- Gender-wise cutoff comparison
- Filtered data export as CSV
- Interactive charts and tables

## Tech Stack

- Python
- MySQL
- Pandas
- NumPy
- Streamlit
- Plotly

## Dataset

The project uses JoSAA opening and closing rank data from 2021–2024.

## Database Schema

Main table: `seat_allotment`

Columns:

- year
- round_no
- institute
- academic_program
- quota
- seat_type
- gender
- opening_rank
- closing_rank

## How to Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts/clean_data.py
python scripts/load_to_mysql.py
streamlit run app.py
