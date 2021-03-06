import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

# 批量获取不同企业的ID值
url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'

# 首页 json 返回的数据是一个列表的形式，里面每一家的信息是字典类型
id_list = []  # 存储企业的 ID
all_data_list = []  # 存储所有的企业详情数据

# 参数封装，并进行分页，如果需要全部，只需把 range 第二个参数修改为 370 即可
for page in range(1, 370):
    page = str(page)
    data = {
        'orderBy': "createDate",
        'orderType': "desc",
        'pageCount': '370',
        'pageNumber': page,
        'pageSize': '15',
        'property': "",
        'totalCount': '5545'
    }

    json_ids = requests.post(url=url, headers=headers, data=data).json()
    for dic in json_ids['list']:
        id_list.append(dic['ID'])  # 将取得的 ID 放入空列表 id_list 中


# 获取企业详情数据
post_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
for id in id_list:
    data = {
        'id': id
    }
    detail_json = requests.post(url=post_url, headers=headers, data=data).json()
    print(detail_json)
    all_data_list.append(detail_json)

# 持久化存储 all_data_list
fp = open('./allData.json', 'w', encoding='UTF-8')
json.dump(all_data_list, fp=fp, ensure_ascii=False)
print('OVER!!')
