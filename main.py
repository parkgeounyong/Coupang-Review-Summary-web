from src.crawl import OpenPyXL
from src.openai_method import *


#입력: ,출력: 요약된 후기
def make_summary(URL):
    #리뷰 크롤링
    review_collection=OpenPyXL.save_file(URL)

    text=""
    for review in review_collection:
        text=text+review

    #리뷰 요약 생성
    element=extract_element(text)
    #요약된 리뷰 반환
    return element
