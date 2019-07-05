from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import json


options = webdriver.ChromeOptions()
options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"')
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 1)
KEYWORD = 'iPhone'
MAX_PAGE = 100

def index_page(page):
    print('正在爬取第', page, '页')
    try:
        url = 'https://search.jd.com/Search?keyword=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage span.p-skip > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage span.p-skip > .btn.btn-default')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage span.p-num > a.curr'), str(page)))
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.m-list #J_goodsList .gl-warp.clearfix .gl-item')))
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    html = browser.page_source
    doc = pq(html)
    items = doc('.m-list #J_goodsList .gl-warp.clearfix .gl-item').items()
    for item in items:
        product = {
        '图片': item.find('.p-img img[data-img="1"]').attr('src'),
        'price': item.find('.p-price i').text(),
        'product profile': item.find('.p-name.p-name-type-2 em').text(),
        'commit': item.find('.p-commit strong a').text(),
        'shop': item.find('.p-shop .J_im_icon a').text(),
        }
        print(product)
        save_products(product)


def save_products(product):
    with open('products.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(product, ensure_ascii=False) + '\n')


def main():
    for i in range(1, MAX_PAGE + 1):
        index_page(i)

if __name__ == '__main__':
    main()
