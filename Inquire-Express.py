#!/usr/bin/python2
#coding:utf-8

import requests
import re

def open_html_query(url):

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    html = requests.get(url, headers=headers)
    html = html.text
    #print(html)
    return html

def kdgs_query(danhao):
    #查询快递公司
    url = 'http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text=' + danhao
    open_html = open_html_query(url)
    kd_code = open_html
    kd_code = re.findall(r'"comCode":"([a-zA-Z]*)","id"', kd_code, re.S)
    return kd_code

def kd_information_query(danhao,kdgs):
    # 查询快递信息 1231231
    danhao_1 = danhao
    #kdgs_1 = kdgs[0]
    for kdgs_1 in kdgs:
    	url = 'https://www.kuaidi100.com/query?type=' + kdgs_1 + '&postid=' + danhao_1 + '&temp=0.07176910013370197'
    	kd_wuliu = open_html_query(url)
    	#print(kd_wuliu)
    	kd_wuliu_time = re.findall(r'time":"(.*?)","ftime', kd_wuliu, re.S)
    	kd_wuliu_ftime = re.findall(r'ftime":"(.*?)","context', kd_wuliu, re.S)
    	kd_wuliu_context = re.findall(u'context":"(.*?)","location', kd_wuliu, re.S)

    	#print(kd_wuliu_context)
	if kd_wuliu_context:
    		for (time,ftime,context) in zip(kd_wuliu_time,kd_wuliu_ftime,kd_wuliu_context):
        		a = ''.join(time)
        		b = ''.join(ftime)
        		c = ''.join(context)
        		print a,b,c
    		print('express:', kdgs_1)
	else:
		print('******')

def main(a):
    danhao = a
    #print(danhao)

    while danhao != 'q':
        # 查询快递公司
        aa = "1"
        aa_tt = aa.isdigit()
        tt = (danhao).isdigit()
        #判断输入是否未数字
        if tt == aa_tt:
            #查询快递公司
            kdgs = kdgs_query(danhao)
            #判断返回值是否为空
            if kdgs:
                # 查询快递信息
                kd_information = kd_information_query(danhao, kdgs)
                danhao = raw_input('Please enter the waybill number(q:quit):')
            else:
                information = 'Not querying ' + str(danhao) + ' information'
                print(information)
                danhao = raw_input('Please enter the correct single number(q:quit):')

        else:
            danhao = raw_input('Please enter the correct single number(q:quit):')

if __name__ == '__main__':
    a = raw_input('Please enter the waybill number(q:quit):')
    main(a)
