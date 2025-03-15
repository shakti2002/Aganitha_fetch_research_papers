# PubMed Paper Fetcher

##  Overview

This project allows users to fetch research papers from **PubMed** using its API. The retrieved papers can be stored in a CSV file for further analysis.

## Project Structure

```
D:\pubmed_project\
│── pubmed_paper_fetcher\         # Project root
│   ├── pubmed_paper_fetcher\     # Main package directory
│   │   ├── __init__.py           # Marks the directory as a Python package
│   │   ├── main.py               # Main script for fetching PubMed papers
│   ├── tests\                    # (Optional) Directory for unit tests
│   │   ├── __init__.py           
│   ├── pyproject.toml             # Poetry config file
│   ├── poetry.lock                # Poetry lock file (auto-generated)
│   ├── README.md                  # Documentation
│   ├── .gitignore                 # Ignore unnecessary files (if using Git)
│   ├── .env                       # Environment variables file (contains API key)
│   ├── papers.csv                 # Output file with fetched papers
```

## Installation & Setup

### 1. Install **Poetry** (Dependency Manager)

Poetry is used to manage dependencies. If you don’t have it installed, run:

```bash
pip install poetry
```

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/pubmed_paper_fetcher.git
cd pubmed_paper_fetcher
```

### 3️. Install Dependencies

```bash
poetry install
```

### 4️. Set Up Environment Variables

Create a `.env` file in the **project root** (`D:\pubmed_project\`) and add your **PubMed API Key**:

```ini
PUBMED_API_KEY=your_pubmed_api_key_here
```

##  Running the Program

### Fetching Papers

To fetch papers related to **deep learning in pharma** and save them as `papers.csv`, run:

```bash
poetry run python pubmed_paper_fetcher/main.py --query "deep learning in pharma" --output papers.csv
```

##  How the Code Works

1. **Load Environment Variables**
   - The script reads `.env` to get the **PubMed API Key**.
2. **Make API Request to PubMed**
   - The script queries PubMed using **Entrez API** to get relevant papers.
3. **Fetch Paper Details**
   - Retrieves paper details like **title, authors, and publication date**.
4. **Save Results in CSV**
   - The data is stored in `papers.csv`.

##  Tools & Libraries Used

- **[Python](https://www.python.org/)** (Core language)
- **[Poetry](https://python-poetry.org/)** (Dependency management)
- **[Requests](https://docs.python-requests.org/en/latest/)** (HTTP requests to PubMed API)
- **[pandas](https://pandas.pydata.org/)** (Data handling and CSV export)
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** (Load API key from `.env` file)
- **[PubMed Entrez API](https://www.ncbi.nlm.nih.gov/books/NBK25501/)** (Used for fetching research papers)

## Additional Commands

### Running Tests

To test the code using `pytest`, run:

```bash
poetry run pytest tests/
```

### Formatting Code

```bash
poetry run black pubmed_paper_fetcher/
```






