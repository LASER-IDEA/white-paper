# Low Altitude Economy Development Index (Quarto Framework)

This project is a refactored version of the Low Altitude Economy Development Index visualization framework, built using **Python** and **Quarto**. It addresses the need for high-quality GIS interactions (Web) and publication-quality PDF reports (Print).

## Features

- **Dual Output Support**:
  - **HTML**: Interactive charts using `Pyecharts` (ECharts).
  - **PDF**: High-resolution static vector graphics using `Matplotlib` and `Seaborn`.
- **Conditional Rendering**: Automatically switches chart engines based on the output format.
- **Modular Data Processing**: Data logic is separated in `data_processing.py`.

## Prerequisites

1. **Python 3.8+**: Ensure Python is installed.
2. **Quarto**: Download and install from [quarto.org](https://quarto.org/docs/get-started/).
3. **LaTeX (for PDF)**: Required for PDF generation.
   - If you don't have LaTeX installed, you can install TinyTeX via Quarto:
     ```bash
     quarto install tinytex
     ```

## Installation

1. Clone the repository and switch to the `quarto` branch.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Preview (Live Reload)
To preview the HTML report while editing:
```bash
quarto preview index.qmd
```

### 2. Render HTML (Interactive)
To generate the interactive web version:
```bash
quarto render index.qmd --to html
```
The output will be in `index.html` (or `_output` folder depending on config).

### 3. Render PDF (Print)
To generate the static white paper for printing:
```bash
quarto render index.qmd --to pdf
```
*Note: This requires a working LaTeX environment.*

## Project Structure

- `index.qmd`: Main Quarto document containing the report structure and conditional rendering logic.
- `data_processing.py`: Python module for mock data generation.
- `requirements.txt`: Python package dependencies.

## Customization

- **Data**: Modify `data_processing.py` to connect to your real data sources (CSV, Database, etc.).
- **Charts**: Edit the Python code chunks in `index.qmd`. You can customize `render_pyecharts` for HTML and the Matplotlib code for PDF.
