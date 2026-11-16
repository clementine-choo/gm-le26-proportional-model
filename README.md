# Greater Manchester's LE26 Prediction Model

**Author:** Clementine Choo  


--

## Project Overview

This is an interactive tool that projects the 2026 Local Elections results in Greater Manchester using a proportional model. It assumes that each party's votes will swing proportionally across Greater Manchester and predicts the number of councillors won by each party as a result. 

---

## Repository Structure

```
gm-le26-proportional-model/
│
├── Assets/                          # Screenshots and visual outputs from the analysis
│   ├── Figure_1.png
│   └── Figure_2.png
│
├── Dataset/
│   ├── WD_DEC_24_UK_BGC.shp/        # Shape file for each ward in the UK
│   └──  GM LE24 result.csv/         # Pre-model assumption of 2024 results
│ 
├── Scripts/                         # Python scripts used to create the interactive model
│   └── le26_prediction.py
│
├── LICENSE                          # MIT License
├── README.md                        # Project overview and documentation
└── requirements.txt                 # Python dependencies
```

---

## Analysis approach

### Step 1: Defining baseline
A baseline is defined for each party in each ward. For every party but Reform, I used the exact results from the 2024 local elections for each ward. Reform are treated differently because they did not stand in the local election, so instead I used the projected votes they receieved in each ward in the 2024 general election.

### Step 2: Choose a proportional swing for each party
Each party gets a multipler, so if we choose 2.0 for the Green Party, we assume that the Green Party will receive 2.0 times the votes they received at the baseline in each ward. The default values are:

| Party                            | Default Value                                |
|----------------------------------|----------------------------------------------|
| Labour           | 0.65       |
| Conservative              | 0.8                        |
| Lib Dem         | 1.0             |
| Green    | 2.0             |
| Reform                | 2.0     |
| Workers Party and Others         | 1.2                          |

### Step 3: Pick a winner in each ward

### Step 4: Aggregate across Greater Manchester and calculate the statistics

### Step 5: Add sliders to create interactivity

### Caveat: The "Councillors Count" metric looks at the number of councillors won by each party within the ones that are up for election and does not include those that are not up for election. 

---

## Key Findings

Since the 2026 local elections have already passed, we can compare the model to actual results

| Party          | Actual Proportional Swing    | Predicted Councillor Count | Actual Councillor Count    |
|----------------------------------|----------------------------------------------|
| Labour           | 0.67       | 35 | 34 |
| Conservative              | 0.75               | 7 | 11 |
| Lib Dem         | 0.99    | 21 | 19 |
| Green    | 2.32   | 31 | 30 |
| Reform                | 2.05     | 106 | 105 |
| Workers Party and Others         | 0.84          | 16 | 15 |

Across 216 wards, the average error for each party is 1.6 ward, which shows that a proportional projection model is remarkably accurate at predicting ward-level results.

## Technologies Used

- **Python**
- **Pandas**
- **NumPy**
- **GeoPandas**
- **MatPlotLib**
