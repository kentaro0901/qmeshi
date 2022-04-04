# 九大のメシ

## 概要
九州大学の今日の学食メニューを一覧表示するWebアプリ「九大のメシ」の中身．また，Twitterにメニューを投稿する「九大のメシbot」も動かしている．

## 特徴
- 今日のメニューのみに絞って確認できる（公式は月間）
- レスポンシブ表示が可能なのでスマホでも見やすい
- 運営主体が異なる学食のメニューを同じページで確認できる
- メニューの更新やTwitterへの投稿も全て自動で行う．

## 使用技術など
- Python 3.8
- Django 3.2
- Bootstrap 5
- Heroku

# 環境構築メモ

## 仮想環境
```
pip install pipenv          # 導入
pipenv install --python 3.9 # 仮想環境の作成 Pipfileがあればそれを読み込む
pipenv sync                 # 仮想環境の再現 Pipfile.lockから再現される
pipenv update               # ライブラリを更新したいとき
pipenv shell                # 仮想環境の起動
pipenv install django       # ライブラリのインストール
pipenv run pip freeze       # インストール済みの確認
exit                        # 仮想環境の終了
```

## django
```
django-admin startproject [project_name]    # プロジェクトの作成
python manage.py migrate                    # SQlite作成
python manage.py createsuperuser            # スーパーユーザーの作成（adminが使える）
python manage.py runserver                  # 開発用サーバの起動
python manage.py startapp [app_name]        # アプリの作成
python manage.py makemigrations [app_name]  # model.pyからDBへ射影するファイルの作成
python manage.py migrate [app_name]         # ↑をDBに反映
python manage.py collectstatic              # staticファイルを[project_name]/staticfilesにまとめる
python manage.py test                       # テスト
```

## ライブラリ
初回のみ
`pipenv install`もしくは`pipenv sync`で必要なものは全部入るはず
```
pipenv install django               # 本体
pipenv install django-bootstrap5    # CSSフレームワーク
pipenv install gunicorn             # 本番用httpサーバー
pipenv install django-heroku        # Herokuとの連携
pipenv install dj-database-url      # 多分postgleSQL用
pipenv install whitenoise           # staticファイルのサポート
```

## Herokuとの連携
初回のみ
```
brew tap heroku/brew && brew install heroku     # herokuのCLI
heroku create [project_name]                    # プロジェクトの作成
heroku config:set SECRET_KEY=""                 # djangoのシークレットキーを環境変数に設定
heroku git:remote -a [project_name]             # リモートリポジトリに設定 自動デプロイを設定するなら不要
git push heroku master                          # 同上
heroku ps:scale web=1                           # スケールの設定（あまりよくわかっていない）
heroku run python manage.py migrate             # heroku上でもマイグレーションしておく
heroku run python manage.py createsuperuser     # heroku上でもスーパーユーザーを作成しておく
heroku open                                     # サイトを開く
```
よく使うコマンド
```
heroku login                                    # CLIログイン
heroku run '[command]' --app [app_name]         # コマンドの実行 ''で囲んだほうがいい？
```

## 開発中メモ
- model.pyを編集したら`makemigrations`と`migrate`を実行
- `pipenv install [hoge]`を実行するとPipfile（&.lock）が更新される
  - Pipfileがある階層で`pipenv install`を実行すると全部入るが，バージョンを指定していないと（多分）最新版が入るので注意
  - チーム開発なら`sync`を使えばPipfile.lockに保存されている他の人のバージョンと同じにできるので安全
- runserverは基本的に動かしっぱなしでいい
- pandasのバージョンを1.4.2にするとread_htmlでエンコードエラーが出る(今は1.3.5) 原因は不明
- ローカルファイル(update.pyなど)のimport順は決まっているため自動フォーマットをかけてはいけない
- `# NOQA`でflake8の警告を無視できる

## リンク
- [管理ページ（ローカル）](http://127.0.0.1:8000/admin/)
- [九大のメシ（ローカル）](http://127.0.0.1:8000/)
- [管理ページ（Heroku）](https://qmeshi.herokuapp.com/admin/)
- [九大のメシ（Heroku）](https://qmeshi.herokuapp.com)
- [九大のメシbot（Twitter）](https://twitter.com/qu_gakushoku)
- [Django入門](https://qiita.com/kaki_k/items/511611cadac1d0c69c54)
- [Herokuにデプロイ](https://qiita.com/frosty/items/66f5dff8fc723387108c)
