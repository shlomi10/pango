import pytest
import allure
import logging

from selenium.common import NoSuchElementException

from automation_framework.utilities.api_helpers import ApiHelper
from automation_framework.utilities.db_helpers import DatabaseHelper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

logging.basicConfig(filename="test_log.log", level=logging.INFO, format="%(asctime)s - %(message)s")

cities = ["London", "New York", "Tokyo", "Paris", "Berlin"]

city_ids = {
    "London": 2643743,
    "New York": 5128581,
    "Tokyo": 1850147,
    "Paris": 2988507,
    "Berlin": 2950159,
}

city_to_url = {
    "London": "https://www.timeanddate.com/weather/uk/london",
    "New York": "https://www.timeanddate.com/weather/usa/new-york",
    "Tokyo": "https://www.timeanddate.com/weather/japan/tokyo",
    "Paris": "https://www.timeanddate.com/weather/france/paris",
    "Berlin": "https://www.timeanddate.com/weather/germany/berlin",
}

@pytest.fixture(scope="module")
def api():
    return ApiHelper()

@pytest.fixture(scope="module")
def db():
    return DatabaseHelper()

@pytest.fixture(scope="function")
def cleanup_db(db):
    db.conn.execute("DELETE FROM weather_data")
    yield db
    db.conn.commit()

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@allure.feature("Temperature Comparison")
@allure.story("Adaptive website scraping")
def test_resilient_scraping(api, driver, city="London"):
    try:
        driver.get(city_to_url[city])
        temp_element = driver.find_element(By.CLASS_NAME, "h2")
        web_temp_text = temp_element.text.strip()
        if "°F" in web_temp_text:
            temp_f = float(web_temp_text.replace("°F", "").strip())
            temp = (temp_f - 32) * 5 / 9
        else:
            temp = float(web_temp_text.replace("°C", "").strip())
        logging.info(f"{city} website temperature: {temp}")
    except NoSuchElementException:
        logging.warning(f"Temperature element not found for {city}")
        temp = None

    assert temp is not None, f"{city}: Failed to extract temperature from site"

@allure.feature("Weather Data Insertion")
@allure.story("Insert API weather data into DB")
@pytest.mark.parametrize("city", cities)
def test_get_weather_data_and_insert_into_db(api, db, cleanup_db, city):
    logging.info(f"Testing API data insertion for city: {city}")
    with allure.step(f"Fetch weather data from API for {city}"):
        response = api.get_current_weather(city)
        data = response.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        logging.info(f"{city} API temp: {temp}, feels_like: {feels_like}")

    with allure.step("Insert data into database"):
        db.insert_weather_data(city, temp, feels_like)

    with allure.step("Verify inserted data matches API"):
        db_data = db.get_weather_data(city)
        logging.info(f"{city} DB data: {db_data}")
        assert db_data[1] == pytest.approx(temp, rel=0.01)
        assert db_data[2] == pytest.approx(feels_like, rel=0.01)

@allure.feature("Weather Data Insertion")
@allure.story("Insert weather data by City ID into DB")
@pytest.mark.parametrize("city, city_id", city_ids.items())
def test_weather_by_city_id(api, db, cleanup_db, city, city_id):
    logging.info(f"Testing city ID weather fetch for: {city} ({city_id})")
    with allure.step(f"Fetch weather by city ID {city_id} for {city}"):
        response = api.get_weather_by_city_id(city_id)
        data = response.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"] - 273.15
        logging.info(f"{city} API temp: {temp}, feels_like: {feels_like}")

    with allure.step("Insert data into database"):
        db.insert_weather_data(city, temp, feels_like)

    with allure.step("Verify inserted data matches API"):
        db_data = db.get_weather_data(city)
        logging.info(f"{city} DB data: {db_data}")
        assert db_data[1] == pytest.approx(temp, rel=0.01)
        assert db_data[2] == pytest.approx(feels_like, rel=0.01)

@allure.feature("Weather Reports")
@allure.story("Get city with highest average temperature")
def test_print_city_with_highest_avg_temp(db):
    with allure.step("Query city with highest average temp"):
        city, avg = db.get_city_with_highest_avg_temp()
        logging.info(f"Highest avg temp: {city} ({avg}°C)")
        allure.attach(f"{city} ({avg:.2f}°C)", name="Highest Avg Temp", attachment_type=allure.attachment_type.TEXT)
        print(f"\nCity with the highest average temperature: {city} ({avg:.2f}°C)")

@allure.feature("Temperature Comparison")
@allure.story("Compare API vs Website temperature")
@pytest.mark.parametrize("city", cities)
def test_compare_api_vs_website_temperature(api, driver, city):
    logging.info(f"Comparing API vs Website temperature for {city}")
    with allure.step(f"Get weather from OpenWeatherMap API for {city}"):
        api_response = api.get_current_weather(city)
        api_data = api_response.json()
        api_temp = api_data["main"]["temp"] - 273.15

    with allure.step(f"Open weather page for {city}"):
        url = city_to_url[city]
        driver.get(url)
        temp_element = driver.find_element(By.CLASS_NAME, "h2")
        web_temp_text = temp_element.text.strip()
        if "°F" in web_temp_text:
            temp_f = float(web_temp_text.replace("°F", "").strip())
            web_temp = (temp_f - 32) * 5 / 9
        else:
            web_temp = float(web_temp_text.replace("°C", "").strip())

    with allure.step("Log temperatures and compare"):
        logging.info(f"{city} - API: {api_temp:.2f}°C, Website: {web_temp:.2f}°C")
        print(f"\n{city} - API Temp: {api_temp}°C, Website Temp: {web_temp}°C")
        allure.attach(
            f"{city} - API Temp: {api_temp:.2f}°C, Website Temp: {web_temp:.2f}°C",
            name=f"{city} Temp Comparison",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Validate discrepancy is acceptable"):
        discrepancy = abs(api_temp - web_temp)
        logging.info(f"{city} discrepancy: {discrepancy:.2f}°C")
        assert discrepancy < 5.0, f"{city} temperature discrepancy too high: {discrepancy:.2f}°C"

@allure.feature("Historical Weather")
@allure.story("Store weather snapshot in history table")
@allure.title("Store historical weather data for city")
def test_store_historical_weather_data(api, db, city="London"):
    logging.info(f"Storing historical weather for {city}")
    with allure.step(f"Fetch weather data for {city}"):
        response = api.get_current_weather(city)
        data = response.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        logging.info(f"{city} temp: {temp}, feels_like: {feels_like}")

    with allure.step("Insert historical weather into DB"):
        db.insert_weather_history(city, temp, feels_like)