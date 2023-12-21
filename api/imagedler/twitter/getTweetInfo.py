import sys, json, random, asyncio
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Twitterのリンク
TWITTER_PATH = 'https://twitter.com/'

# ランダムな間隔(1~2秒)でタイムアウトを行う
async def randomSleep(num = 1):
    await asyncio.sleep(random.random() + num)
    
# ドライバの設定
def setDriver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    options.add_argument('--user-agent=' + USER_AGENT)
    return webdriver.Chrome('api/imagedler/twitter/chromedriver', options=options)

# ドライバからTwitterにログイン
async def twitterLogin(driver, userId, password):
    initUrl = TWITTER_PATH + 'i/flow/login'
    driver.get(initUrl)
    # ユーザー名入力
    # ユーザー名入力のinput欄のclass"r-30o5oe"が表示されるまで待つ
    inputClass = 'r-30o5oe'
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, inputClass)))
    # 表示されたらinputを取得してユーザー名を挿入
    userInput = driver.find_element(By.CLASS_NAME, inputClass)
    await randomSleep()
    userInput.send_keys(userId)
    # ボタンを取得
    # buttonSelector = '.css-18t94o4.css-1dbjc4n.r-sdzlij.r-1phboty.r-rs99b7.r-ywje51.r-usiww2.r-2yi16.r-1qi8awa.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr.r-13qz1uu'
    buttonSelector = '.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-usiww2.r-13qz1uu.r-2yi16.r-1qi8awa.r-ymttw5.r-o7ynqc.r-6416eg.r-1ny4l3l'
    passwordSendButton = driver.find_element(By.CSS_SELECTOR, buttonSelector)
    await randomSleep()
    passwordSendButton.click()

    # パスワード入力
    inputSelector = '.r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-1dz5y72.r-fdjqy7.r-13qz1uu'
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, inputSelector)))
    passwordInput = driver.find_element(By.CSS_SELECTOR, inputSelector)
    await randomSleep()
    passwordInput.send_keys(password)
    # buttonSelector = '.css-18t94o4.css-1dbjc4n.r-sdzlij.r-1phboty.r-rs99b7.r-19yznuf.r-64el8z.r-1ny4l3l.r-1dye5f7.r-o7ynqc.r-6416eg.r-lrvibr'
    buttonSelector = '.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-19yznuf.r-64el8z.r-1dye5f7.r-o7ynqc.r-6416eg.r-1ny4l3l'
    loginButton = driver.find_element(By.CSS_SELECTOR, buttonSelector)
    await randomSleep()
    loginButton.click()

# ツイート情報の取得
async def getTweet(driver, query):
    await randomSleep()
    # 初期リンク
    initUrl = TWITTER_PATH + query['twitterID']
    if query['getTweetType'] == 'liked_tweets':
        initUrl += '/likes'

    driver.get(initUrl)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'article')))

    # 必要なツイート情報を取得
    tweetInfo = []
    # 読み込んだツイートからツイート情報を取得する
    tweetRemains = int(query['getNumberOfTweet'])
    # 取得したツイートのID
    gotTweetIds = []
    # スクロールする位置
    scrollY = 4000
    while tweetRemains > 0:
        await randomSleep(2.5)
        articles = driver.find_elements(By.TAG_NAME, 'article')
        await randomSleep()
        for article in articles:
            # ツイートの取得数上限に達した場合は取得を中断
            if tweetRemains == 0:
                return tweetInfo
            result = await getTweetInfo(query, article)
            # 取得が中断された場合、その時点でツイート情報一覧を返す
            if result == False:
                return tweetInfo
            # ツイート内に画像が存在しない場合はスルー
            if result == 'continue':
                continue
            # スクロール処理後のツイート再取得時、既に取得しているツイートの場合は配列に挿入しない
            if result['postID'] in gotTweetIds:
                continue

            gotTweetIds.append(result['postID'])
            tweetInfo.append(result)
            tweetRemains -= 1
            # print(result['url'])
        
        # ウィンドウを現在表示されている画面の最下部までスクロール
        # articles[len(articles)-1].location_once_scrolled_into_view
        driver.execute_script(f"window.scrollTo(0, {scrollY});")
        scrollY += 4000

# 個々のツイート情報を取得
async def getTweetInfo(query, article):
    tweetInfo = dict()
    # 画像とツイート元リンクを取得 
    try:
        imageBlockSelector = '.css-175oi2r.r-1ssbvtb.r-1s2bzr4'
        imageBlock = article.find_element(By.CSS_SELECTOR, imageBlockSelector)
    except NoSuchElementException:
        # print('指定した要素が存在しません。')
        await randomSleep()
        return 'continue'
        
    # 画像のURLからツイート元のURLを作成
    imageUrl = imageBlock.find_element(By.TAG_NAME, 'a').get_attribute('href')
    # ツイート元の相対URL
    tweetRelativePath = imageUrl[:(imageUrl.index('/photo/'))]
    # 相対URLの末尾がそのツイートのIDなのでそれを取得
    postID = tweetRelativePath.split('/')[-1]
    # 前回取得した画像以降を取得したい場合、この時点でツイートIDが前回取得した最後のツイートのIDだった場合falseを返してツイート取得終了
    if (
        query['isGetFromPreviousTweet'] and
        'suspendID' in query and
        postID == query['suspendID']
    ): 
        # print('前回取得した画像です。')
        return False 
    tweetInfo['postID'] = postID
    tweetInfo['url'] = tweetRelativePath
    # 画像を取得
    images = imageBlock.find_elements(By.TAG_NAME, 'img')
    imagePaths = []
    for image in images:
        imagePath = image.get_attribute('src')
        # 画像サイズをlargeに修正
        nameQueryIndex = imagePath.find('name=')
        if nameQueryIndex != -1:
            largeImagePath = imagePath[:nameQueryIndex] + 'name=large'
        else:
            largeImagePath = imagePath
        imagePaths.append(largeImagePath)
    tweetInfo['images'] = imagePaths
    await randomSleep()
        
    # ユーザー名取得
    userBlockSelector = '.css-175oi2r.r-zl2h9q'
    userBlock = article.find_element(By.CSS_SELECTOR, userBlockSelector)
    # ユーザー名テキストを囲むspan共通のcssセレクタを利用しタグを取得
    userBlockSpanSelector = '.css-1qaijid.r-bcqeeo.r-qvutc0.r-1tl8opc'
    userBlockSpans = userBlock.find_elements(By.CSS_SELECTOR, userBlockSpanSelector)
    # 取得したspan要素の1番目がユーザー名
    tweetInfo['user'] = userBlockSpans[0].text

    # # ツイート内容を取得
    # tweetBlockSelector = '.css-901oao.r-vlxjld.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0'
    # try:
    #     tweetBlock = article.find_element(By.CSS_SELECTOR, tweetBlockSelector)
    #     # ツイートのテキストを囲むspan要素
    #     tweetSpan = tweetBlock.find_element(By.TAG_NAME, 'span')
    #     tweetInfo['text'] = tweetSpan.text
    # except NoSuchElementException:
    #     print('指定した要素が存在しません。(tweetText)')
    tweetInfo['text'] = '-'
    # 投稿日時はこの情報から取得できないのでnullに設定
    tweetInfo['post_time'] = None

    return tweetInfo