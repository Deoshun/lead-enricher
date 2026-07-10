# Lead Matcher & Enricher

A modular Python tool designed to automate lead generation workflows. This project takes a raw list of potential leads (e.g., from Google Places), evaluates and filters them using a **Weight of Evidence (WoE)** qualification model, and automatically crawls the web to enrich qualified candidates with contact emails, phone numbers, and social media links.



## 🚀 Features

*   **Smart Classification:** Uses a Laplace-smoothed Weight of Evidence (WoE) model to score and qualify leads based on industry or business types.
*   **Automated Enrichment:** Deep-crawls company websites up to configurable depths to extract emails, global phone numbers, and social profiles.
*   **Fallback Search Discovery:** Seamlessly uses search engine parsing to locate websites when a direct link isn't explicitly provided in the raw data.
*   **Flexible Data Pipelines:** Ingests raw leads from `.csv`, `.xls`, or `.ods` sheets and exports clean, structured categorization sets.
*   **Dual-mode UI:** Can run silently via backend configurations or interactively using a built-in step-by-step graphical folder picker.



## 📂 Project Architecture

```text
.
├── column_name_config.json   # Maps your unique source sheet headers to standard fields
├── config.json               # System behavioral thresholds and internal path rules
├── requirements.txt          # Python dependencies
├── src/
│   ├── main.py               # Application entry point
│   ├── data_exporter/        # Handles exporting clean structured datasets
│   ├── enrich/               # Core scraping, search fallbacks, and regex parsers
│   ├── lead/                 # Base object models and unified file importers
│   └── qualify/              # WoE optimization engines and mathematical processing
└── README.md

```


## 🛠️ Installation & Setup

1. **Clone the Repository**
```bash
git clone [https://github.com/Deoshun/lead-enricher.git](https://github.com/Deoshun/lead-enricher.git)
cd lead-enricher

```


2. **Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```



---

## ⚙️ Configuration Guide

### 1. Match Your File Headers (`column_name_config.json`)

Different lead lists use different column titles. Map your incoming file headers to the fields expected by the application:

```json
{
  "company_name": "your_sheet_name_column",
  "address": "your_sheet_address_column",
  "types": "your_sheet_industry_tags_column",
  "website": "your_sheet_url_column",
  "phone": "your_sheet_phone_column"
}

```

### 2. Configure System Logic (`config.json`)

Adjust the operational thresholds and lead directory path bindings:

```json
{
  "interactive": "False",
  "threshold": "0.6",
  "raw_leads_dir": "imports/leads/raw_leads",
  "example_qualified_leads_dir": "imports/leads/valid_examples",
  "example_unqualified_leads_dir": "imports/leads/invalid_examples"
}

```

*Set `"interactive": "True"` if you want a Tkinter folder pop-up GUI to manually select directories on run.*

---

## 📈 The Qualification Workflow (How it Works)

To automatically qualify your target `raw_leads`, the engine learns what a "good" or "bad" lead looks like using example training pools:

1. **The Training Set:** Drop ~50 target examples of ideal leads into your `valid_examples` directory, and ~50 poor-fit examples into `invalid_examples`.
2. **Mathematical Evaluation:** The system builds an analytical profiling grid based on the industry tags present in your training sets using a Weight of Evidence framework.
3. **Filtering:** Raw targets with composite scores hitting above your custom `"threshold"` are cleared for deep scraping; poor fits are exported cleanly to an unqualified registry without hitting your network bandwidth.

---

## 🖥️ Usage

Run the primary automation pipeline straight from the terminal root:

```bash
python src/main.py

```

### 📤 Output Sets

Once processing concludes, your generated matches will settle inside the `/exports` folder, sorted clean by contact availability:

* `with_email_output.csv` — Verified leads with an extracted email.
* `with_social_links_output.csv` — Leads missing direct emails but populated with verified social profiles.
* `with_number_output.csv` — Leads containing only validated telephone points.
* `unqualified_output.csv` — Raw targets that fell under your scoring qualification threshold.

---

## 🧮 Understanding the Qualification Engine (WoE Math)

To evaluate if an incoming business type is a good match, this tool implements a **Weight of Evidence (WoE)** framework commonly used in statistical credit scoring and classification tasks. 

### The Formula
For any given business type tag ($evidence$), the score is calculated as:

```text
                       % of Total Good Leads containing this tag
WoE = ln( ------------------------------------------------------------------- )
                       % of Total Bad Leads containing this tag
```

Which translates programmatically in `src/qualify/woe.py`.

### How to Interpret the Output:
*   **Positive Score ($> 0$):** The tag appears at a higher rate in your valid examples than your invalid examples. This tag actively pulls the lead *towards* being qualified.
*   **Negative Score ($< 0$):** The tag appears more frequently in your invalid examples. It acts as negative weight, signaling a poor match.
*   **Zero Score ($= 0$):** The tag is completely neutral or unseen, exerting no influence.

### Real-World Implementation in This Code
1.  **Calibration (`woe.py`):** When the application fires up, `BusinessTypeWOE` reads all categories inside your example folders. It applies **Laplace Smoothing** (initializing counts at `1` instead of `0`) to gracefully prevent math crashes like dividing by zero or taking the natural log ($\ln$) of zero.
2.  **Scoring (`qualifier.py`):** For a raw lead, the system sums up the individual WoE weights for all its tags ($\sum \text{WoE}$).
3.  **The Sigmoid Gate:** Because raw WoE sums can span anywhere from negative to positive infinity, the code passes the net weight through a **Sigmoid Activation Function**:

$$\text{Score} = \frac{1}{1 + e^{-x}}$$

This compresses the final outcome into a clean probability percentage between `0.0` and `1.0`. If that resulting percentage beats your configured threshold (e.g., `0.6`), the lead is passed forward for scraping!

🎥 **Deep Dive:** For a comprehensive, intuitive visual breakdown of how Weight of Evidence (WoE) and Information Value (IV) work mathematically, check out this excellent video guide: [Weight of Evidence & Information Value Explained](https://www.youtube.com/watch?v=98Zzr6PU19U).

## ⚖️ Legal & Compliance Disclaimer

This codebase contains generic web-scraping utilities. When configuring depth settings or running lead generation campaigns across open domains:

* Always verify that your operations comply with data privacy regulations like **GDPR**, **CCPA**, and local spam policies.
* This tool includes built-in compliance checks designed to respect remote domain `robots.txt` access permissions and delay rates natively. Please use responsibly.

