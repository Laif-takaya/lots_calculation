# PythonでSeleniumのwebdriverモジュールをインポート
import re
from selenium import webdriver
import datetime
from time import sleep
# 1.操作するブラウザを開く
#WebDriverを格納しているディレクトリを指定
def highLow(date):
    currency_pair=date[:7]
    stop=date[0:2]
    up_down=date[-2:]

    driver = webdriver.Chrome()

    # 2.操作するページを開く
    driver.get('https://demotrade.highlow.com/')
    # 基本設定はここまで。↑は使い回し可能。ここから下は、やりたい動作によって増える
    sleep(2)
    # 3.操作する要素を指定
    # 4.その要素を操作する
    driver.find_element_by_link_text('クイックデモ').click()
    sleep(5)
    driver.find_element_by_link_text('取引を始める。').click()
    sleep(2)
    account_balance = driver.find_element_by_id("balance").text
    ab = int(re.sub("\\D", "", account_balance))
    ab=ab//10
    if ab>=200000:
        ab=200000

    driver.find_element_by_xpath('//*[@id="ChangingStrikeOOD"]').click()#Turbo
    driver.find_element_by_xpath('//*[@id="assetsCategoryFilterZoneRegion"]/div/div[5]/span').click()#5m
    if currency_pair=="USD/JPY":
        driver.find_element_by_xpath('//*[@id="3266"]').click() #USD/JPY
    elif currency_pair=="EUR/JPY":
        driver.find_element_by_xpath('//*[@id="3330"]').click() #EUR/JPY
    elif currency_pair=="EUR/USD":
        driver.find_element_by_xpath('//*[@id="3248"]/div[1]').click() #EUR/USD
    elif currency_pair=="AUD/JPY":
        driver.find_element_by_xpath('//*[@id="3284"]').click() #AUD/JPY
    elif currency_pair=="AUD/USD":
        driver.find_element_by_xpath('//*[@id="rightButton"]').click() #NEXT
        sleep(1)
        driver.find_element_by_xpath('//*[@id="3348"]').click() #AUD/USD
    elif currency_pair=="GBP/JPY":
        driver.find_element_by_xpath('//*[@id="3312"]').click() #GBP/JPY
    elif currency_pair=="NZD/JPY":
        driver.find_element_by_xpath('//*[@id="rightButton"]').click() #NEXT
        sleep(1)
        driver.find_element_by_xpath('//*[@id="3408"]').click() #NZD/JPY
    else:
        result ="通過ペアは存在しません"

    driver.execute_script("window.scrollTo(0, 400)")
    sleep(2)
    element = driver.find_element_by_id("amount")
    element.send_keys(ab)
    element.clear()
    element.send_keys(ab)
    if up_down=="ハイ":
        driver.find_element_by_xpath('//*[@id="up_button"]').click()#上ボタン
    elif up_down=="ロー":
        driver.find_element_by_xpath('//*[@id="down_button"]').click()#下ボタン
    else:
        result ="方向が取得できません"
    #5分単位のタイミングチェック
    dt = datetime.datetime.now()
    time = dt.minute
    while True:
        if time%5 == 0:
            break
        dt = datetime.datetime.now()
        time = dt.minute
        sleep(2)

    driver.find_element_by_xpath('//*[@id="invest_now_button"]').click()#購入ボタン
    #マーチン
    rate = driver.find_element_by_id("strike").text
    entry_time = datetime.datetime.now()
    judgment_time = entry_time + datetime.timedelta(minutes=5)
    while True:
        if entry_time >= judgment_time:
            judgment_rate = driver.find_element_by_id("strike").text
            break
        entry_time = datetime.datetime.now()
        time = dt.minute
        sleep(1)

    if rate > judgment_rate:
        driver.find_element_by_xpath('//*[@id="invest_now_button"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="invest_now_button"]').click()
        result ="マーチンしました"
    else:
        result ="かち"

    return result
