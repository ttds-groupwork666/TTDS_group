#coding=utf-8
#programmer: Xinyue Sheng
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
from collections import defaultdict
import json
import xml.etree.ElementTree as ET
import os


def getHTMLText(url):
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		if "出错了" in r.text:
			return 0
		else:
			return r.text
	except:
		return 0

def findLyrics(url,n):
	html = getHTMLText(url)
	if html != 0:
		soup = BeautifulSoup(html, 'html.parser')
		txt = [y for y in [str(x).strip() for x in soup.p.contents if str(x)!='<br/>' and "欢迎您的光临" not in str(x) and "谢谢欣赏" not in str(x) and "www.90lrc.cn" not in str(x) and 'QQ' not in str(x)] if y != '']		
		song_info = {'id':n, 'song':txt[0],'singer':txt[1],'album':txt[2],'lyric':("\n").join(txt[3:])}	
		print(txt[1], n, txt[0]) #print the process
		n = n + 1
		return song_info,n
	else:
		return {},n

def findSongs(url,n):
	html = getHTMLText(url)
	song_list = []
	if html != 0:
		soup = BeautifulSoup(html,'html.parser')
		singer_list = soup('a')
		song_link = []
		for link in singer_list:
			song_id = link.attrs['href']
			if 'geci' in song_id:
				song_url = 'https://www.90lrc.cn/'+song_id
				song_info,n = findLyrics(song_url,n)
				if song_info != {}:
					song_list.append(song_info)
	return song_list,n

def findSingers(url, singer_dict,n):
	new_singer = {}
	html = getHTMLText(url)
	if html != 0:
		soup = BeautifulSoup(html,'html.parser')
		for s in soup('div','gs'):
			singers = s('a',href=re.compile('/geshou/*'))
			for p in singers:
				if p.string not in singer_dict:
					singer_url = "https://www.90lrc.cn"+p.attrs['href']	
					# test = 'https://www.90lrc.cn/geshou/103434.html' #test
					singer_song_list,n = findSongs(singer_url, n)
					new_singer[p.string] = 1
					saveXML(singer_song_list)

	return new_singer,n

def saveXML(singer_song_list):
	if os.path.exists('music.xml') == False:
		root = ET.Element("music")
		for i in singer_song_list:
			song = ET.SubElement(root,"song")
			ET.SubElement(song,"id").text = str(i['id'])
			ET.SubElement(song,"songname").text = i['song']
			ET.SubElement(song,"singer").text = i['singer']
			ET.SubElement(song,"album").text = i['album']
			ET.SubElement(song,"lyric").text = i['lyric']
		tree = ET.ElementTree(root)
		tree.write("music.xml",encoding='utf-8')
	else:
		tree = ET.parse('music.xml')
		root = tree.getroot()
		for i in singer_song_list:
			song = ET.SubElement(root,"song")
			ET.SubElement(song,"id").text = str(i['id'])
			ET.SubElement(song,"songname").text = i['song']
			ET.SubElement(song,"singer").text = i['singer']
			ET.SubElement(song,"album").text = i['album']
			ET.SubElement(song,"lyric").text = i['lyric']
		tree = ET.ElementTree(root)
		tree.write("music.xml",encoding='utf-8')


def main():
	website = "https://www.90lrc.cn/"
	singer_dict = 'singer_dict.json'
	n = 1
	if os.path.exists(singer_dict) == True:
		with open(singer_file,'a+') as f:
			singer_dict = json.loads(singer_file)
			new_singer,n = findSingers(website, singer_dict,n)
			json_str = json.dumps(new_singer, index = 4)
			f.write(json_str)
		f.close()
	else:
		singer_dict = {}
		new_singer,n = findSingers(website, singer_dict,n)
		json_str = json.dumps(new_singer, index = 4)
		with open(singer_dict,'a+') as f:
			f.write(json_str)
		f.close()


main()



