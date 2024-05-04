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
    return webdriver.Chrome('api/imagedler/fanbox/chromedriver', options=options)

# ドライバからTwitterにログイン
async def fanboxLogin(driver, userId, password):    
    # ログインボタンが表示されるまで待機
    # loginButtonDivClass = '.Header__WidthLargeOnly-sc-60utt6-4.MkeTl'
    # loginButtonDiv = driver.find_element(By.CSS_SELECTOR, loginButtonDivClass)
    
    loginButtonClass = '.ButtonBase-sc-1pize7g-0.CommonButton__CommonButtonOuter-sc-1s35wwu-0.iorEfw.flNDpw'
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, loginButtonClass)))
    loginButton = driver.find_elements(By.CSS_SELECTOR, loginButtonClass)[1]
    
    loginButton.click()
    
    # ユーザー名入力
    # 入力フォーム表示まで待機
    inputClass = '.sc-bn9ph6-6.kwyvbO'
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, inputClass)))
    
    # 表示されたらinputを取得してユーザー名を挿入
    inputs = driver.find_elements(By.CSS_SELECTOR, inputClass)
    await randomSleep()
    inputs[0].send_keys(userId)
    await randomSleep()
    inputs[1].send_keys(password)
    await randomSleep()
    
    # ログインボタンをクリック
    loginButtonClass = '.sc-bdnxRM.jvCTkj.sc-dlnjwi.klNrDe.sc-2o1uwj-10.jQmNGr.sc-2o1uwj-10.jQmNGr'
    loginButton = driver.find_element(By.CSS_SELECTOR, loginButtonClass)
    await randomSleep()
    loginButton.click()

# ツイート情報の取得
async def getImage(driver, url: str, userId, password):
    # url末尾が記事IDの場合その記事のみ、postsの場合すべての記事のイラストを取得
    urlParams = url.split('/')
    print(f'URL末尾: {urlParams[-1]}')
    isGetSingleArticles = urlParams[-1].isnumeric()
    
    print(f'IS GET SINGLE ARTICLES: {isGetSingleArticles}')
    driver.get(url)
    
    await randomSleep(2)
    await applyNsfw(driver)
    await randomSleep(5)
    
    # ログイン処理
    await fanboxLogin(driver, userId, password)
    
    await randomSleep()
    await applyNsfw(driver)
    await randomSleep(2)
    
    
    if isGetSingleArticles:
        print(f'GET SINGLE PAGE')
        
        # 見出しが表示されるまで待つ
        loadTags = '.PostDetailPage__Wrapper-sc-1f34f31-0.dogzhh'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, loadTags)))
        
        # 記事内の投稿画像のURLをすべて取得
        imagePaths = await getImagePaths(driver)
    elif urlParams[-1] == 'posts':
        print(f'GET MULTIPLE PAGE')
        
        # 全ての記事の画像を取得する場合
        imagePaths = []
        
        # 次の投稿ページが存在するか
        isExistNextPage = True
        while isExistNextPage:
            # 記事一覧が表示されるまで待つ
            loadTags = '.CreatorPostList__Wrapper-sc-1gerkjf-0.jZJlYv'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, loadTags)))
            await randomSleep()
            
            # 各記事のURLを取得
            articleCardTag = '.CardPostItem__Wrapper-sc-1bjj922-0.eGwQXQ'
            articleCards = driver.find_elements(By.CSS_SELECTOR, articleCardTag)
            
            for articleCard in articleCards:
                await randomSleep()
                # 記事本体に遷移
                articleCard.click()
                
                # 見出しが表示されるまで待つ
                loadTags = '.PostDetailPage__Wrapper-sc-1f34f31-0.dogzhh'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, loadTags)))
                
                # 画像URLを配列に追加
                imagePaths.extend(await getImagePaths(driver))
                await randomSleep()
                
                # 記事一覧ページにブラウザバック
                driver.back()
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, loadTags)))
                
            # ペジネーションを取得
            paginationDivClass = '.Pagination__Wrapper-sc-1oq4naf-0.bJbfKZ'
            paginationDiv = driver.find_element(By.CSS_SELECTOR, paginationDivClass)
            # ペジネーション内から現在のページを取得
            currentPageClass = '.Pagination__SelectedItemWrapper-sc-1oq4naf-3.fwOlpq'
            currentPage = paginationDiv.find_element(By.CSS_SELECTOR, currentPageClass)
            # 現在のページの次の要素を取得
            try:
                await randomSleep()
                nextPage = currentPage.find_element(By.CSS_SELECTOR, '+ div a').get_attribute('href')
                print(f'次のページに遷移します。現在の画像数: {len(imagePaths)}')
                nextPage.click()
            except NoSuchElementException:
                # 次のページが存在しない場合は、その時点でスクレイピング終了
                isExistNextPage = False
                print(f'次のページが存在しないので、スクレイピングを終了します。')
                break
    else:
        print(f'ERROR: URLが正しくありません。')
        return

    return imagePaths

async def applyNsfw(driver):
    # 年齢確認表示が出た場合の処理
    try: 
        displayNsfwClass = '.ButtonBase-sc-1pize7g-0.CommonButton__CommonButtonOuter-sc-1s35wwu-0.iorEfw.dhrsDw'
        displayNsfw = driver.find_element(By.CSS_SELECTOR, displayNsfwClass)
        displayNsfw.click()
        
    except NoSuchElementException:
        print(f'年齢確認無し')
        return
    

async def getImagePaths(driver):    
    await randomSleep()
    # 画像URLを含むaタグを取得
    try:
        imagePathTagClass = '.PostImage__Anchor-sc-xvj0xk-1.iWdaRc'
        imagePathTags = driver.find_elements(By.CSS_SELECTOR, imagePathTagClass)
        imagePaths = []
        print(f'add {len(imagePathTags)} URLs')
        for imagePathTag in imagePathTags:
            imagePaths.append(imagePathTag.get_attribute('href'))
    except NoSuchElementException:
        print(f'この記事には画像が含まれていないか、より多くの支援が必要です。')
        return []
                    
    return imagePaths
    
    