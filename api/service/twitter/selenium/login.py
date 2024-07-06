from api.service.twitter.selenium.tag import getTag
from api.utils.sleep import randomSleep

from selenium import webdriver
from selenium.webdriver.common.by import By

def login(driver: webdriver, userId, password, url):
    driver.get(url)
    
    # ユーザー名入力
    # ユーザー名入力のinput欄のclass"r-30o5oe"が表示されるまで待つ
    # 表示されたらinputを取得してユーザー名を挿入
    userInput = getTag(
        driver,
        'r-30o5oe',
        getBy = By.CLASS_NAME,
        waitForDisplay = True
    )
    userInput.send_keys(userId)
    randomSleep()
    
    # ボタンを取得
    passwordSendButton = getTag(
        driver, 
        '.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l',
    )
    passwordSendButton.click()

    # パスワード入力
    passwordInput = getTag(
        driver,
        '.r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7',
        waitForDisplay = True
    )
    randomSleep()
    passwordInput.send_keys(password)
    
    loginButton = getTag(
        driver, 
        '.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-19yznuf.r-64el8z.r-1fkl15p.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l'
    )
    randomSleep()
    loginButton.click()