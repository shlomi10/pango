# 🌦️ Weather API Testing and Analysis Project

<div align="center">

**[Python 3.12](https://www.python.org/)** &nbsp;|&nbsp;
**[Pytest](https://docs.pytest.org/en/stable/)** &nbsp;|&nbsp;
**[Selenium](https://www.selenium.dev/)** &nbsp;|&nbsp;
**[Allure Reports](https://docs.qameta.io/allure/)** &nbsp;|&nbsp;
**[Docker Compose](https://docs.docker.com/compose/)**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Test_Framework-green.svg?style=for-the-badge&logo=pytest)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-Reports-orange.svg?style=for-the-badge&logo=allure)](https://docs.qameta.io/allure/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg?style=for-the-badge&logo=docker)](https://docs.docker.com/compose/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI/CD-blue?style=for-the-badge&logo=github-actions)](https://github.com/)

</div>

---

## 📚 Overview

This project performs end-to-end validation and comparison of weather data from [OpenWeatherMap](https://openweathermap.org/current) API against live website data from [timeanddate.com](https://www.timeanddate.com/weather/). It stores and analyzes temperature data using SQLite and generates detailed test reports using Allure.

---

## ✨ Features

- 🔄 Dynamic API requests using city names and IDs  
- 💾 SQLite storage with average and historical weather data  
- 🕵️ Selenium scraping of weather data from timeanddate.com  
- 📊 Data discrepancy validation between sources  
- 📦 Dockerized test execution with Allure UI  
- 🔐 Configurable via `config.ini`  
- 🧪 Integrated with GitHub Actions for CI/CD  

---

## 📁 Folder Structure

```
automation_framework/
├── config/
│   └── config.ini
├── utilities/
│   ├── api_helpers.py
│   └── db_helpers.py
├── tests/
│   └── test_openweather_api.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🧪 Test Scenarios

| Test Name                               | Purpose |
|----------------------------------------|---------|
| `test_get_weather_data_and_insert_into_db` | Get current weather from API and insert into DB |
| `test_weather_by_city_id`              | Use city ID to fetch weather and validate DB |
| `test_compare_api_vs_website_temperature` | Compare scraped vs API temperature values |
| `test_print_city_with_highest_avg_temp` | Output the city with the highest avg temp |
| `test_store_historical_weather_data`   | Log temperature snapshots in history table |

---

## ⚙️ Configuration

Create `automation_framework/config/config.ini`:

```ini
[API]
API_KEY = your_openweather_api_key_here

[DB]
DB_NAME = data.db
```

---

## 🐳 Docker Usage

### Build and Run

```bash
docker-compose up --build
```

### Stop and Clean

```bash
docker-compose down
```

### Run Tests Only

```bash
docker-compose run --rm weather-tests
```

---

## 🔎 Allure Report Access

Once tests run successfully, view the report at:

```
http://localhost:5050/projects/default/reports/latest/index.html
```

> Auto-regenerates every 3 seconds. Refresh if it’s blank initially.

---

## 🧠 Smart Features

- ✅ Dynamic test generation via `pytest.mark.parametrize`
- 🧠 Intelligent logging to `test_log.log`
- 📥 Automated data validation using `pytest.approx`
- 🧮 Average temperature and discrepancy calculations

---

## 🔁 GitHub Actions CI/CD

Easily integrate using `.github/workflows/test.yml` to:

- Run Docker tests on every commit or PR
- Publish Allure reports as artifacts

Example snippet:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker-compose up --build --abort-on-container-exit
```

---

## 🔍 Troubleshooting

| Problem | Solution |
|--------|----------|
| Report not visible | Refresh browser, restart `allure-ui` |
| Chrome/Selenium error | Ensure Linux containers are active |
| Config not loaded | Double-check `config.ini` path in Docker |

---

## 📜 License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

<div align="center">

## 📋 Quick Reference

| Action                               | Command |
|--------------------------------------|---------|
| **Clone the repo**                   | `git clone https://github.com/shlomi10/fastapi-order-management.git` |
| **Create virtual environment**       | `python -m venv venv` |
| **Activate environment (Windows)**   | `venv\Scripts\activate` |
| **Activate environment (Linux/Mac)** | `source venv/bin/activate` |
| **Install dependencies**             | `pip install -r requirements.txt` |
| **Start all services**               | `docker-compose up --build` |
| **Swagger**                          | `http://127.0.0.1:8000/docs#/` |
| **Stop services**                    | `docker-compose down` |
| **Run tests**                        | `pytest tests/ --alluredir=allure-results` |
| **Serve Allure report**              | `allure serve allure-results` |
| **View published reports**           | `https://shlomi10.github.io/fastapi-order-management/` |
| **Pull Docker image**                | `docker pull shlomi10/fastapi-order-management:latest` |

💡 Built for weather validation automation — fast, reproducible, and scalable.

</div>
