# IllustManager(仮)
## README
- 名前の通り画像管理システム
- ローカルで動作します。事故が怖いのでWeb上に公開とかはしない予定

## 概要
- いろいろ画像管理システム
  - 各種SNSから画像を自動DLする
  - ローカルの画像からタグを生成する
  - 画像とタグを紐づけてDBに格納する
  - etc

## Image Manager
ローカルにある画像に対して、[Deepdanbooru](https://github.com/KichangKim/DeepDanbooru)を用いて、
イラストにタグ付与を行い、DBに紐づける形で登録します。
以下はWIP
- タグを基準にした画像ソート
- 手動で画像にタグを付与してDeepdanbooruに学習させる
  - ローカルのDeepdanbooruに対して学習させるのみでpublicにはしない 

## ImageDLer
- Twitter(現X)・pixivの画像をまとめて取得・ダウンロードするツールです。
- 指定したユーザーIDの、Twitterは「いいね」、pixivは「ブックマーク」・「ポスト」の画像一覧を取得できます。
- pixivの投稿取得には[pixivpy](https://github.com/upbit/pixivpy)モジュールを利用しています。
