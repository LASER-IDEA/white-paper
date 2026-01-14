# Low Altitude Economy Development Index (Streamlit Framework)

This project provides a comprehensive dashboard for visualizing the Low Altitude Economy Development Index using **Streamlit** and **ECharts**.

## Features

- **5 Dimensions Analysis**: Scale, Structure, Space, Efficiency, Innovation.
- **18 Interactive Metrics**: Visualized using ECharts for high interactivity.
- **Mock Data Generation**: Built-in data factory for testing and development.

## Prerequisites

- Python 3.8+
- Pip

## Installation

1. Clone the repository and switch to the `streamlit-implementation` branch.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## AI Configuration (Optional)

The application includes AI-powered data analysis features using DeepSeek models.

### Setup API Key

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   # Replace with your actual DeepSeek API key
   DEEPSEEK_API_KEY=your_actual_deepseek_api_key_here
   ```

3. **Get API Key:**
   - Visit [DeepSeek Platform](https://platform.deepseek.com/)
   - Create an account and get your API key
   - Replace `your_actual_deepseek_api_key_here` with your real key

### Security Notes
- 🔒 The `.env` file is automatically ignored by Git
- 🔒 API keys are never displayed in the UI
- 🔒 Never commit real API keys to version control
- 🔒 Use the `.env.example` file as a template

### AI Features
- **Auto Model Selection**: `deepseek-chat` for simple tasks, `deepseek-reasoner` for complex analysis
- **Intelligent Analysis**: Ask questions about the data and get AI-powered insights
- **Chart Generation**: AI can suggest and create new visualizations based on your queries

## Usage


Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

## Project Structure

- `streamlit_app.py`: Main application entry point defining the layout.
- `charts_lib.py`: Library of ECharts visualization components.
- `data_factory.py`: Module for generating mock data.
- `requirements.txt`: Python dependencies.


# Nodejs version

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`


## reference
https://github.com/mikedeng/city_geojson/tree/master
https://echarts.streamlit.app/