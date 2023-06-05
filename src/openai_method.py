import openai
from konlpy.tag import Okt
from nltk import Text

openai.api_key = "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"


def Tokenizer(text):
    okt = Okt()

    # 형태소 분석
    morphemes = okt.pos(text)

    # 명사, 형용사 형태소만 추출
    adj = [word for word, pos in morphemes if pos in ['Adjective'] and len(word) >= 2 and word not in ['입니다', '있습니다']]

    # 단어 빈도수 계산
    adj_freq = Text(adj).vocab()

    # 빈도수가 높은 단어 10개 출력
    top_adj = adj_freq.most_common(4)
    #top_nouns = [t[0] for t in top_nouns]
    top_adj = [t[0] for t in top_adj]
    # 결과 출력
    return top_adj

    

def extract_element(text):
    # 문장 요약
    prompt = "너는 쿠팡에서 판매되는 돼지 고기 상품에 대한 후기를 작성하는 돼지고기 소비자야. 돼지 고기 후기에서 추출한 형용사 중 가장 빈도수가 높은 5개 형용사를 사용하여, 한 문장으로 이루어진 돼지고기 맛에 대한 후기를 작성해보자. 매운맛과 관련된 문장이나 단어는 포함하지 않을 거야. 함께 한국어 문법에 맞는 문장으로 작성해보자. 그럼 step by step으로 진행해보자."
    top_adj = Tokenizer(text)
    prompt+="\n"
    for token in top_adj:
        prompt += token+" " 
    completions = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = completions.choices[0].text.strip()
    return message
