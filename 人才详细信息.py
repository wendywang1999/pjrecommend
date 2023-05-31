# -*- coding: utf-8 -*-
# @Time : 2023/2/28/028 20:27
# @Author : LeeSheel
# @File : 02根据人才id获取详细信息.py
import datetime
import json
from termcolor import  cprint
import requests
import csv
import time


def get_source(id):
    url = 'https://www.5iai.com/api/resume/baseInfo/public/{}'.format(id)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    res = requests.get(url, headers=header)
    html = res.text
    return html

def calculate_age(birth):
    birth_d = datetime.datetime.strptime(birth, "%Y-%m-%d")
    today_d = datetime.datetime.now()
    age = today_d.year - birth_d.year
    return age




def get_info(html):
        try:
            data_list =[]
            json_data = json.loads(str(html))
            data = json_data['data']
            id = data['id']+',' #求职者id
            name = data['username'] #姓名
            resumeName = data['expectPosition'] #预期岗位
            '''
            其他信息：
            性别、年龄、居住地址、工作经验、自我评价、期望薪资低、期望薪资高、工作性质、期望行业、工作地区、到岗时间、简历关键词
            学历、大学专业、
            '''
            gender = data['gender'] #其他- 性别  0为男、1为女
            birthday = data['birthday']
            print(birthday)
            if birthday != None:
                if 'T' in str(birthday):
                    age = calculate_age(birthday.split('T')[0]) #其他- 年龄
                else:
                    age = calculate_age(birthday.split(' ')[0])  # 其他- 年龄
            else:
                age='无'
            print(age)
            address = data['address']
            exp = data['exp'] #其他- 工作经验
            selfEvaluation = data['selfEvaluation'] #其他- 工作经验
            # print(selfEvaluation)
            willSalaryStart = data['willSalaryStart'] #其他- 期望薪资低
            willSalaryEnd  = data['willSalaryEnd'] #其他- 期望薪资高
            jobStatus = data['jobStatus']  #其他- 工作性质 0：全职 1：实习
            expectIndustry = data['expectIndustry']#其他- 期望行业
            city = data['city']  #工作地区
            arrivalTime = data['arrivalTime'] #到岗时间
            keywordList = data['keywordList']
            # print("keywords",keywordList)
            keywords  = ""   #简历关键词 空格隔开
            if keywordList != "":
                for v in keywordList:
                    keywords+=v['labelName']+' '
            else:
                keywords+="无"
            # print(keywords)

            educationExperienceList = data['educationExperienceList']
            education =""#学历 空格隔开
            speciality ="" #大学专业 空格隔开
            if educationExperienceList !="":
                for v in educationExperienceList:
                    education += v['educationalBackground']+' '
                    speciality +=v['speciality']+' '
            else:
                education +='无'
                speciality +='无'

            print(id,name,resumeName, gender,address,age,exp,selfEvaluation,willSalaryStart,willSalaryEnd,jobStatus
                 ,expectIndustry,city,arrivalTime,keywords,education,speciality)
            print("----------------------------------------------------------------------------------")
            data_list.append(
                [id,name,resumeName, gender,age,address,exp,selfEvaluation,willSalaryStart,willSalaryEnd,jobStatus
                 ,expectIndustry,city,arrivalTime,keywords,education,speciality])

            with open('根据人才id获取详细数据(10897条).csv', 'a+', encoding='utf-8', newline='') as csvFile:
                for rows in data_list:
                    csv.writer(csvFile).writerow(rows)
        except:
            pass


def reads_txt():
    f=open('找人才页面id.txt')
    data = f.readlines()  #
    f.close()  # 关
    print(data) #返回list
    return data


if __name__ == '__main__':
    with open('根据人才id获取详细数据(10897条).csv', 'a+', encoding='utf-8', newline='') as csvFile:
        csv.writer(csvFile).writerow(
            ['求职者id', '姓名', '期望岗位', '性别', '年龄', '居住地址', '工作经验', '自我评价', '期望薪资低', '期望薪资高',
             '工作性质', '期望行业', '工作地区', '到岗时间','简历关键词','学历','学科专业'])
    csvFile.close()
    ids = reads_txt()

    for index, id in enumerate(ids):
        print("爬取第{}个,id为{}".format(index + 1, id))
        res = get_source(id.strip())
        get_info(res)
        time.sleep(2)

    # res = get_source('1630105867208753152')
    # get_info(res)







