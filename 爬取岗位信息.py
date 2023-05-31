import time
import requests
from bs4 import BeautifulSoup
import os
import csv
import json



def write_main_page(file_path, rec_json, count):
    data_list = []
    for key in rec_json:
        if key != 'enterpriseAddress' and key != 'enterpriseExtInfo' and key != 'keywordList' and key != 'skillsList':
            data_list.append(rec_json[key])
        if key == 'enterpriseExtInfo':
            for enterpriseExt_key in rec_json['enterpriseExtInfo']:
                if enterpriseExt_key != 'logo':
                    data_list.append(rec_json['enterpriseExtInfo'][enterpriseExt_key])
        if key == 'enterpriseAddress':
            for enterpriseAddress_key in rec_json['enterpriseAddress']:
                data_list.append(rec_json['enterpriseAddress'][enterpriseAddress_key])
        # if key == 'keywordList':
        #     kw0 = rec_json['keywordList'][0]
        #     kw1 = rec_json['keywordList'][1]
        #     for kw0_key in kw0:
        #         data_list.append(kw0[kw0_key])
        #     for kw1_key in kw1:
        #         data_list.append(kw1[kw1_key])

        # if key == 'keywordList':
        #     kw0 = main_json['keywordList'][0]
        #     kw1 = main_json['keywordList'][1]
        #     tempKeyWords = ''
        #     flag = 0
        #     for kw0_key in kw0:
        #         if kw0_key == 'labelName':
        #             if flag == 0:
        #                 tempKeyWords = tempKeyWords.join(kw0[kw0_key])
        #                 flag = 1
        #             else:
        #                 tempKeyWords = tempKeyWords.join(',' + kw0[kw0_key])
        #
        #     data_list.append(tempKeyWords)
        #     tempKeyWords = ''
        #     flag = 0
        #
        #     for kw1_key in kw1:
        #         if kw0_key == 'labelName':
        #             if flag == 0:
        #                 tempKeyWords = tempKeyWords.join(kw1[kw1_key])
        #                 flag = 1
        #             else:
        #                 tempKeyWords = tempKeyWords.join(',' + kw1[kw1_key])
        #     data_list.append(tempKeyWords)
        if key == 'keywordList':
            temp_key_words = ''
            flag = 0
            for kw_item in rec_json['keywordList']:
                for kw in kw_item:
                    if kw_item == 'labelName':
                        if flag == 0:
                            # tempSkillStr = tempSkillStr.join(skill_item[skill_kw])
                            temp_key_words = tempSkillStr + kw_item[kw]
                            flag = 1
                        else:
                            # tempSkillStr = tempSkillStr.join(',' + skill_item[skill_kw])
                            temp_key_words = tempSkillStr + ',' + kw_item[kw]
            data_list.append(temp_key_words)
        if key == 'skillsList':
            tempSkillStr = ''
            flag = 0
            for skill_item in rec_json['skillsList']:
                for skill_kw in skill_item:
                    if skill_kw == 'labelName':
                        if flag == 0:
                            # tempSkillStr = tempSkillStr.join(skill_item[skill_kw])
                            tempSkillStr = tempSkillStr + skill_item[skill_kw]
                            flag = 1
                        else:
                            # tempSkillStr = tempSkillStr.join(',' + skill_item[skill_kw])
                            tempSkillStr = tempSkillStr + ',' + skill_item[skill_kw]
            data_list.append(tempSkillStr)
    f = csv.writer(open(file_path, 'a+', encoding='utf-8', newline=''))
    f.writerow(data_list)
    count = count + 1
    print("\n\n\n\n---------------------------")
    print("爬取id{}，当前为第{}条数据".format(rec_json['id'], (int)(count / 3) + 1))
    print("\n\n\n\n---------------------------")
    return count


# 读取CSV文件
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


# 写入CSV文件
def write_csv(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


# 从CSV文件中读取表头
def get_csv_headers(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
    return headers


# 构建请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
url_pattern = "https://www.5iai.com/api/enterprise/job/public/es?pageNumber={}"
internal_detail_url_pattern = "https://www.5iai.com/api/enterprise/detail/{}"
internal_public_url_pattern = "https://www.5iai.com/api/enterprise/job/public?id={}"

if not os.path.exists("originMainPage.csv"):
    # 创建存储csv文件存储数据
    file0 = open('originMainPage.csv', "w", encoding="utf-8-sig", newline='')
    csv_head0 = csv.writer(file0)
    # 表头
    header = ['id', 'publishTime', 'updateTime', 'willNature', 'positionName', 'minimumWage', 'maximumWage',
              'payMethod',
              'exp', 'educationalRequirements', 'count', 'unkid', 'enterpriseId', 'provinceCode', 'cityCode',
              'regionCode', 'detailedAddress', 'remarks', 'keywords', 'enterpriseExtId', 'shortName', 'industry',
              'econKind', 'personScope']
    csv_head0.writerow(header)
    file0.close()

if not os.path.exists("originInternalDetailPage.csv"):
    # 创建存储csv文件存储数据
    file1 = open('originInternalDetailPage.csv', "w", encoding="utf-8-sig", newline='')
    csv_head1 = csv.writer(file1)
    # 表头
    header = ['id', 'enterpriseId', 'shortName', 'industry', 'econKind', 'startDate', 'registCapi', 'personScope',
              'website', 'email', 'phone', 'slogan', 'introduction',
              'label', 'postCode', 'recruitJobNum', 'totalPublicJobNum', 'unkid', 'enterpriseId', 'provinceCode',
              'cityCode', 'regionCode', 'detailedAddress', 'remarks']
    csv_head1.writerow(header)
    file1.close()

if not os.path.exists("originInternalPublicPage.csv"):
    # 创建存储csv文件存储数据
    file2 = open('originInternalPublicPage.csv', "w", encoding="utf-8-sig", newline='')
    csv_head2 = csv.writer(file2)
    # 表头
    header = ['id', 'enterpriseId', 'publishTime', 'updateTime', 'willNature', 'positionName', 'minimumWage',
              'maximumWage', 'payMethod', 'exp', 'educationalRequirements', 'count', 'jobRequiredments',
              'welfare', 'workplace', 'deadline', 'function', 'publisher', 'status', 'publisherName', 'enterpriseName',
              'messageTemplateId', 'unkid', 'enterpriseId', 'provinceCode', 'cityCode', 'regionCode', 'detailedAddress',
              'remarks', 'keywords', 'skillList',
              'resumeCount']
    csv_head2.writerow(header)
    file2.close()

total_pages = 159
index = 0
total_count = 0
for i in range(1, total_pages):
    index = index + 1
    # 增加时延防止反爬虫
    time.sleep(3)
    url = url_pattern.format(i)
    response = requests.get(url=url, headers=headers)

    # 声明网页编码方式，需要根据具体网页响应情况
    response.encoding = 'utf-8'
    response.raise_for_status()
    # soup = BeautifulSoup(response.text, 'html.parser')
    data = json.loads(response.text)
    data1 = data['data']['content']
    total_pages = data['data']['totalPages']
    # 解析
    for i in range(1, 11):
        try:
            item_id = data1[i - 1]['id']
            main_json = data1[i - 1]
            url = internal_public_url_pattern.format(item_id)
            time.sleep(1)
            response_public = requests.get(url=url, headers=headers)
            public_json = json.loads(response_public.text)['data']
            total_count = write_main_page('./originMainPage.csv', main_json, total_count)
            # public_json = public_json['data']
            enterprise_id = public_json['enterpriseId']
            url = internal_detail_url_pattern.format(enterprise_id)
            total_count = write_main_page('./originInternalPublicPage.csv', public_json, total_count)
            time.sleep(1)
            response_detail = requests.get(url=url, headers=headers)
            detail_json = json.loads(response_detail.text)['data']
            # detail_json = detail_json['data']
            total_count = write_main_page('./originInternalDetailPage.csv', detail_json, total_count)
        except:
            print("数据缺失")
