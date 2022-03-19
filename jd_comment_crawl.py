import xlwt
import requests
import json
f = xlwt.Workbook()
sheetwrite = f.add_sheet('comment')
sheetwrite.write(0,0,'comment')
k = 1
for page in range(0,100+1):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}

    #url1 = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=5225346&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(page)

    url2 = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=5225346&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(page)

    response = requests.get(url2, headers=header)
    data = response.text
    jd = json.loads(data.lstrip('fetchJSON_comment98vv12345(').rstrip(');'))
    data_list = jd['comments']

    for data in data_list:
        content = data['content']
        sheetwrite.write(k,0,content)
        k +=1
f.save('./bad.xls')