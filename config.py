import json

class Config:
	def __init__(self):
		config_file = open("config.json", "r")
		config_dict: dict = json.load(config_file)
		config_file.close()

		self.homework: str = config_dict.get("homework", "")
		self.cookies: dict = config_dict.get("cookies", {})
		self.score: dict = config_dict.get("score", {"max": 100, "min": 100})
		self.remark: str = config_dict.get("remark", "请不要吝啬文字，评语至少5个字，但也不要乱写")
		self.start_question: int = config_dict.get("start_question", 0)
		self.start_student: int = config_dict.get("start_student", 0)
		self.log_level: str = config_dict.get("log_level", "INFO")
