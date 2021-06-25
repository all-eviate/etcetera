import numpy as np
import pandas as pd
import pickle
import math
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


class DB:
    def __init__(self):
        self.ch_id = []
        self.ch_name = []
        self.ch_bizno = []
        self.ch_date0 = []
        self.ch_date1 = []
        self.ch_date2 = []
        self.ch_who = []
        self.ch_cat = []
        self.ch_den_count = []
        self.ch_den_total = []
        self.ch_den_db = []
        self.ch_den = []

    def set_header(self, ch_id, ch_name, ch_bizno, ch_date0, ch_date1, ch_date2, ch_who, ch_cat, ch_den_count, ch_den_total, ch_den_db, ch_den):
        self.ch_id.append(ch_id)
        self.ch_name.append(ch_name)
        self.ch_bizno.append(ch_bizno)
        self.ch_date0.append(ch_date0)
        self.ch_date1.append(ch_date1)
        self.ch_date2.append(ch_date2)
        self.ch_who.append(ch_who)
        self.ch_cat.append(ch_cat)
        self.ch_den_count.append(ch_den_count)
        self.ch_den_total.append(ch_den_total)
        self.ch_den_db.append(ch_den_db)
        self.ch_den.append(ch_den)

    def set_property(self, ch_id, ch_name, ch_bizno, ch_date0, ch_date1, ch_date2, ch_who, ch_cat, ch_den_count, ch_den_total, ch_den_db, ch_den):
        for i in range(len(ch_den_db)):
            self.ch_id.append(ch_id)
            self.ch_name.append(ch_name)
            self.ch_bizno.append(ch_bizno)
            self.ch_date0.append(ch_date0)
            self.ch_date1.append(ch_date1)
            self.ch_date2.append(ch_date2)
            self.ch_who.append(ch_who)
            self.ch_cat.append(ch_cat)
            self.ch_den_count.append(ch_den_count[i])
            self.ch_den_total.append(ch_den_total[i])
            self.ch_den_db.append(ch_den_db[i])
            self.ch_den.append(ch_den)

    def save(self, path):
        row = {'프로필 ID': self.ch_id,
               '프로필명': self.ch_name,
               '사업자 번호': self.ch_bizno,
               '심사 요청일': self.ch_date0,
               '심사 처리일': self.ch_date1,
               '심사 처리일2': self.ch_date2,
               '심사 처리자': self.ch_who,
               '처리 분류': self.ch_cat,
               '당일 반려 횟수': self.ch_den_count,
               '반려 사유 수': self.ch_den_total,
               '반려 사유 DB': self.ch_den_db,
               '반려 사유': self.ch_den}
        df = pd.DataFrame(row)
        df.to_csv(path, mode='a', encoding='euc-kr', index=False, header=False)


def save_csv(df, save_path, duplicated_drop_list=['프로필 ID']):
    try:
        df.drop_duplicates(duplicated_drop_list, keep='first')
        df.to_csv(save_path, encoding='euc-kr', index=False)
        print('csv 생성완료')
    except:
        duplicated_drop_list = ['id']
        df.drop_duplicates(duplicated_drop_list, keep='first')
        df.to_csv(save_path, encoding='euc-kr', index=False)
        print('csv 생성완료')


input_path = 'dendb_input.csv'
save_path = 'dendb_output.csv'
with open('comment.pickle', 'rb') as fr:
    comment = pickle.load(fr)

inf = pd.read_csv(input_path, encoding='euc-kr')
in_id_array = inf['id']
in_name_array = inf['name']
in_bizno_array = inf['bizno']
in_date0_array = inf['date0']
in_date1_array = inf['date1']
in_date2_array = inf['date2']
in_who_array = inf['who']
in_cat_array = inf['cat']
in_den_count_array = inf['den_count']
in_den_total_array = inf['den_total']
in_den_db_array = inf['den_db']
in_den_array = inf['den']
in_check_array = inf['check']

if type(in_check_array[0]) != str:
    db = DB()
    db.set_header('프로필 ID', '프로필명', '사업자 번호', '심사 요청일', '심사 처리일', '심사 처리일2',
                  '심사 처리자', '처리 분류', '당일 반려 횟수', '반려 사유 수', '반려 사유 DB', '반려 사유')
    db.save(save_path)


for i, ch_id in enumerate(in_id_array):
    if type(in_check_array[i]) == str:
        print('continue')
        continue
    ch_den_db = []
    ch_name = in_name_array[i]
    ch_bizno = in_bizno_array[i]
    ch_date0 = in_date0_array[i]
    ch_date1 = in_date1_array[i]
    ch_date2 = in_date2_array[i]
    ch_who = in_who_array[i]
    ch_cat = in_cat_array[i]
    ch_den_count = []
    ch_den_total = []
    ch_den = in_den_array[i]
    print(ch_id)

    begin = ch_den.find('[사유]')
    trim0 = ch_den[begin+4:]
    trim1 = trim0.replace(' ', '')
    if '총' in trim1:
        total_dens = int(trim1[trim1.find('총')+1])
    else:
        total_dens = 1
    ch_den_count.append(1)
    ch_den_total.append(total_dens)

    for a in range(total_dens - 1):
        ch_den_count.append(a+2)
        ch_den_total.append(0)

    first = 1
    while total_dens > 0:
        total_dens -= 1
        start = trim0.find('[') + 1
        end = trim0.find(']')
        den = trim0[start:end].strip()
        if '마스킹' in den:
            escape = trim0.find('\r\n', end)
            detail = trim0[end:escape].replace(' ', '')
            if '누락' in den:
                if '사업자등록증명내' in detail:
                    den = '누락_사업자등록증명'
                elif '사업자등록증내' in detail or '사업자등록증상단내' in detail:
                    den = '누락_사업자등록증'
                elif '신분증' in detail:
                    den = '누락_신분증'
                elif '재직증명서' in detail:
                    den = '누락_재직'
                elif '통신판매업' in detail:
                    den = '누락_통신판매업'
                elif '고유번호증' in detail:
                    den = '누락_고유번호증'
            elif '오류' in den:
                if '사업자등록증명내' in detail:
                    den = '오류_사업자등록증명'
                elif '사업자등록증내' in detail:
                    den = '오류_사업자등록증'
                elif '신분증' in detail:
                    den = '오류_신분증'
                elif '재직증명서' in detail:
                    den = '오류_재직'
                elif '고유번호증' in detail:
                    den = '오류_고유번호증'
        elif '사업자등록증과신청기재정보<' in den.replace(' ', '') and '>불일치' in den.replace(' ', ''):
            den = '사업자-신청 기재 정보 불일치'
        elif '고유번호증과신청기재정보<' in den.replace(' ', '') and '>불일치' in den.replace(' ', ''):
            den = '고유번호증-신청 기재 정보 불일치'
        print(den)
        if den in comment:
            ch_den_db.append(comment[den])
            print("FOUND!")
        else:
            if first > 0:
                print(ch_cat)
                m = input("MATCH? : ")
                if m == '':
                    reg = input("register? (y) : ")
                    if reg == 'y':
                        comment[den] = ch_cat
                        with open('comment.pickle', 'wb') as fw:
                            pickle.dump(comment, fw)
                        print('added to dict')
                    ch_den_db.append(ch_cat)
                else:
                    reg = input("register? (y) : ")
                    if reg == 'y':
                        comment[den] = m
                        with open('comment.pickle', 'wb') as fw:
                            pickle.dump(comment, fw)
                        print('added to dict')
                    ch_den_db.append(m)
            else:
                m = input("Input comment : ")
                reg = input("register? (y) : ")
                if reg == 'y':
                    comment[den] = m
                    with open('comment.pickle', 'wb') as fw:
                        pickle.dump(comment, fw)
                    print('added to dict')
                ch_den_db.append(m)
        first -= 1
        trim0 = trim0[end+1:]
    db = DB()
    db.set_property(ch_id, ch_name, ch_bizno, ch_date0, ch_date1, ch_date2,
                    ch_who, ch_cat, ch_den_count, ch_den_total, ch_den_db, ch_den)
    db.save(save_path)

    in_check_array[i] = 'O'
    save_csv(inf, input_path)
