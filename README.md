vjvj_crawler
============

##Requirements

Python 3+ 

scrapy
```
  pip install scrapy
```

##Run Setting

config directory 의 config.cfg 에 크롤링할 정보 입력  

```
  >>> main.py 섹션명
```

##Run

```
  >>> main.py
```

##config.cfg 구성

```
[섹션명1]
parsing_url = crawling url (ex : http://...&page=__page__)
limit_page = __PAGE__에 치환될 crawling page 제한
regex_article = 게시물 영역 pattern
regex_title = 게시물의 title pattern
regex_seq = 게시물의 seq 가 될 부분의 pattern

[섹션명2]
형식 상동
```
