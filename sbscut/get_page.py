import time

import requests
from requests import Response

from sbscut.html_parser import HTMLParser
from sbscut.status_code_helper import status_code_log
from sbscut.logger import logger


def post(url: str, cookies: dict, data: dict, headers: dict, parser: HTMLParser, ques: int, stu: int) -> dict:
	status_code: int = 0
	while status_code != 200:
		try:
			logger.info(f"Getting question {ques}, student {stu}...")
			next_question: Response = requests.post(url=url, cookies=cookies, headers=headers, data=data)
			status_code = next_question.status_code
			parser.feed(next_question.text)
			next_question.close()

			status_code_log(status_code, f"get question {ques}, student {stu}")

			if status_code != 200:
				time.sleep(1.0)
		except Exception as e:
			logger.error(f"Failed to get question {ques}, student {stu}, exception: {e}")
			logger.info("Waiting for 1 second...")
			time.sleep(1.0)
	parser.set_data(data)
	return data

def submit(url: str, cookies: dict, data: dict, headers: dict, parser: HTMLParser) -> dict:
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
	parser.set_data(data)
	return data
