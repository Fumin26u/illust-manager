import sys, json, random
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Twitterのリンク
TWITTER_PATH = 'https://x.com/'

# ランダムな間隔(1~2秒)でタイムアウトを行う
def randomSleep():
    sleep(random.random() + 1)
    
# タグを取得
def getTag(
        parent,
        target, 
        getBy = By.CSS_SELECTOR, 
        waitForDisplay = False, 
        waitTime = 3
    ):
    try:
        if waitForDisplay:
            WebDriverWait(parent, waitTime).until(
                EC.visibility_of_element_located((getBy, target))
            )
        return parent.find_element(getBy, target)
    
    except NoSuchElementException:
        return None


# ドライバの設定
def setDriver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    options.add_argument('--user-agent=' + USER_AGENT)
    driver = webdriver.Chrome(options=options)
    
    return driver

# ドライバからTwitterにログイン
def twitterLogin(driver: webdriver, userId, password):
    initUrl = TWITTER_PATH + 'i/flow/login'
    driver.get(initUrl)
    
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


# ツイート情報の取得
def getTweet(driver: webdriver, query):
    randomSleep()
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
    
    while tweetRemains > 0:
        
        randomSleep()
        articles = driver.find_elements(By.TAG_NAME, 'article')
        
        print ('articles: ', len(articles))
        for article in articles:
            # ツイートの取得数上限に達した場合は取得を中断
            if tweetRemains == 0:
                return tweetInfo
            
            result = getTweetInfo(article, query)
            # 取得が中断された場合、その時点でツイート情報一覧を返す
            if result == False:
                return tweetInfo
            
            # ツイート内に画像が存在しない場合はスルー
            if result == 'continue':
                continue

            print("append tweet: ", result['images'])
            gotTweetIds.append(result['postID'])
            tweetInfo.append(result)
            tweetRemains -= 1
        
        # ウィンドウを現在表示されている画面の最下部までスクロール
        lastArticle = articles[-1]
        driver.execute_script("arguments[0].scrollIntoView();", lastArticle)

# 個々のツイート情報を取得
# ロードが完了したツイートのIDリスト
doneTweetList = []
def getTweetInfo(article, query):
    tweetInfo = dict()
    
    try:
        imageBlockSelector = '.css-175oi2r.r-16y2uox.r-1pi2tsx.r-13qz1uu'
        imageBlocks = article.find_elements(By.CSS_SELECTOR, imageBlockSelector)
    except NoSuchElementException:
        print('指定した要素が存在しません。')
        randomSleep()
        return 'continue'
        
    # 画像のURLからツイート元のURLを作成
    imagePaths = []
    for imageBlock in imageBlocks:   
        imageUrl = imageBlock.find_element(By.TAG_NAME, 'a').get_attribute('href')

        # ツイート元の相対URL
        tweetRelativePath = imageUrl[:(imageUrl.index('/photo/'))]
        
        # 相対URLの末尾がそのツイートのIDなのでそれを取得
        postID = tweetRelativePath.split('/')[-1]
        # 取得したツイートIDが既に取得済みの場合はスルー
        if postID in doneTweetList:
            print('既に取得済みのツイートです。')
            return 'continue'
        
        doneTweetList.append(postID)
        
        # 前回取得した画像以降を取得したい場合、この時点でツイートIDが前回取得した最後のツイートのIDだった場合falseを返してツイート取得終了
        if (
            query['isGetFromPreviousTweet'] and
            'suspendID' in query and
            postID == query['suspendID']
        ): 
            print('前回取得した画像です。')
            return False 
        
        tweetInfo['postID'] = postID
        tweetInfo['url'] = tweetRelativePath
        
        # 画像を取得
        image = imageBlock.find_element(By.TAG_NAME, 'img')
        imagePath = image.get_attribute('src')
        
        # 画像サイズをlargeに修正
        nameQueryIndex = imagePath.find('name=')
        if nameQueryIndex != -1:
            largeImagePath = imagePath[:nameQueryIndex] + 'name=large'
        else:
            largeImagePath = imagePath
        imagePaths.append(largeImagePath)
        
    tweetInfo['images'] = imagePaths
    randomSleep()
        
    # ユーザー名取得
    userBlockSelector = '.css-175oi2r.r-zl2h9q'
    userBlock = article.find_element(By.CSS_SELECTOR, userBlockSelector)
    
    # ユーザー名テキストを囲むspan共通のcssセレクタを利用しタグを取得
    # userBlockSpanSelector = '.css-1qaijid.r-dnmrzs.r-1udh08x.r-3s2u2q.r-bcqeeo.r-qvutc0.r-1tl8opc'
    userBlockSpanSelector = '.css-1jxf684.r-dnmrzs.r-1udh08x.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-1tl8opc'
    userBlockSpans = userBlock.find_elements(By.CSS_SELECTOR, userBlockSpanSelector)
    
    # 取得したspan要素の1番目がユーザー名
    tweetInfo['user'] = userBlockSpans[0].text

    # # ツイート内容を取得
    tweetInfo['text'] = '-'
    # 投稿日時はこの情報から取得できないのでnullに設定
    tweetInfo['post_time'] = None

    return tweetInfo
