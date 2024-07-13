import os, sys, asyncio
from time import sleep
# pixivpy: pixivからデータを抽出するAPI
from pixivpy3 import *
from api.driver.connectPixivpyApi import connect_pixivpy_api

# 画像の取得先設定(ブックマークor作品)
def __getImageInfo(pixivpy, id: int, postType: str, word: str = None):
    if postType == "bookmark":
        return pixivpy.user_bookmarks_illust(id, 'public')
    elif postType == "post":
        return pixivpy.user_illusts(id)
    elif postType == "tag":
        if word == None:
            return False
        return pixivpy.search_illust(word = word, search_target = 'exact_match_for_tags', sort='date_asc')
    else:
        return False

# 投稿日付のフォーマット
def __formatPostDate(date: str) -> str:
    return str(date).split('+')[0].replace('T', ' ')

async def getImage(query, latestGetPosts = None):
    pixivpy = connect_pixivpy_api()
    imagesInfo = __getImageInfo(pixivpy, int(query['userID']), query['getPostType'], query['tag'])
    if imagesInfo == False:
        print('画像URLの取得に失敗しました。')
        sys.exit()

    # 画像のリンクを保管する配列
    illusts = []
    # 残りDL回数
    remaining = int(query['getNumberOfPost'])

    # 画像URL一覧を作成
    # URL取得を継続するかどうかのフラグ
    isContinueRefers = True
    while isContinueRefers:
        for imageCounter, imageInfo in enumerate(imagesInfo['illusts']):
            
            # ページのブックマーク数が30以下の場合現在のループで取得を終了
            if len(imagesInfo['illusts']) < 30:
                isContinueRefers = False

            # 次のブックマーク列の作成
            if imageCounter == 29:
                nextUrl = imagesInfo['next_url']
                await asyncio.sleep(1)
                print(f'redirecting to next page...')
                nextQs = pixivpy.parse_qs(nextUrl)
                await asyncio.sleep(1)
                print(f'get Image Infomations... remaining: {remaining}')
                if query['getPostType'] == "bookmark":
                    imagesInfo = pixivpy.user_bookmarks_illust(**nextQs)
                elif query['getPostType'] == "post":
                    imagesInfo = pixivpy.user_illusts(**nextQs)
                elif query['getPostType'] == "tag":
                    imagesInfo = pixivpy.search_illust(**nextQs)
                else:
                    isContinueRefers = False
                    break
                print('---------------------------------')
                await asyncio.sleep(1)


            # 取得した画像が指定されたIDの場合ループを終了
            if (
                str(imageInfo['id']) in latestGetPosts and
                query['isGetFromPreviousPost']
            ):
                isContinueRefers = False
                break

            # 残りDL数カウンタが0になった場合ループ終了
            if remaining <= 0:
                isContinueRefers = False
                break
            
            # タグ検索時、ブックマーク数が指定された数より少ない場合スルー
            if query['getPostType'] == "tag" and imageInfo['total_bookmarks'] < int(query['minBookmarks']):
                continue
            
            # ユーザーまたはタグ検索時かつR-18タグを除外する場合、R-18カテゴリをスルー
            tagList = [tag['name'] for tag in imageInfo['tags'] if 'name' in tag]
            if query['getPostType'] == "post" or query['getPostType'] == "tag":
                if query['isIgnoreSensitive'] and "R-18" in tagList:
                    print(f'ignore R-18 image: {imageInfo["id"]}')
                    continue
            
            # 残りDL数のデクリメント
            remaining -= 1

            # 上記バリデーションを全て通過した場合画像情報を作成して配列に追加
            illustsInfoQueue = dict()
            illustsInfoQueue['postID'] = imageInfo['id']
            illustsInfoQueue['post_time'] = imageInfo['create_date']
            illustsInfoQueue['user'] = imageInfo['user']['name']
            illustsInfoQueue['text'] = imageInfo['title']
            illustsInfoQueue['url'] = 'https://www.pixiv.net/artworks/' + str(imageInfo['id'])
            illustsInfoQueue['images'] = []
            # 画像URLの挿入
            # 画像が1枚の場合
            if len(imageInfo['meta_pages']) == 0:
                illustsInfoQueue['images'].append(imageInfo['meta_single_page']['original_image_url'])
            # 画像が複数枚の場合
            else:
                for metaPage in imageInfo['meta_pages']:
                    illustsInfoQueue['images'].append(metaPage['image_urls']['original'])

            illusts.append(illustsInfoQueue)
        # isContinueRefers = False
    
    print('done get images info')
    return illusts