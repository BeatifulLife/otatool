import os


class fileHelper:
	@staticmethod
	def getFileSize(filepath: str):
		assert(filepath is not None)
		if os.path.exists(filepath):
			return os.path.getsize(filepath)
		else:
			raise Exception("getFileSize: File doest't exitst:", filepath)
			return 0

	@staticmethod
	def getFileModfifyTimeStamp(filepath: str):
		assert(filepath is not None)
		if os.path.exists(filepath):
			return os.path.getmtime(filepath)
		else:
			raise Exception("getFileModfifyTimeStamp: File doest't exitst:", filepath)
			return 0.0

	@staticmethod
	def getFileCreateTimeStamp(filepath: str):
		assert(filepath is not None)
		if os.path.exists(filepath):
			return os.path.getmtime(filepath)
		else:
			raise Exception("File doest't exitst:", filepath)
			return 0.0

	@staticmethod
	def getFileAccessTimeStamp(filepath: str):
		assert(filepath is not None)
		if os.path.exists(filepath):
			return os.path.getatime(filepath)
		else:
			raise Exception("getFileAccessTimeStamp: File doest't exitst:", filepath)
			return 0.0

