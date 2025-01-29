from api.utils.sleep import randomSleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ツイート情報の取得
def getTweet(driver: webdriver, query, latestGetTweets, url):
    randomSleep()
    # 初期リンク
    initUrl = url

    driver.get(initUrl)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'article')))

    # 必要なツイート情報を取得
    tweetInfo = []
    
    # 読み込んだツイートからツイート情報を取得する
    tweetRemains = int(query['getNumberOfPost'])
    
    # 取得したツイートのID
    gotTweetIds = []
    
    while tweetRemains > 0:
        print('tweetRemains: ', tweetRemains)
        randomSleep()
        articles = driver.find_elements(By.TAG_NAME, 'article')
        
        print ('articles: ', len(articles))
        for article in articles:
            # ツイートの取得数上限に達した場合は取得を中断
            if tweetRemains == 0:
                print('ツイートの取得数上限に達しました。')
                return tweetInfo
            
            result = __getTweetInfo(article, query, latestGetTweets)
            # 取得が中断された場合、その時点でツイート情報一覧を返す
            if result == False:
                return tweetInfo
            
            # ツイート内に画像が存在しない場合はスルー
            if result == 'continue':
                continue

            gotTweetIds.append(result['id'])
            tweetInfo.append(result)
            tweetRemains -= 1
        
        # ウィンドウを現在表示されている画面の最下部までスクロール
        lastArticle = articles[-1]
        driver.execute_script("arguments[0].scrollIntoView();", lastArticle)

# 個々のツイート情報を取得
# ロードが完了したツイートのIDリスト
doneTweetList = []
def __getTweetInfo(article, query, latestGetTweets):
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
        
        # 前回取得した画像以降を取得したい場合、
        # この時点でツイートIDが前回取得したツイートのID一覧に含まれていた場合、
        # falseを返してツイート取得終了
        print("append Post: " + postID)
        if (
            query['isGetFromPreviousPost'] and
            postID in latestGetTweets
        ): 
            print('前回取得した画像です。')
            return False 
        
        tweetInfo['id'] = postID
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
    tweetInfo['created_at'] = None

    return tweetInfo
