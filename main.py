import requests
from bs4 import BeautifulSoup

def scrape_laptops(url):
    laptop_list = []
    for page in range(1, 21):
        current_url = f"{url}?page={page}"
        response = requests.get(current_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            laptops = soup.select('.thumbnail')

            for laptop in laptops:
                product_url = laptop.select_one('a')['href']
                laptop_info = scrape_individual_laptop(f"https://webscraper.io{product_url}")
                laptop_list.append(laptop_info)

        else:
            print(f"Error: {response.status_code}")

    return laptop_list

def scrape_individual_laptop(url):
    response = requests.get(url)
    laptop_info = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.select_one('.title').text.strip()
        price = soup.select_one('.price').text.strip()
        description = soup.select_one('.description').text.strip()

        # Витягнення рейтингу
        review_count_element = soup.select_one('.review-count')
        review_count = review_count_element.text.strip().split(' ')[0]  # Отримання кількості відгуків
        rating_icons = review_count_element.select('.ws-icon.ws-icon-star')
        rating = len(rating_icons)

        laptop_info = {
            'Model name': title,
            'Price': price,
            'Description': description,
            'Review Count': review_count,
            'Rating': rating,
        }
    else:
        print(f"Error: {response.status_code}")

    return laptop_info

def save_list_info(laptop_list, filename='laptops.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for laptop in laptop_list:
            file.write(f"{laptop}\n")

if __name__ == "__main__":
    laptop_url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops'
    laptops_data = scrape_laptops(laptop_url)
    save_list_info(laptops_data)
