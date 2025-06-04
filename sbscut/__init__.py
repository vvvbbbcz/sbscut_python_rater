import random
import requests
import time
from requests import Response

from sbscut.config import Config
from sbscut.data_helper import *
from sbscut.get_page import post, submit
from sbscut.html_parser import HTMLParser
from sbscut.logger import logger, init_logger
from sbscut.status_code_helper import status_code_log

url = "https://1024.se.scut.edu.cn/%E4%BD%9C%E4%B8%9A%E4%BA%92%E8%AF%84.aspx"

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
	# "Content-Type": "multipart/form-data",
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}


def main():
	parser: HTMLParser = HTMLParser()
	conf: Config = Config()

	homework: str = conf.homework
	cookies: dict = conf.cookies
	init_logger(conf.log_level)

	# get first page
	logger.info(f"Getting first page of homework {homework}...")
	first_page: Response = requests.get(url=url, cookies=cookies, headers=headers)
	parser.feed(first_page.text)
	first_page.close()

	data: dict = {
		"__EVENTARGUMENT": "",
		"__LASTFOCUS": "",
	}

	parser.set_data(data)

	# jump to first question
	data["__EVENTTARGET"] = "ctl00$MainContent$dropTitleList"
	data["ctl00$MainContent$dropTitleList"] = get_drop_title_list(homework, conf.start_question)
	data["ctl00$MainContent$dropStudent"] = get_drop_student(1)
	data = post(url, cookies, data, headers, parser, conf.start_question, 1)

	for question in range(conf.start_question, 51):
		if question != conf.start_question:
			# get next question
			data["__EVENTTARGET"] = "ctl00$MainContent$dropTitleList"
			data["ctl00$MainContent$dropTitleList"] = get_drop_title_list(homework, question)
			data = post(url, cookies, data, headers, parser, question, 1)

		for student in range(1, 4):
			# get next student
			if student != 1:
				data["__EVENTTARGET"] = "ctl00$MainContent$dropStudent"
				data["ctl00$MainContent$dropStudent"] = get_drop_student(student)
				data = post(url, cookies, data, headers, parser, question, student)
			else:
				data["ctl00$MainContent$dropStudent"] = get_drop_student(student)

			# submit score
			data["__EVENTTARGET"] = ""  # reset __EVENTTARGET
			data["ctl00$MainContent$dropScore"] = random.randint(conf.score["min"], conf.score["max"])
			data["ctl00$MainContent$btnScore"] = "提交"
			data["ctl00$MainContent$txtRemark"] = conf.remark

			data = submit(url, cookies, data, headers, parser)
			data.pop("ctl00$MainContent$btnScore")  # unset btnScore
			data.pop("ctl00$MainContent$txtRemark")  # unset txtRemark


if __name__ == '__main__':
	main()
