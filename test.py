import requests

from lxml import html
from multiprocessing.pool import Pool
from xl import save_xl

# url_pattern = 'https://zhkh-service.ru/company/geo/moskovskaya-oblast/g-moskva/'
# urls = [url_pattern] + [f'{url_pattern}/page/{n}/' for n in range(2, 88)]


# def get_companies(url):
#     response = requests.get(url)

#     tree = html.fromstring(response.text)
#     return tree.xpath("//div[@class='w-grid-list']//a/@href")


# with Pool(20) as p:
#     companies = p.map(get_companies, urls)
# p.close()


# with open('companies.txt', 'w') as f:
#     for lines in companies:
#         f.writelines(line + '\n' for line in lines)


with open('companies.txt', 'r') as f:
    urls = f.readlines()


def get_company(url):
    company_name = '-'
    company_phone = '-'
    company_email = '-'
    company_address = '-'

    response = requests.get(url.strip())

    tree = html.fromstring(response.text)

    company_name = tree.xpath("//h1[@itemprop='headline']/text()")[0]

    top_3_fields = tree.xpath(
        "//div[@class='w-post-elm post_custom_field type_text company-param']")
    for div in top_3_fields:
        key = div.xpath('./span/text()')[0].strip()
        if key == 'Телефон':
            company_phone = div.xpath("./text()")[0]
        if key == 'Электронная почта':
            company_email = div.xpath("./a/text()")[0]
        if key == 'Фактический адрес':
            company_address = div.xpath("./a/text()")[0]
    return {
        "url": url,
        "name": company_name,
        "phone": company_phone,
        "email": company_email,
        "address": company_address
    }


with Pool(20) as p:
    company_data = p.map(get_company, urls)
p.close()

save_data = [list(company.values()) for company in company_data]

save_xl('ЖКХ.xlsx', save_data, [
    "url",
    "Компании и ТСЖ",
    "Телефон",
    "Электронная почта",
    "Фактический адрес",
])
