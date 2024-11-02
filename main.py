import requests
from bs4 import BeautifulSoup
import json

# URL для первой страницы
base_url = "http://quotes.toscrape.com"
page_url = "/page/1"
all_quotes = []

num_pages = int(input("Введите количество страниц для скрапинга: "))
current_page = 1

while page_url and current_page <= num_pages:
    print(f"Сбор данных с страницы {current_page}")

    # HTML-код текущей страницы
    response = requests.get(base_url + page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Все элементы с цитатами
    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        # Извлечение текста, автора и тегов
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

        # Сохранение данных в виде словаря
        all_quotes.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    next_button = soup.find("li", class_="next")
    page_url = next_button.find("a")["href"] if next_button else None
    current_page += 1

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=4)

print(f"Сбор данных завершен. Результаты сохранены в data.json. Обработано страниц: {min(num_pages, current_page - 1)}")
