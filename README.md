# 🚁 Low Altitude Economy Development Index Dashboard

A comprehensive, dual-platform dashboard for analyzing and visualizing China's Low Altitude Economy (LAE) development metrics. This project combines **Streamlit (Python)** and **React (TypeScript)** implementations to provide interactive data exploration and professional reporting capabilities.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9+-3178C6.svg)](https://www.typescriptlang.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![ECharts](https://img.shields.io/badge/ECharts-5.4+-EE6666.svg)](https://echarts.apache.org/)

[![Deploy to GitHub Pages](https://github.com/LASER-IDEA/white-paper/actions/workflows/deploy.yml/badge.svg)](https://github.com/LASER-IDEA/white-paper/actions/workflows/deploy.yml)

## 🌟 Key Features

### 📊 Comprehensive Analytics Framework
- **5 Core Dimensions**: Scale, Structure, Space, Efficiency, Innovation
- **18 Key Metrics**: Flight operations, fleet composition, airspace utilization, and more
- **Time Series Analysis**: Calendar heatmaps, seasonal patterns, and trend analysis
- **Geographic Insights**: Regional distribution and spatial analysis

### 🤖 AI-Powered Analysis (Optional)
- **Intelligent Query Processing**: Natural language data exploration
- **Auto Model Selection**: Context-aware choice between `deepseek-chat` and `deepseek-reasoner`
- **Dynamic Visualization**: AI-generated charts based on user queries
- **Smart Insights**: Automated pattern recognition and trend analysis

### 🎨 Professional Visualizations
- **Interactive Charts**: Powered by ECharts for rich interactivity
- **Dual Implementation**: Consistent experience across Python and TypeScript
- **Responsive Design**: Optimized for desktop and mobile viewing
- **Export Capabilities**: PDF generation and data export features

## 🏗️ Project Structure

```
white-paper/
├── python/                    # Python Streamlit Application
│   ├── src/
│   │   ├── app.py            # Main Streamlit application
│   │   ├── charts.py         # ECharts visualization library
│   │   ├── data_factory.py   # Mock data generation
│   │   ├── data_processor.py # Data processing utilities
│   │   ├── llm_helper.py     # AI integration module
│   │   └── utils/
│   │       └── generate_mock_csv.py
│   ├── data/                 # Sample datasets
│   │   ├── sample_flight_data.csv
│   │   └── shenzhen.json
│   └── tests/                # Unit tests
│       └── test.py
├── web/                      # TypeScript React Application
│   ├── src/
│   │   ├── components/
│   │   │   ├── charts/
│   │   │   │   └── Charts.tsx
│   │   │   └── ReportPage.tsx
│   │   ├── utils/
│   │   │   └── mockData.ts
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── types.ts
│   ├── public/
│   │   └── data/
│   │       └── shenzhen.json
│   ├── test/                 # HTML test files
│   │   ├── geo_guangdong.html
│   │   └── geo_lines.html
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs/                     # Documentation and Assets
│   ├── pdf/                  # White papers and reports
│   │   ├── Low-Altitude Economy White Paper.pdf
│   │   └── 白皮书.pdf
│   └── figures/              # Generated chart exports
│       └── index_files/
│           └── figure-pdf/
├── config/                   # Configuration Files
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment template
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Python Streamlit Version

#### Prerequisites
- Python 3.8 or higher
- pip package manager

#### Installation
```bash
# Clone repository
git clone <repository-url>
cd white-paper

# Install Python dependencies
pip install -r config/requirements.txt
```

#### AI Setup (Optional)
```bash
# Copy environment template
cp config/.env.example .env

# Edit .env file with your DeepSeek API key
# DEEPSEEK_API_KEY=your_actual_api_key_here
```

#### Running the Application
```bash
# Navigate to Python app directory
cd python

# Run Streamlit app
streamlit run src/app.py
```

### TypeScript React Version

#### Prerequisites
- Node.js 16 or higher
- npm or yarn package manager

#### Installation
```bash
# Navigate to web app directory
cd web

# Install dependencies
npm install
# or
yarn install
```

#### Running the Application
```bash
# Start development server
npm run dev
# or
yarn dev
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `config/.env.example`):

```bash
# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# Model Selection (auto-selected based on query complexity)
DEEPSEEK_CHAT_MODEL=deepseek-chat
DEEPSEEK_REASONER_MODEL=deepseek-reasoner
```

### API Key Security
- 🔐 API keys are stored securely in `.env` files (ignored by Git)
- 🔐 Keys are never displayed in the UI interface
- 🔐 Environment variables are loaded automatically
- ⚠️ Never commit real API keys to version control

## 📈 Data Dimensions & Metrics

### 1. Scale & Growth 📈
- **Traffic Volume**: Daily/weekly flight operations
- **Market Size**: Economic indicators and growth metrics
- **Demand Patterns**: Seasonal and temporal analysis

### 2. Structure & Entity 🏗️
- **Fleet Composition**: Aircraft types and distribution
- **Entity Analysis**: Market participant segmentation
- **Operational Networks**: Route and connectivity patterns

### 3. Space & Geography 🗺️
- **Airspace Utilization**: Geographic coverage analysis
- **Regional Distribution**: Provincial and municipal metrics
- **Infrastructure Mapping**: Airport and facility networks

### 4. Efficiency & Quality ⚡
- **Operational Metrics**: Performance and reliability indicators
- **Quality Standards**: Safety and service quality measures
- **Resource Optimization**: Capacity and utilization analysis

### 5. Innovation & Integration 🚀
- **Technology Adoption**: Emerging tech integration
- **Regulatory Framework**: Policy and compliance metrics
- **Market Integration**: Cross-sector collaboration indicators

## 🤖 AI Features

### Intelligent Analysis
- **Natural Language Queries**: Ask questions in plain English
- **Contextual Understanding**: AI interprets data relationships
- **Automated Insights**: Pattern recognition and trend analysis

### Smart Model Selection
- **Simple Queries** → `deepseek-chat`: Fast responses for basic analysis
- **Complex Analysis** → `deepseek-reasoner`: Deep reasoning for complex queries

### Dynamic Visualization
- **Chart Generation**: AI creates appropriate visualizations
- **Data Exploration**: Interactive chart recommendations
- **Custom Analysis**: Tailored insights based on user needs

## 🛠️ Development

### Python Development
```bash
# Install development dependencies
pip install -r config/requirements.txt

# Run tests
cd python && python -m pytest tests/

# Format code
black src/ tests/
```

### TypeScript Development
```bash
# Install dependencies
cd web && npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

## 📚 Documentation

- **[Technical White Paper](docs/pdf/Low-Altitude%20Economy%20White%20Paper.pdf)**: Comprehensive analysis framework
- **[中文白皮书](docs/pdf/白皮书.pdf)**: Chinese version of the technical documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ECharts**: Powerful charting library for interactive visualizations
- **Streamlit**: Framework for building data applications
- **DeepSeek**: AI models for intelligent data analysis
- **Vite**: Fast build tool for modern web applications

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team.

## 贡献者

<!-- readme: collaborators,contributors -start -->
<table>
	<tbody>
		<tr>
            <td align="center">
                <a href="https://github.com/stevedegit">
                    <img src="https://avatars.githubusercontent.com/u/30927032?v=4" width="100;" alt="stevedegit"/>
                    <br />
                    <sub><b>stevedegit</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/sallychenhk">
                    <img src="https://avatars.githubusercontent.com/u/199864563?v=4" width="100;" alt="sallychenhk"/>
                    <br />
                    <sub><b>S.C</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/sunshuo0410-del">
                    <img src="https://avatars.githubusercontent.com/u/225815183?v=4" width="100;" alt="sunshuo0410-del"/>
                    <br />
                    <sub><b>sunshuo0410-del</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/zzzhangllei">
                    <img src="https://avatars.githubusercontent.com/u/254819203?v=4" width="100;" alt="zzzhangllei"/>
                    <br />
                    <sub><b>zzzhangllei</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/xiahaa">
                    <img src="https://avatars.githubusercontent.com/u/36867143?v=4" width="100;" alt="xiahaa"/>
                    <br />
                    <sub><b>estimation</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/hux062303">
                    <img src="https://avatars.githubusercontent.com/u/7478889?v=4" width="100;" alt="hux062303"/>
                    <br />
                    <sub><b>hux062303</b></sub>
                </a>
            </td>
		</tr>
	<tbody>
</table>
<!-- readme: collaborators,contributors -end -->

---

## Star History

<picture>
  <source
    media="(prefers-color-scheme: dark)"
    srcset="
      https://api.star-history.com/svg?repos=LASER-IDEA/white-paper&type=Date&theme=dark
    "
  />
  <source
    media="(prefers-color-scheme: light)"
    srcset="
      https://api.star-history.com/svg?repos=LASER-IDEA/white-paper&type=Date
    "
  />
  <img
    alt="Star History Chart"
    src="https://api.star-history.com/svg?repos=LASER-IDEA/white-paper&type=Date"
  />
</picture>

---

**🏢 Low Altitude Economy Research Institute** | **📊 Data-Driven Insights for Aviation Innovation**
