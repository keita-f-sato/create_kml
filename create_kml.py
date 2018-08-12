import simplekml
import pandas as pd
import numpy as np
import os
import csv
import shutil
import pyproj


file_list = os.listdir(os.path.curdir)
point_data = []
to_kml = []


print('1:長崎県 鹿児島県のうち北方北緯32度南方北緯27度西方東経128度18分東方東経130度を境界線とする区域内')
print('2:福岡県　佐賀県　熊本県　大分県　宮崎県　鹿児島県（I系に規定する区域を除く。)')
print('3:山口県　島根県　広島県')
print('4:香川県　愛媛県　徳島県　高知県')
print('5:兵庫県　鳥取県　岡山県')
print('6:京都府　大阪府　福井県　滋賀県　三重県　奈良県 和歌山県')
print('7:石川県　富山県　岐阜県　愛知県')
print('8:新潟県　長野県　山梨県　静岡県')
print('9:東京都（XIV系、XVIII系及びXIX系に規定する区域を除く。)　福島県　栃木県　茨城県　埼玉県 千葉県 群馬県　神奈川県')
print('10:青森県　秋田県　山形県　岩手県　宮城県')
print('11:北海道　小樽市 函館市 伊達市 北斗市 豊浦町 壮瞥町 洞爺湖町 北海道後志総合振興局の所管区域 北海道渡島総合振興局の所管地域 北海道檜山振興局の所管区域')
print('12:北海道 11および12以外')
print('13:北海道 北見市　帯広市　釧路市　網走市　根室市　美幌町　津別町　斜里町　清里町　小清水町　訓子府町　置戸町　佐呂間町　大空町　北海道十勝総合振興局の所管区域　北海道釧路総合振興局の所管区域　北海道根室振興局の所管区域')
print('14:小笠原村')
print('15:沖縄')

print('/////////////////////////////////////////////////////////////////////////////////////////////////')

print('日本測地系を数字のみ入力してください')
input_number = input('>>>  ')
Japan_Plane_Rectangular = 2442 + int(input_number)


sim_list = [s for s in file_list if '.sim' in s] #.simファイルを検索
name_list = [n.replace(".sim", "") for n in sim_list] #.simファイルのファイル名のリスト作成
shutil.copyfile("./%s"%sim_list[0], "./%s1.sim"%name_list[0]) #.simファイルをcsvに変換する前にコピーを作成

for sim , name in zip(sim_list , name_list): #.simファイルを.csvに変換
    os.rename(sim, name+ '.csv')

file_list = os.listdir(os.path.curdir) #ファイルリスト更新
csv_list = [s for s in file_list if '.csv' in s] #csvのファイルリストを作成

csv_file = open('./%s' % csv_list[0], "r", encoding="SHIFT-JIS", errors="", newline="" )
f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

for row in f:
    point_data.append(row)

point_data = [p for p in point_data if len(p) >= 6] #座標データのある行だけピックアップ
point_data_df = pd.DataFrame(point_data) #データフレーム化

df = point_data_df.iloc[0:,2:]
xy = point_data_df.iloc[0:,3:]
xy = xy.values.tolist()

for i in xy:
    y = float(i[0])
    x = float(i[1])

    p = pyproj.Proj(init='epsg:%s' % Japan_Plane_Rectangular)
    lat,lon = p(x,y,inverse=True) #平面直角座標を経度緯度に変換

    to_kml.append([lat,lon,i[2]])

df = df.values.tolist()

kml = simplekml.Kml()

for point,name in zip(to_kml,df):
    kml.newpoint(name=name[0], coords=[(point[0], point[1], point[2])])

kml.save('%s.kml'%name_list[0]) #kmlファイル作成
point_data_df.to_csv('%s.csv'%name_list[0]) #csvファイル作成
