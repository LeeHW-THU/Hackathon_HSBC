# -*- coding: utf-8 -*-
# @Time    : 2019/4/13 7:23 PM
# @Author  : LeeHW
# @File    : sql.py
# @Software: PyCharm
import pandas
import sqlite3
import requests
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime


# plt.style.use('ggplot')
# mpl.rcParams['font.family'] = 'simhei'

def test_fzb(df):
	test = [
		'[所有者权益(或股东权益)合计]',
		'资产总计',
		'流动资产合计',
		'流动负债合计',
		'存货',
		'应收账款',
		'负债合计'
	]
	columns = df.columns.values.tolist()
	print(columns)
	for t in test:
		if not t in columns:
			print(t + ' not in fzb')

def test_llb(df):
	test = [

	]
	columns = df.columns.values.tolist()
	print(columns)
	for t in test:
		if not t in columns:
			print(t + ' not in llb')

def test_lrb(df):
	test = [
		'营业收入',
		'营业成本',
		'净利润',
		'营业总收入',
		'利息支出',
		'所得税费用',
		'营业利润',
		'财务费用',
	]
	columns = df.columns.values.tolist()
	print(columns)
	for t in test:
		if not t in columns:
			print(t + ' not in lrb')

def create_data(stock_id):	#生成临时数据库
	try:
		conn = sqlite3.connect("{}_data.db".format(stock_id))
		df = pandas.read_csv('{}_fzb.csv'.format(stock_id))
		df = df.fillna(0)
		# test_fzb(df)
		df.to_sql('fzb', conn, if_exists='replace', index=False)
		df = pandas.read_csv('{}_llb.csv'.format(stock_id))
		df = df.fillna(0)
		# test_llb(df)
		df.to_sql('llb', conn, if_exists='replace', index=False)
		df = pandas.read_csv('{}_lrb.csv'.format(stock_id))
		df = df.fillna(0)
		renameColumns(df)
		# test_lrb(df)
		df.to_sql('lrb', conn, if_exists='replace', index=False)
		remove_csv(stock_id)
	except BaseException:
		print("读取数据失败——请联网或者重新下载...")
	else:
		print('建立{}_data.db数据库完成....'.format(stock_id))

def renameColumns(df):
	columns_need_rename = [
		'一、营业收入',
		'二、营业支出',
		'三、营业利润',
		'四、利润总额',
		'五、净利润',
	]
	columns_correct = [
		'营业收入',
		'营业成本',
		'营业利润',
		'利润总额',
		'净利润',
	]
	columns = df.columns.values.tolist()
	for column_need_rename in columns_need_rename:
		if column_need_rename in columns:
			df.rename(columns={column_need_rename : columns_correct[columns_need_rename.index(column_need_rename)]}, inplace = True)

headers = {
	'User-Agent': 'Mozilla/5.0',
	'Cookie': 'xq_a_token=4c6af5a6a2c8e7862e51b7761695e6e88e768a3'
}


def download_lrb(stock_id):
	lrb_base_url = 'http://api.xueqiu.com/stock/f10/incstatement.csv?page=1&size=10000&symbol='
	url = lrb_base_url + stock_id
	r = requests.get(url, headers=headers)
	filename = url.split('=')[-1] + '_lrb.csv'
	print("下载利润表...保存为:", filename)
	with open(filename, 'wb') as f:
		f.write(r.content)


def download_fzb(stock_id):
	fzb_base_url = 'http://api.xueqiu.com/stock/f10/balsheet.csv?page=1&size=10000&symbol='
	url = fzb_base_url + stock_id
	r = requests.get(url, headers=headers)
	filename = url.split('=')[-1] + '_fzb.csv'
	print("下载负债表...保存为:", filename)
	with open(filename, 'wb') as f:
		f.write(r.content)


def download_llb(stock_id):
	llb_base_url = 'http://api.xueqiu.com/stock/f10/cfstatement.csv?page=1&size=10000&symbol='
	url = llb_base_url + stock_id
	r = requests.get(url, headers=headers)
	filename = url.split('=')[-1] + '_llb.csv'
	print("下载流量表...保存为:", filename)
	with open(filename, 'wb') as f:
		f.write(r.content)


def find_code(stock_id, stock_lib, comp_lib):
	if (stock_id[0] >= u'\u4e00') and (stock_id <= u'\u9fa5'):
		if stock_id in comp_lib:
			return True
	else:
		if stock_id in stock_lib:
			return True
	return False

def download_data(stock_id):
	try:
		download_lrb(stock_id)
		download_fzb(stock_id)
		download_llb(stock_id)
	except BaseException:
		print("下载失败——请联网或者重新下载...")
	else:
		print("下载三表数据完成...")


def remove_csv(stock_id):
	os.remove('./{}_lrb.csv'.format(stock_id))
	os.remove('./{}_fzb.csv'.format(stock_id))
	os.remove('./{}_llb.csv'.format(stock_id))
	print('删除临时csv文件完成...')


def remove_db():
	db_files = []
	files = os.listdir('./')
	for file in files:
		if file.find('_data.db') >= 0:
			db_files.append(file)
	# print(db_files)
	for db_file in db_files:
		os.remove('./{0}'.format(db_file))
		print('删除临时{0}文件完成...'.format(db_file))



def load_code():
	stock_lib = []
	comp_lib = []
	with open('code.txt', 'r', encoding='utf-8') as f:
		for line in f:
			data = line.strip('\n').split(';')
			stock_lib.append(data[0])
			comp_lib.append(data[1])
	return stock_lib, comp_lib


def select_col(stock_id, col, db):
	conn = sqlite3.connect("{}_data.db".format(stock_id))
	cursor = conn.cursor()
	result = cursor.execute("select {0} from {1}".format(col, db))
	arr = []
	for row in result:
		arr.append(row[0])
	return arr


def get_time_list(stock_id):
	time_list = select_col(stock_id, '报表期截止日', 'main.lrb')
	time_list = [str(i) for i in time_list]
	time_list = time_list[::-1]
	time_1 = [datetime.datetime.strptime(d, '%Y%m%d').date() for d in time_list]

	time_list = select_col(stock_id, '报表日期', 'main.fzb')
	time_list = [str(i) for i in time_list]
	time_list = time_list[::-1]
	time_2 = [datetime.datetime.strptime(d, '%Y%m%d').date() for d in time_list]

	time_list = select_col(stock_id, '报表期截止日', 'main.llb')
	time_list = [str(i) for i in time_list]
	time_list = time_list[::-1]
	time_3 = [datetime.datetime.strptime(d, '%Y%m%d').date() for d in time_list]

	min_length = min(len(time_1), len(time_2), len(time_3))
	for i in [time_1, time_2, time_3]:
		if len(i) == min_length:
			time_list = i
			break
	# print(len(time_list))
	return time_list


def Profitability_Analysis(stock_id):  # 获利能力分析
	time_list = get_time_list(stock_id)
	"""
	
	营业毛利率: (营业收入 - 营业成本) / 营业收入 
	
	营业净利率: 净利润 / 营业总收入
	
	所有者权益报酬率: 净利润 / 所有者权益 
	
	资产报酬率: (净利润 + 利息支出 + 所得税费用) / 资产总计
	
	"""
	yysr = select_col(stock_id, '营业收入', 'main.lrb')[::-1]
	yycb = select_col(stock_id, '营业成本', 'main.lrb')[::-1]
	jlr = select_col(stock_id, '净利润', 'main.lrb')[::-1]
	yyzsr = select_col(stock_id, '营业总收入', 'main.lrb')[::-1]
	syzqy = select_col(stock_id, '[所有者权益(或股东权益)合计]', 'main.fzb')[::-1]
	lxzc = select_col(stock_id, '利息支出', 'main.lrb')[::-1]
	sdsfy = select_col(stock_id, '所得税费用', 'main.lrb')[::-1]
	zczj = select_col(stock_id, '资产总计', 'main.fzb')[::-1]

	# 资产报酬率:	(净利润 + 利息支出 + 所得税费用) / 资产总计
	zcbcl = [(jlr[i] + lxzc[i] + sdsfy[i]) / zczj[i] for i in range(len(time_list))]

	# 营业毛利率:	（营业收入 - 营业成本） / 营业收入
	yymll = [(yysr[i] - yycb[i]) / yysr[i] for i in range(len(time_list))]

	# 所有者权益报酬率: 净利润 / 所有者权益
	syzqybcl = [jlr[i] / syzqy[i] for i in range(len(time_list))]

	# 营业净利率: 净利润 / 营业总收入
	yyjll = [jlr[i] / yyzsr[i] for i in range(len(time_list))]

	return yymll, yyjll, syzqybcl, zcbcl, time_list


def Solvency_analysis(stock_id):  # 偿债能力分析
	time_list = get_time_list(stock_id)

	"""
	
	流动比率:流动资产合计/流动负债合计
	
	利息保障倍数:营业利润/财务费用
	
	"""
	ldzchj = select_col(stock_id, '流动资产合计', 'main.fzb')[::-1]
	ldfzhj = select_col(stock_id, '流动负债合计', 'main.fzb')[::-1]
	yylr = select_col(stock_id, '营业利润', 'main.lrb')[::-1]
	cwfy = select_col(stock_id, '财务费用', 'main.lrb')[::-1]

	# 流动比率:流动资产合计/流动负债合计
	ldbl = [ldzchj[i] / ldfzhj[i] for i in range(len(time_list))]
	# 利息保障倍数:营业利润/财务费用
	lxbzbs = [yylr[i] / cwfy[i] for i in range(len(time_list))]

	return ldbl, lxbzbs, time_list


def Economic_efficiency_analysis(stock_id):  # 经济效率分析
	time_list = get_time_list(stock_id)

	"""
	存货周转率:营业成本/存货
	
	应收账款周转率:营业收入/应收帐款
	
	总资产周转率:营业收入/资产总计
	"""
	yycb = select_col(stock_id, '营业成本', 'main.lrb')[::-1]
	ch = select_col(stock_id, '存货', 'main.fzb')[::-1]
	yysr = select_col(stock_id, '营业收入', 'main.lrb')[::-1]
	zchj = select_col(stock_id, '资产总计', 'main.fzb')[::-1]
	yszk = select_col(stock_id, '应收账款', 'main.fzb')[::-1]

	# 存货周转率:营业成本/存货
	chzzl = [yycb[i] / ch[i] for i in range(len(time_list))]
	# 应收账款周转率:营业收入/应收帐款
	yszkzzl = [yysr[i] / yszk[i] for i in range(len(time_list))]
	# 总资产周转率:营业收入/资产总计
	zzczzl = [yysr[i] / zchj[i] for i in range(len(time_list))]

	return chzzl, yszkzzl, zzczzl, time_list


def Financial_Structure_Analysis(stock_id):  # 财务结构分析
	time_list = get_time_list(stock_id)

	"""
	所有者权益比率:所有者权益/资产总计
	
	负债比率:负债合计/资产总计
	"""
	zczj = select_col(stock_id, '资产总计', 'main.fzb')[::-1]
	syzqy = select_col(stock_id, '[所有者权益(或股东权益)合计]', 'main.fzb')[::-1]
	fzhj = select_col(stock_id, '负债合计', 'main.fzb')[::-1]

	# 所有者权益比率:所有者权益/资产总计
	syzqybl = [syzqy[i] / zczj[i] for i in range(len(time_list))]
	# 负债比率:负债合计/资产总计
	fzbl = [fzhj[i] / zczj[i] for i in range(len(time_list))]

	return syzqybl, fzbl, time_list


if __name__ == '__main__':
	stock_id = input()
	stock_lib, comp_lib = load_code()
	if find_code(stock_id, stock_lib, comp_lib):
		download_data(stock_id)
		create_data(stock_id)
	# remove_db(stock_id)
	# Profitability_Analysis()
	# Solvency_analysis()
	#print(Economic_efficiency_analysis(stock_id))
	#print(Financial_Structure_Analysis(stock_id))
	#print(Solvency_analysis(stock_id))
	#print(Profitability_Analysis(stock_id))
