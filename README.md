# 팀 소개

# 이하람  
컴퓨터과학과 24학번
MBTI: ISTJ
좋아하는 것: 피아노, 밴드, 뜨개질, 문학, 차, 만년필, 뜨개질, 이외 다수...

# 김현수

# 조재관

### 코드 실행 방법
- Web
- 크롤링

## 🚀 실행 방법 – 크롤링

1. 프로젝트 루트 디렉토리에서 아래 명령어를 실행하세요.

###  전체 사이트 크롤링 실행
```
python review_analysis/crawling/main.py -o database --all
````

###  특정 사이트만 실행
```
python review_analysis/crawling/main.py -o database --site {사이트이름}
```


2. 크롤링 결과는 아래 위치에 저장됩니다:

```
database/reviews_{사이트이름}.csv
```

> 예: `reviews_kakao.csv`, `reviews_naver.csv` 등


- EDA/FE

![이미지1](https://i.imgur.com/niDtCoG.jpg)  
![이미지2](https://i.imgur.com/FB4KpiX.jpg)
