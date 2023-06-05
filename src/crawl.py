from bs4 import BeautifulSoup as bs
from typing import Optional,Union,Dict,List
import time
import re
import requests as rq
import json
import re

def get_headers(
    key: str,
    default_value: Optional[str] = None
    )-> Dict[str,Dict[str,str]]:
    """ Get Headers """
    JSON_FILE : str = 'json/headers.json'
    
    with open(JSON_FILE,'r',encoding='UTF-8') as file:
        headers : Dict[str,Dict[str,str]] = json.loads(file.read())

    try :
        return headers[key]
    except:
        if default_value:
            return default_value
        raise EnvironmentError(f'Set the {key}')

class Coupang:
    @staticmethod
    def get_product_code(url: str)-> str:
        """ 입력받은 URL 주소의 PRODUCT CODE 추출하는 메소드 """
        prod_code : str = url.split('products/')[-1].split('?')[0]
        return prod_code

    def __init__(self)-> None:
        self.__headers : Dict[str,str] = get_headers(key='headers')

    def main(self, URL)-> List[List[Dict[str,Union[str,int]]]]:
        # URL 주소
        URL : str = URL

        # URL의 Product Code 추출
        prod_code : str = self.get_product_code(url=URL)

        # URL 주소 재가공
        URLS : List[str] = [f'https://www.coupang.com/vp/product/reviews?productId={prod_code}&page={page}&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true' for page in range(1,self.get_review_count(URL))]

        # __headers에 referer 키 추가
        self.__headers['referer'] = URL
        
        #웹사이트에서 리뷰 읽어드리면서 내용없으면 리턴
        with rq.Session() as session:
            data=[]
            for url in URLS:
                data_s=self.fetch(url=url,session=session)
                for i in data_s:
                    review_content = i['review_content']
                    if(review_content=="등록된 리뷰내용이 없습니다"): 
                        return data
                    data.append(review_content)
            return data

    def fetch(self,url:str,session)-> List[Dict[str,Union[str,int]]]:
        save_data : List[Dict[str,Union[str,int]]] = list()

        with session.get(url=url,headers=self.__headers) as response :
            html = response.text
            soup = bs(html,'html.parser')
            
            # Article Boxes
            article_lenth = len(soup.select('article.sdp-review__article__list'))

            flag=0
            for idx in range(article_lenth):
                dict_data : Dict[str,Union[str,int]] = dict()
                articles = soup.select('article.sdp-review__article__list')

                # 구매자 이름
                user_name = articles[idx].select_one('span.sdp-review__article__list__info__user__name')
                if user_name == None or user_name.text == '':
                    user_name = '-'
                else:
                    user_name = user_name.text.strip()

                # 평점
                rating = articles[idx].select_one('div.sdp-review__article__list__info__product-info__star-orange')
                if rating == None:
                    rating = 0
                else :
                    rating = int(rating.attrs['data-rating'])

                # 구매자 상품명
                prod_name = articles[idx].select_one('div.sdp-review__article__list__info__product-info__name')
                if prod_name == None or prod_name.text == '':
                    prod_name = '-'
                else:
                    prod_name = prod_name.text.strip()

                # 헤드라인(타이틀)
                headline = articles[idx].select_one('div.sdp-review__article__list__headline')
                if headline == None or headline.text == '':
                    headline = '등록된 헤드라인이 없습니다'
                else:
                    headline = headline.text.strip()

                # 리뷰 내용
                review_content = articles[idx].select_one('div.sdp-review__article__list__review > div')
                if review_content == None :
                    review_content = '등록된 리뷰내용이 없습니다'
                    flag=1
                else:
                    review_content = re.sub('[\n\t]','',review_content.text.strip())

                # 맛 만족도
                answer = articles[idx].select_one('span.sdp-review__article__list__survey__row__answer')
                if answer == None or answer.text == '':
                    answer = '맛 평가 없음'
                else:
                    answer = answer.text.strip()
                

                dict_data['prod_name'] = prod_name
                dict_data['user_name'] = user_name
                dict_data['rating'] = rating
                dict_data['headline'] = headline
                dict_data['review_content'] = review_content
                dict_data['answer'] = answer

                save_data.append(dict_data)


            time.sleep(1)

            return save_data

        
    # 입력: 읽어드릴 URL
    # 출력: 페이지 수 출력
    # 동작: 전체리뷰/한 페이지에 존재하는 리뷰(5) + 1    
    def get_review_count(self, url):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}
        res = rq.get(url, headers=headers)
        res.raise_for_status()

        soup = bs(res.text, "lxml")
        items = soup.find_all("span", attrs={"class":re.compile("^count")})
        count_str = items[0].text # Tag 객체에서 텍스트만 추출하여 저장
        count = int(''.join(filter(str.isdigit, count_str)))
        return int(count / 5) + 1
        

class OpenPyXL:
    @staticmethod
    def save_file(URL)-> None:
        # 크롤링 결과
        results= Coupang().main(URL)
        # 크롤링 결과 모음
        return results
