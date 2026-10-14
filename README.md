# E-commerce Product Analysis

A Python notebook project that explores a retail product dataset and groups products using K-means clustering. The work covers missing-value handling, exploratory plots, feature scaling, and interpretation of product clusters.

The dataset contains **609 product records across seven categories**. This repository is an exploratory analysis project; it is separate from the e-commerce web application featured in my portfolio.

## Analysis workflow

1. Inspect the dataset shape, types, missing values, and duplicate rows.
2. Fill missing numeric values and gender labels, then remove records with remaining missing fields in the latest notebook.
3. Plot price and rating distributions, category counts, and gender counts.
4. Standardize `Original_price`, `price`, `perc_of_unit_sold`, and `rating` with `StandardScaler`.
5. Compare K-means inertia for one through ten clusters, then fit a four-cluster model with `random_state=42`.
6. Visualize cluster membership and calculate summaries such as mean price and rating.

## Repository guide

| File | Purpose |
| --- | --- |
| [`update_2_E_commerce_analysis.ipynb`](update_2_E_commerce_analysis.ipynb) | Most recent analysis: cleaning, exploratory plots, scaling, and clustering |
| [`project1update .ipynb`](project1update%20.ipynb) | Earlier version with additional distribution, outlier, and correlation exploration |
| [`Copy_of_E_commerce_analysis.ipynb`](Copy_of_E_commerce_analysis.ipynb) | Initial inspection and missing-value experiments |
| [`Datasets/combined_datasets.csv`](Datasets/combined_datasets.csv) | Combined product dataset used by the notebooks |
| [`Datasets/`](Datasets/) | Category-specific CSV files |
| [`Project DataSet.pdf`](Project%20DataSet.pdf) | Original dataset documentation |

The CSV fields include category, product, original price, listed price, percentage of units sold, rating, shipping eligibility, and gender. It also contains an exported row-index column.

## Run locally

The latest notebook records Python 3.11.3 in its kernel metadata. Required libraries are pandas, NumPy, Matplotlib, seaborn, and scikit-learn, plus Jupyter for interactive execution.

```bash
git clone https://github.com/mohamed6hani/E-commerce-anaylsis.git
cd E-commerce-anaylsis
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

```bash
python -m pip install jupyterlab pandas numpy matplotlib seaborn scikit-learn
python -m jupyter lab
```

Open `update_2_E_commerce_analysis.ipynb` from the repository root. For a portable input path, change its CSV-loading cell to:

```python
df = pd.read_csv("Datasets/combined_datasets.csv")
```

Run the cells in order. The repository does not pin library versions, and its saved outputs come from earlier executions; rerunning with a current environment may require compatibility adjustments.

## Interpretation and limitations

- Clusters describe similarity in the selected product attributes. They do not predict demand or establish causes of sales performance.
- The variable named `revenue_by_cluster` sums listed prices. It is **not measured revenue**, because transaction quantities and realized sales amounts are unavailable.
- Earlier notebooks reference an older `shpping_rate` column and a CSV path at the repository root. The committed dataset uses `Shipping Eligibility` inside `Datasets/`; start with the latest notebook.
- The earlier `project1update .ipynb` reuses the rating outlier threshold for price filtering. Treat that experiment as historical rather than a validated preprocessing method.
- Sampling is not seeded, K-means initialization count is not specified, and categorical label encodings should not be interpreted as numeric magnitudes. No clustering quality benchmark, automated tests, or fresh execution verification is included.

The next improvement is a reproducible environment, corrected preprocessing, explicit K-means initialization settings, and a comparison of cluster quality across candidate values of K.

