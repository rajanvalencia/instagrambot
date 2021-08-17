# -*- coding: utf-8 -*-
from decouple import config
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import time 

def main():
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://instagram.com")
    time.sleep(2)

    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.send_keys(config('USERNAME'))
    password.send_keys(config('PASSWORD'))

    # Submit
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)
    later_button = EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '後で')]"))
    WebDriverWait(driver, 10).until(later_button).click()
    WebDriverWait(driver, 10).until(later_button).click()

    total_likes = 0;

    hashtags = ["多言語", "多文化", "多文化共生", "多文化教育", "多文化交流",  "多様性", "日本語", "日本語学校", "日本語教師", "日本語勉強"]

    max_likes_per_hashtag = int(config('LIKE_LIMIT')) // len(hashtags)
    print('Max likes per hashtag: ', max_likes_per_hashtag)

    for hashtag in hashtags:
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(5)

        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        links = driver.find_elements_by_tag_name("a")
        links = [l.get_attribute("href") for l in links]
        links = [l for l in links if l.startswith("https://www.instagram.com/p/")]

        for link in links[:max_likes_per_hashtag]:
            try:
                driver.get(link)

                try:
                    like_post(driver)
                    total_likes +=  1
                except NoSuchElementException:
                    pass

                # comment_post(driver)
            
                if total_likes > int(config('LIKE_LIMIT')):
                    print('Limit reached')
                    print_and_close(driver, total_likes)

            except WebDriverException:
                print_and_close(driver, total_likes)

    print_and_close(driver, total_likes)


def like_post(driver):
    like_button = driver.find_element_by_xpath("//*[@aria-label='いいね！']")
    like_button.click()


def comment_post(driver):
    driver.find_element_by_tag_name("form").click()
    text_area = driver.find_element_by_tag_name("textarea")
    text_area.send_keys(config('COMMENT'))
    submit_button = EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    WebDriverWait(driver, 10).until(submit_button).click()


def print_and_close(driver, total_likes):
    print('Total likes: ', total_likes)
    time.sleep(2)
    driver.close()


if __name__ == "__main__":
    main()
