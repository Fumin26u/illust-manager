-   login firebase console
    PowerShell -ExecutionPolicy RemoteSigned firebase login

-   "このシステムではスクリプトの実行が無効になっている
    ため..." と出た時の対処
    Set-ExecutionPolicy RemoteSigned -Scope Process

-   .gitignore が機能しないとき
    git rm -r --cached .

-   ホスティングサービスにデプロイする場合の nuxt build コマンド
    npm run generate

-   firebase hosting にデプロイする
    firebase deploy

-   firebase hosting にデプロイしているファイルの削除
    firebase hosting:disable
