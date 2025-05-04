FROM seleniarm/standalone-chromium:120.0

USER root

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt .
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

CMD ["pytest", "--alluredir=allure-results"]
