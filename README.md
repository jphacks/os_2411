# <ruby>Chronotes<rp>(</rp><rt>クロノート</rt><rp>)</rp></ruby>

[![YouTube](https://raw.githubusercontent.com/jphacks/os_2411/refs/heads/main/docs/images/1.png)](https://www.youtube.com/watch?v=JpJH_WVD53E)

**[紹介動画](https://www.youtube.com/watch?v=JpJH_WVD53E)**

## 製品概要

### 背景 (製品開発のきっかけ、課題等)

![2](https://raw.githubusercontent.com/jphacks/os_2411/refs/heads/main/docs/images/2.png)

日記や日報と言った毎日の記録をつける作業って、面倒くさいと感じたことはありませんか？  
また、せっかくつけた記録を振り返ることなく、活用できずにいませんか？  
私達はそのような課題を解決したいと考え、「Chronotes」を開発しました。  

### 製品説明 (具体的な製品の説明)

![3](https://raw.githubusercontent.com/jphacks/os_2411/refs/heads/main/docs/images/3.png)

ChronotesはAI駆動のノート生成を行うアプリケーションです。  
ユーザーはあらかじめアカウントを連携しておくだけで、AIが毎日の作業ログを自動で収集し、簡潔にまとめて「ノート」に書き出します。  
ユーザーはこのノートを見るだけで、毎日の作業内容を把握でき、振り返ることができます。  
作業ログはGitHub, Discord, Slack, Qiitaなどの複数のサービスから毎日自動で収集します。  
現在は開発者向けサービスとして開発しているため、開発者向けのサービス連携が多いです。  
また、毎日生成されるノートだけではなく、週や月ごとに作業内容をまとめたノートも生成します。  
これにより、この週はooをやった、この月はxxをやった、のように大局的な視点で振り返ることができます。  

### 特長

#### 1. 特長1

![6](https://raw.githubusercontent.com/jphacks/os_2411/refs/heads/main/docs/images/6.png)

Chronotesでは、カレンダーを使用して日々の進捗を可視化することができます。  
表示されているカレンダーは、メモに記録された文字数に基づいて日付の色が変化する仕組みを取り入れています。  
文字数が多い日ほど色が濃く、少ない日ほど色が薄くなります。  
この色の変化により、メモの量、つまりその日の活動や記録の充実度を直感的に把握することが可能です。  
例えば、カレンダー上で色が濃い日付は、その日に多くのメモが残されていることを示しており、逆に色が薄い日付はあまり書き込みがなかったことを意味します。  
この視覚的な進捗の表現は、ユーザーが自身の活動のペースや取り組みの度合いを一目で確認するのに役立ちます。  

#### 2. 特長2

![8](https://raw.githubusercontent.com/jphacks/os_2411/refs/heads/main/docs/images/8.png)

Chronotesでは、ノートの自動生成のために各サービスとの連携を行っています。  
この例では、SlackとDiscordからは会話内容、ZennやQiitaからは記事のタイトル、GitHubからはコミットメッセージと変更内容を収集しています。  
これらの収集されたデータはGeminiによって要約され、ノートとして出力されます。

#### 3. 特長3

![9](https://raw.githubusercontent.com/jphacks/os_2411/refs/heads/main/docs/images/9.png)

生成された要約文からタイトルとタグを自動生成します。
今回の文章からは、タイトルは「SlackとDiscordの連携」、タグは「Intrinsic」「GAS」「LZ78」が生成され、計3つのタグが生成されます。

#### 4. 特長4

![7](https://raw.githubusercontent.com/jphacks/os_2411/refs/heads/main/docs/images/7.png)

Chronotesでは日々の記録の可視化にも力を入れており、ノートのタグからワードと頻度を元にWordCloudを生成します。  
これは頻度が高いワードほど大きく表示されるもので、サマリーページに表示することにより、ユーザーは特定の期間の内容を簡潔に把握することができます。  

### 解決出来ること

![4](https://raw.githubusercontent.com/jphacks/os_2411/refs/heads/main/docs/images/4.png)

Chronotesは、開発者やチームリーダー、自己管理を重視する人々のためのアプリケーションです。  
AIが毎日の作業ログを自動で収集し、簡潔なノートを生成します。  
これにより、日報を書く手間が省け、重要な業務に集中できるようになり、四半期や半期の評価作業もスムーズに行え、作業効率が向上します。  

### 注力したこと (こだわり等)

* スマホ/PC問わず使えるようなUI
* AIによるノートの自動生成
* ノートの内容に即したタイトルやタグの自動生成
* ノートをまとめる機能による大局的な視点での振り返り
* WordCloudによる日々の記録の可視化
* GitHub ActionsによるCI/CD

## 開発技術

![10](https://raw.githubusercontent.com/jphacks/os_2411/refs/heads/main/docs/images/10.png)

### 活用した技術

<img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/google-gemini-icon.png" width="5%">

* Gemini

#### API・データ

<div style="display: flex; align-items: center;">
    <img src="https://skillicons.dev/icons?i=github,gitlab" />
    <img height="48" width="48" src="https://cdn.simpleicons.org/slack/4A154B" />
    <img src="https://skillicons.dev/icons?i=discord" />
    <img height="48" width="48" src="https://cdn.simpleicons.org/wakatime/7d7d7d" />
    <img height="48" width="48" src="https://cdn.simpleicons.org/zenn/3EA8FF" />
    <img height="48" width="48" src="https://cdn.simpleicons.org/qiita/55C500" />
    <img height="48" width="48" src="https://pbs.twimg.com/profile_images/540067771736813568/tIWMSAZF_400x400.png" />
</div>

* GitHub
* GitLab
* Slack
* Discord
* Wakatime
* Zenn
* Qiita
* Connpass

#### フレームワーク・ライブラリ・モジュール

![tech](https://skillicons.dev/icons?i=nextjs,go,docker,githubactions)

* Next.js
* TipTap
* Go
* Docker
* Docker Compose
* GitHub Actions

### 独自技術

#### ハッカソンで開発した独自機能・技術

* [対応するサービスの拡大 (connpass, Wakatime)](https://github.com/yashikota/chronotes/pull/105)

    connpassからは参加したイベントのタイトル、Wakatimeから1日の作業時間を取得が可能になった。
  

* [ノートを他のユーザーとシェアできる機能の作成](https://github.com/yashikota/chronotes/pull/141)

    生成されたノートはセキュリティ上、所有者本人のみ閲覧できるが、外部に公開したい場面もありうる。  
    そのため、一時的に外部に公開できるような機能開発を行った。  
    この共有機能はユーザーが任意のタイミングで公開・非公開を選ぶことができる。  
    これによりユーザーは共有したいノートを好きなタイミングで公開できるようになった。  

* [形態素解析エンドポイントの作成](https://github.com/yashikota/chronotes/pull/142)

    現在WordCloudで生成される元のデータはタグだが、本文から生成したいというニーズもあることから任意のテキストを入力すると、形態素解析した結果を返すエンドポイントを作成した。  
    これにより、より詳細な情報をユーザーは一目で確認することができるようになった。  

* [画像のアップロードに対応](https://github.com/GenichiMaruo/chronotes-front/pull/49)

    ユーザーエクスペリエンス向上のため、ノートエディターに画像を直接ドラッグ&ドロップする機能を実装した。この機能により、ユーザーは画像を簡単にノートに挿入できるようになった。
    ドラッグ&ドロップされた画像は、フロントエンドのAPI通信モジュールを経由してバックエンドにアップロードされる。バックエンドでは、セキュリティ確保のため、アップロードされた画像にアクセスするためのURLに有効期限を設定している。これにより、不正なアクセスやデータ漏洩のリスクを軽減している。

* [期間要約ページを新規作成](https://github.com/GenichiMaruo/chronotes-front/pull/44)

    期間要約表示ページを新たに作成し、より詳細な分析を可能にした。期間選択をプルダウンメニューに変更し、より多くの期間候補を追加することで、ユーザーは任意の期間のデータを手軽に要約できるようになった。さらに、ページ上部にワードクラウドを表示することで、指定期間のノートに頻繁に使われているタグを一目で把握できるようになり、データの可視化を強化した。ワードクラウドは、ノートに付与されたタグの頻度に基づいてフロントエンドで自動生成されている。

* [デモモードの作成](https://github.com/GenichiMaruo/chronotes-front/pull/50)

    URLにdemoクエリパラメータを追加することで、事前に準備されたデータを使ってChronotesを試せるようになります。
    これにより、初回のみの試用や、紹介時にサインアップやログインを省いてスムーズに利用体験が可能です。
    https://chronotes.yashikota.com/?demo

<!-- 
submodule更新
```sh
git submodule update --init --recursive
```
-->
