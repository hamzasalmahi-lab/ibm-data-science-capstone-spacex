# IBM Applied Data Science Capstone — SpaceX Falcon 9 Landing Prediction

Predicting whether the first stage of a SpaceX Falcon 9 rocket will land
successfully, using publicly available launch records.

**Author:** Hamza S. Almahi, MBBS
**Course:** [IBM Applied Data Science Capstone](https://www.coursera.org/learn/applied-data-science-capstone) (Coursera)
**Final deliverable:** [`presentation/SpaceX_Capstone_Report.pdf`](presentation/SpaceX_Capstone_Report.pdf)

---

## Why this matters

SpaceX advertises a Falcon 9 launch at roughly **$62M**, while comparable launches
from other providers cost upwards of **$165M**. The difference is driven almost
entirely by reusing the first stage. If we can predict whether the first stage
will land successfully — given the site, payload, orbit, booster version, and
flight history — we have a direct way to estimate the marginal cost of any
given launch. That's commercially useful for anyone bidding against SpaceX.

---

## Repository structure

```
.
├── notebooks/
│   ├── 01_data_collection_api.ipynb           # Pull launches from the SpaceX REST API
│   ├── 02_data_collection_webscraping.ipynb   # Scrape Wikipedia Falcon 9 launch table
│   ├── 03_data_wrangling.ipynb                # Clean data + engineer landing-outcome label
│   ├── 04_eda_visualization.ipynb             # Pandas / matplotlib / seaborn EDA
│   ├── 05_eda_sql.ipynb                       # SQLite queries over the cleaned dataset
│   ├── 06_interactive_visual_folium.ipynb     # Folium launch-site maps
│   └── 07_predictive_analysis.ipynb           # 4-classifier comparison + GridSearchCV
├── app/
│   └── spacex_dash_app.py                     # Plotly Dash launch-records dashboard
├── data/                                      # Cleaned CSVs (dataset_part_1.csv, etc.)
├── results/                                   # Generated figures, confusion matrix, etc.
└── presentation/
    └── SpaceX_Capstone_Report.pdf             # Final slide deck (35 slides)
```

---

## Methodology

1. **Data collection** — SpaceX REST API (`api.spacexdata.com/v4/launches/past`)
   joined with helper endpoints for rocket / payload / launchpad / cores;
   supplemented by scraping the Wikipedia *List of Falcon 9 and Falcon Heavy
   launches* page with BeautifulSoup.
2. **Data wrangling** — null inspection, mean-imputation of `PayloadMass`,
   per-site and per-orbit counts, and engineering of the binary landing-outcome
   `Class` label (1 = booster landed, 0 = did not).
3. **EDA** — visual exploration in pandas/matplotlib/seaborn and ten SQL
   queries against the cleaned dataset in SQLite.
4. **Interactive analytics** — Folium maps of all four launch sites with
   `MarkerCluster`, outcome icons, and proximity overlays; Plotly Dash app
   with a site dropdown, payload range slider, success pie chart, and
   payload-vs-outcome scatter.
5. **Predictive analysis** — Logistic Regression, SVM, Decision Tree, and KNN,
   all tuned with `GridSearchCV` (10-fold CV) and evaluated on a held-out
   20% test split.

---

## Headline results

| Model               | CV / training | Test  |
|:--------------------|:-------------:|:-----:|
| Logistic Regression | 0.8464        | 0.8333 |
| SVM                 | 0.8482        | 0.8333 |
| **Decision Tree**   | **0.8893**    | **0.8889** |
| KNN                 | 0.8482        | 0.8333 |

**Best model: Decision Tree — 88.9% test accuracy** (recall on the "Landed"
class = 100%, recall on "Did not land" = 50%).

Key findings from the EDA:

- **KSC LC-39A** is the most successful launch site (highest success share).
- **ES-L1**, **GEO**, **HEO**, and **SSO** orbits show 100% landing success in
  the dataset.
- Annual landing success has climbed from **0% (2010 – 2013)** to **~84% (2020)**.
- Heavier payloads correlate with lower landing success — a direct cost lever.

---

## Tech stack

- Python 3.x, Jupyter
- pandas, numpy, requests, BeautifulSoup4
- matplotlib, seaborn, plotly, folium
- scikit-learn (Logistic Regression, SVM, Decision Tree, KNN, GridSearchCV)
- Plotly Dash
- SQLite via `ipython-sql`

---

## Quick start

```bash
git clone https://github.com/hamzasalmahi-lab/ibm-data-science-capstone-spacex.git
cd ibm-data-science-capstone-spacex
pip install -r requirements.txt
jupyter lab notebooks/
```

The Dash app can be launched separately:

```bash
python app/spacex_dash_app.py   # then visit http://127.0.0.1:8050
```

---

## License

MIT — see `LICENSE`.
