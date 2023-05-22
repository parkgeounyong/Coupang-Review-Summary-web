import openai
import re
from konlpy.tag import Okt
from nltk import Text
import matplotlib.pyplot as plt

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
    prompt = "$와$  사이에 있는 건 돼지 고기의 상태를 나타내는 형용사야. 해당 형용사로 후기를 작성해줘. 단, 아래의 지시사항을 참고해줘.\n\n1. 입력 언어: 한국어\n2. 출력언어: 한국어\n3. 스타일: 간결하게\n4. 독자 대상:구매자\n5. 답변 길이: utf-8 인코딩 기준 최대 100바이트\n6. 후기 카테고리: 돼지 고기\n7. 추가 지시사항:\n후기를 작성할 때 형용사는 반드시 포함하여 돼지 고기 후기를 작성해줘, 요약 형태로 작성해줘\n\n$"
    top_adj = Tokenizer(text)
    prompt+="\n"
    for token in top_adj:
        prompt += token+" "
    prompt=prompt+"\n$"    
    completions = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = completions.choices[0].text.strip()
    return message
