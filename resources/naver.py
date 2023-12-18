from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
import requests
from mysql_connection import get_connection
from mysql.connector import Error

class ChineseResource(Resource) :

    def post(self) :
        
        data = request.get_json()

        # 네이버의 파파고 API를 호출하여
        # 결과를 가져온다.

        # 파파고 API의 문서를 보고,
        # 어떤 데이터를 보내야 하는지 파악하여
        # reuests 의 get, post, put, delete 등의
        # 함수를 이용하여 호출하면 된다. 

        req_data = {
                        "source": "ko",
                        "target": "zh-CN",
                        "text": data['sentence']
                    }
        
        req_header = { "X-Naver-Client-Id" : "24q0xj6Ca8KwNEoUmZAM",
                      "X-Naver-Client-Secret" : "fO6Ih4cylA"}

        response = requests.post("https://openapi.naver.com/v1/papago/n2mt",  
                      req_data, 
                      headers= req_header )
        
        # 데이터를 파파고 서버로 부터 받아왔으니,
        # 우리가 필요한 데이터만 뽑아내면 된다.

        print(response)

        # 원하는 데이터를 뽑기 위해서는
        # json 으로 먼저 만들어 놔야 한다.
        response = response.json()

        print()
        print(response)


        chinese = response["message"]["result"]["translatedText"]

        return {"result" : "success" ,
                "chinese" : chinese}, 200
    

class NewsResource(Resource) :

    def get(self) :

        query = request.args.get('query')

        
    # 네이버 뉴스 검색 API 를 호출
        
        query_string = {'query' : query,
                        'display' : 30,
                        'sort' : 'date' }

        req_header = { "X-Naver-Client-Id" : "24q0xj6Ca8KwNEoUmZAM",
                      "X-Naver-Client-Secret" : "fO6Ih4cylA"}

        response = requests.get("https://openapi.naver.com/v1/search/news.json",
                     query_string,
                     headers= req_header)
        # 리스판스는 json 으로 해줘야 한다.
        response = response.json()

        return {'result' : 'success', 
                'items' : response['items'],
                'count' : len(response['items']) },200



