### safebooruからのスクレイピングコード.

### ソース

- scraping_from_safebooru.ipynb  
ダウンロードするメインコード

- scraping_from_safebooru.py  
スクレイピング用関数

- arrange_images_from_json_info.ipynb
jsonファイルを読み込んで、データ準備する最低限のコード

  - jsonからタグを抽出して、txtに出力. 
  - タグを見てウインク画像だけをコピー ( "greyscale"や"monochrome"タグを外すなどの前処理が考えられる. )


### memo

- あまりに大きい画像サイズは圧縮を考えたほうがいいかも
  - たまに超美麗画像 ( > 20MB )などがあるので、学習時のファイル読み込みに影響あるかも?

- 

### Todo
- 異常系のスキップ処理
- 並列取得処理.