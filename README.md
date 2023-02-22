# navernews_img-cap

### 네이버 뉴스를 보면 뉴스 관련된 사진과 바로 밑에 그에 대한 설명이 있는 것을 볼 수 있다. 

<img width="744" alt="image" src="https://user-images.githubusercontent.com/42092560/220531659-d4814a3c-5c6a-40f9-8031-c78aaea1ceff.png">

### 이 두가지를 잘 긁어오면 이미지 캡셔닝 데이터로 잘 사용 할 수 있지 않을까

***

### 뉴스 카테고리와 시작 날짜 끝 날짜를 입력하면 그 기간 안의 해당 카테고리 뉴스의 이미지와 캡션을 크롤링 합니다.
- ### 뉴스 카테고리
```
    경제 : Economy
    정치 : Politics
    사회 : Society
    생활 : LifeCulture
    세계 : World
    IT : It
    사설칼럼 : Opinion
```
- ### 캡션 결과 / tsv파일
```
이미지파일 이름 [탭] 캡션
이미지파일 이름 [탭] 캡션
이미지파일 이름 [탭] 캡션
...
```
- ### 사용법
```
-i : 이미지 디렉토리
-c : 캡션 디렉토리
-s : 시작 날짜
-e : 끝 날짜
-n : 이미지 폴더 하나당 저장할 이미지 개수
-g : 뉴스 카테고리
```
```
$ python3 main.py -i ./image -c ./caption -s 20230220 -e 20230222 -n 3 -g It
```
