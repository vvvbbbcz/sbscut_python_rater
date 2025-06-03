import random
import requests
import time
from requests import Response

from config import Config
from data_helper import *
from html_parser import HTMLParser
from logger import logger
from status_code_helper import status_code_log

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
	logger.setLevel(conf.log_level)

	# get first page
	logger.info("Getting first page of homework " + homework + "...")
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
	data["ctl00$MainContent$dropStudent"] = get_drop_student(conf.start_question)

	status_code: int = 0
	while status_code != 200:
		try:
			logger.info(f"Getting question {conf.start_question}...")
			next_question: Response = requests.post(url=url, cookies=cookies, headers=headers, data=data)
			status_code = next_question.status_code
			parser.feed(next_question.text)
			next_question.close()

			status_code_log(status_code, f"get question {conf.start_question}")

			if status_code != 200:
				time.sleep(1.0)
		except Exception as e:
			logger.error(f"Failed to get question {conf.start_question}, exception: {e}")
			logger.info("Waiting for 1 second...")
			time.sleep(1.0)
	parser.set_data(data)

	for question in range(conf.start_question, 51):
		if question != conf.start_question:
			# get next question
			data["__EVENTTARGET"] = "ctl00$MainContent$dropTitleList"
			data["ctl00$MainContent$dropTitleList"] = get_drop_title_list(homework, question)

			status_code: int = 0
			while status_code != 200:
				try:
					logger.info("Getting question " + str(question) + "...")
					next_question: Response = requests.post(url=url, cookies=cookies, headers=headers, data=data)
					status_code = next_question.status_code
					parser.feed(next_question.text)
					next_question.close()

					status_code_log(status_code, "get question " + str(question))

					if status_code != 200:
						time.sleep(1.0)
				except Exception as e:
					logger.error("Failed to get question " + str(question) + ", exception: " + str(e))
					logger.info("Waiting for 1 second...")
					time.sleep(1.0)
			parser.set_data(data)

		for student in range(1, 4):
			# get next student
			if student != 1:
				data["__EVENTTARGET"] = "ctl00$MainContent$dropStudent"
				data["ctl00$MainContent$dropStudent"] = get_drop_student(student)

				status_code: int = 0
				while status_code != 200:
					try:
						logger.info("Getting student " + str(student) + "...")
						next_student: Response = requests.post(url=url, cookies=cookies, headers=headers, data=data)
						status_code = next_student.status_code
						parser.feed(next_student.text)
						next_student.close()

						status_code_log(status_code, "get student " + str(student))

						if status_code != 200:
							time.sleep(1.0)
					except Exception as e:
						logger.error("Failed to get student " + str(student) + ", exception: " + str(e))
						logger.info("Waiting for 1 second...")
						time.sleep(1.0)
				parser.set_data(data)
			else:
				data["ctl00$MainContent$dropStudent"] = get_drop_student(student)

			# submit score
			data["__EVENTTARGET"] = ""  # reset __EVENTTARGET
			data["ctl00$MainContent$dropScore"] = random.randint(conf.score["min"], conf.score["max"])
			data["ctl00$MainContent$btnScore"] = "提交"
			data["ctl00$MainContent$txtRemark"] = conf.remark

			status_code = 0
			while status_code != 200:
				try:
					logger.info("Submitting score...")
					score: Response = requests.post(url=url, cookies=cookies, headers=headers, data=data)
					status_code = score.status_code
					parser.feed(score.text)
					score.close()

					status_code_log(status_code, "submit score")

					logger.info("Waiting for 15 seconds...")
					time.sleep(15.0)
				except Exception as e:
					logger.error("Failed to submit score, exception: " + str(e))

			# set data
			parser.set_data(data)
			data.pop("ctl00$MainContent$btnScore") # unset btnScore
			data.pop("ctl00$MainContent$txtRemark") # unset txtRemark

if __name__ == '__main__':
	main()
