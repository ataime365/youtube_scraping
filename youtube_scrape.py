from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

youtube_url = 'https://www.youtube.com/feed/trending'

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

if __name__ == "__main__": 
    driver = get_driver()
    driver.maximize_window()
    driver.get(youtube_url)
    time.sleep(10)
    print(driver.title)

    container = driver.find_elements(By.TAG_NAME ,"ytd-video-renderer") #This was already 96
    Top_ten_list = []
    for cont in container[0:10]:
        title_tag = cont.find_element(By.ID, 'video-title')
        title = title_tag.get_attribute('title')
        url = title_tag.get_attribute('href')
        views = title_tag.get_attribute('aria-label').split(' ')[-2]
        thumbnail_tag = cont.find_element(By.TAG_NAME, 'img')
        thumbnail_url = thumbnail_tag.get_attribute('src')
        # chanel_div = cont.find_element(By.ID, 'channel-name') #This also works
        # channel = chanel_div.text
        des_tag = cont.find_element(By.ID, "description-text")
        des = des_tag.text
        
        channel_div = cont.find_element(By.ID, 'container') #Narrowing it down #This works
        channel = channel_div.find_element(By.TAG_NAME, 'a').text
        
        
        print(title, url, views, thumbnail_url, des, channel)
        data_dict = {'title':title, 'url': url, 'views':views, 'thumbnail_url':thumbnail_url, 'description':des, 'channel':channel}
        Top_ten_list.append(data_dict)
        
    # print(Top_ten_list)
    videos_df = pd.DataFrame(Top_ten_list)
    print(videos_df)
    videos_df.to_csv('trending.csv', index=False)
        
        
        
        
        
        