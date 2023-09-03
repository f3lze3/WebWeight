# -*- encoding: utf-8 -*-
'''
@File 		:	WebWeight.py
@Time		:	2023/5/6 21:32:08
@Author		:	f3lze3
@Version	:	0.1
'''

import requests
from bs4 import BeautifulSoup
import warnings
from fake_useragent import UserAgent
import optparse
import colorama
from colorama import Fore, Style
import threading
from urllib.parse import urlparse
import csv
from time import sleep
from datetime import datetime
import os


warnings.filterwarnings("ignore")

colorama.init(autoreset=True)

RED = Fore.RED
GREEN = Fore.GREEN

BRIGHT = Style.BRIGHT


def banner():
	print(BRIGHT + Fore.BLUE + """
		$$\      $$\           $$\       $$\      $$\           $$\           $$\        $$\     
		$$ | $\  $$ |          $$ |      $$ | $\  $$ |          \__|          $$ |       $$ |    
		$$ |$$$\ $$ | $$$$$$\  $$$$$$$\  $$ |$$$\ $$ | $$$$$$\  $$\  $$$$$$\  $$$$$$$\ $$$$$$\   
		$$ $$ $$\$$ |$$  __$$\ $$  __$$\ $$ $$ $$\$$ |$$  __$$\ $$ |$$  __$$\ $$  __$$\\_$$  _|  
		$$$$  _$$$$ |$$$$$$$$ |$$ |  $$ |$$$$  _$$$$ |$$$$$$$$ |$$ |$$ /  $$ |$$ |  $$ | $$ |    
		$$$  / \$$$ |$$   ____|$$ |  $$ |$$$  / \$$$ |$$   ____|$$ |$$ |  $$ |$$ |  $$ | $$ |$$\ 
		$$  /   \$$ |\$$$$$$$\ $$$$$$$  |$$  /   \$$ |\$$$$$$$\ $$ |\$$$$$$$ |$$ |  $$ | \$$$$  |
		\__/     \__| \_______|\_______/ \__/     \__| \_______|\__| \____$$ |\__|  \__|  \____/ 
		                                                            $$\   $$ |                   
		                                                            \$$$$$$  |                   
		                                                             \______/                    
		""")


def lookup(domain, seq, output, writer):
	weights = []

	print("[*] 域名：" + domain)

	if output:
		weights.append(seq)
		weights.append(domain)
	else:
		print()

	headers = {
		"User-Agent": UserAgent().random
	}

	proxies = {
		"HTTP": "127.0.0.1:10809",
		"HTTPS": "127.0.0.1:10809"
	}

	url = "https://www.aizhan.com/cha/" + domain

	try:
		response = requests.get(url, headers=headers, verify=False)

		html = response.text

		soup = BeautifulSoup(html, "lxml")

		imgs = soup.find_all("img")		

		for img in imgs:
			flag = img.get("alt")
			src = img.get("src")
			
			if not output:

				if flag and "br" in src and "mbr" not in src:
					print(BRIGHT + GREEN + "[+] 百度PC权重：" + flag)
				if flag and "mbr" in src:
					print(BRIGHT + GREEN + "[+] 百度移动权重：" + flag)
				if flag and "360" in src:
					print(BRIGHT + GREEN + "[+] 360权重：" + flag)
				if flag and "sm" in src:
					if flag == "n":
						print(BRIGHT + GREEN + "[+] 神马权重： 0")
					else:
						print(BRIGHT + GREEN + "[+] 百度PC权重：" + flag)
				if flag and "sr" in src:
					print(BRIGHT + GREEN + "[+] 搜狗权重：" + flag)
				if flag and "pr" in src:
					print(BRIGHT + GREEN + "[+] 谷歌权重：" + flag)

			else:
				if flag and "爱站网" not in flag:
					if flag == "n":
						weights.append("0")
					else:
						weights.append(flag)
		

		if writer:
			writer.writerow(weights)

		# print(imgs)

		sleep(3)

	except Exception as e:
		print(BRIGHT + RED + "[-] " + repr(e))


def main():
	banner()
	optparser = optparse.OptionParser("usage: python %s -u <url/domain>" % __file__)
	optparser.add_option("-u", "--url", dest="url", help="specify a url or domain")
	optparser.add_option("-f", "--file", dest="file", help="specify a filename")
	optparser.add_option("-o", "--output", dest="output", default=str(datetime.now()).replace(":", "-") + ".csv", help="specify a csv filename to output (default csv)")
	(options, args) = optparser.parse_args()

	url = options.url
	filename = options.file
	output = options.output

	if (not url) and (not filename and not output):
		print(optparser.usage)
		exit(0)

	elif url:
		domain = urlparse(url).netloc

		if domain == "":
			domain = urlparse(url).path
		

		lookup(domain, 0, None, None)

	elif filename and output:
		if "." not in output:
			output = output + ".csv"
		if not os.path.exists("output"):
			os.mkdir("output")


		f = open(filename, "r", encoding="utf-8")
		urls = f.readlines()
		f.close()

		header = ["序号", "域名", "百度PC权重", "百度移动权重", "360权重", "神马权重", "搜狗权重", "谷歌权重"]

		seq = 1

		output_path = os.path.join("output", output)

		with open(output_path, "w+", newline="") as f:
			writer = csv.writer(f)
			writer.writerow(header)

			for url in urls:
				domain = urlparse(url).netloc
				if domain == "":
					domain = urlparse(url).path

				lookup(domain.strip(), seq, output_path, writer)

				seq += 1

			f.close()

		print()
		print(f"已保存到 {output_path}")
	else:
		print(optparser.usage)
		exit(0)


if __name__ == '__main__':
	p = threading.Thread(target=main)
	p.start()
	p.join()
