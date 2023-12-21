# IllustManager(仮)
## README
- 現在開発中につき、ダウンロードのみでは動作しないです。

- 本リポジトリの一部は、[こちらの顔検出ツール](https://github.com/maya-hanada/anime-face-detector)を利用させて頂いております。

以下WIP
***
## 概要
- 機械学習によるキャラクター画像のキャラクター毎のフォルダ分類器(Character Classificator(仮))と、[ImageDLer](https://github.com/Fumiya0719/likedimagedler_v2)の、2ツールの統合リポジトリです。

- 両ツールともにWebUI上で使用可能です。

## Character Classificator(仮)
- キャラクターの顔画像を基に機械学習を行い作成したモデルを用いて、イラスト内のキャラクターを判別するツールです。

- ~~正直どういう仕組みかよくわかっていない~~

- 顔認識には、[こちらのツール(リポジトリ)](https://github.com/maya-hanada/anime-face-detector)を利用させて頂いております。

## ImageDLer
- Twitter(現X)・pixivの画像をまとめて取得・ダウンロードするツールです。

- 指定したユーザーIDの、Twitterは「いいね」、pixivは「ブックマーク」・「ポスト」の画像一覧を取得できます。

- pixivの投稿取得には[pixivpy](https://github.com/upbit/pixivpy)モジュールを利用させて頂いております。