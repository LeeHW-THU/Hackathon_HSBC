import pandas as pd
import baostock as bs
def dupontROE(stock_id,quarter):
	stock_id=stock_id.lower()
	stock_id=stock_id[0:2]+'.'+stock_id[2:]
	dupont_list = []
	s1_dupont = bs.query_dupont_data(code=stock_id, year=2018, quarter=quarter)
	while (s1_dupont.error_code == '0') & s1_dupont.next():
		dupont_list.append(s1_dupont.get_row_data())
	s1 = pd.DataFrame(dupont_list, columns=s1_dupont.fields)
	s1 = float(s1['dupontROE'].values[0])
	return s1

def roeAvg(stock_id):
	return ((dupontROE(stock_id,1)+dupontROE(stock_id,2)+dupontROE(stock_id,3)+dupontROE(stock_id,4))/4)
