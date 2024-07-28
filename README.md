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

## Character Classificator(仮)
- [Deepdanbooru](https://github.com/KichangKim/DeepDanbooru)を用いて、イラスト内のキャラクターを判別するツールです。

## ImageDLer
- Twitter(現X)・pixivの画像をまとめて取得・ダウンロードするツールです。

- 指定したユーザーIDの、Twitterは「いいね」、pixivは「ブックマーク」・「ポスト」の画像一覧を取得できます。

- pixivの投稿取得には[pixivpy](https://github.com/upbit/pixivpy)モジュールを利用しています。
