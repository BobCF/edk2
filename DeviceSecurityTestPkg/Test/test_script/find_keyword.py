import re
import sys
import os
import codecs

class logprocessor:



	def __init__(self, LogPath, KeywordPath):
		print("========================== new test case begin ============================\n")
		self.LogPath = LogPath
		self.KeywordPath = KeywordPath
		self.ExpectKeywordLines, self.ErrorKeywordLines = self.GetKeywords(self.KeywordPath)
		self.LogContent = self.GetLogContent(self.LogPath)
		pass
		
	def Check(self):
		Result = False
		
		print("\n*************try to find Keyword in the log ......\n")
		for line in self.ExpectKeywordLines:
			if(line in self.LogContent):
				Result=True
			else:
				Result = False
				print("\n***Can not find the following ExpectKeyword in the log!!!\n")
				print(line)
				break

		if (not Result):
			print("\n***not found ExpectKeyword in the log!!!\n")
			print("*** So this test case failed :(\n")
			print("******************************************************\n")
			return

		for line in self.ErrorKeywordLines:
			if(line not in self.LogContent):
				Result=True
			else:
				Result = False
				print("\n***find the following ErrorKeyword in the log!!!\n")
				print(line)
				break
			
		if (Result):
			print("\n***found all ExpectKeywords and not found any ErrorKeyword in the log :-)")
			print("*** So this test case passed :-)\n")
		else:
			print("\n***found ErrorKeyword in the log!!!")
			print("*** So this test case failed :(\n")
			
		print("******************************************************\n")
		pass

	def GetKeywords(self, KeywordPath):
		KeywordFile = open(KeywordPath, 'r')
		AllKeywordLines = KeywordFile.readlines()
		ExpectKeywordLines = []
		ErrorKeywordLines = []
		HaveErrorKeyword = False

		TargetKeywordLines = ExpectKeywordLines
		print("--------------------------ExpectKeywords list start------------------------\n")
		for line in AllKeywordLines:
			line = line.strip()
			if (not line):
				continue
			if (line.startswith('ErrorKeyword')):
				HaveErrorKeyword = True
				TargetKeywordLines = ErrorKeywordLines
				print("\n------------------------ExpectKeywords list end--------------------------\n")
				print("\n------------------------ErrorKeywords list start-------------------------\n")
				continue
			print(line)
			TargetKeywordLines.append(line)
		if (HaveErrorKeyword):
			print("\n------------------------ErrorKeywords list end---------------------------\n")
		else:
			print("\n------------------------ExpectKeywords list end--------------------------\n")
		KeywordFile.close()
		return ExpectKeywordLines, ErrorKeywordLines
		pass
		
	def GetLogContent(self, LogPath):
		LogFile = codecs.open(LogPath, 'r', 'utf-16le')
		LogFileLines = []
		for line in LogFile.readlines():
			line = line.strip()
			if (not line):
				continue
			LogFileLines.append(line)		
		LogFile.close()
		return LogFileLines
		pass
		
if __name__ == '__main__':

	if len(sys.argv) != 3:
		print("Usage:\n%s" % "  python find_Keyword.py <logFile> <KeywordFile> " )
		sys.exit(0)
	
	LogPath = sys.argv[1]
	KeywordPath = sys.argv[2]
	
	my_logprocessor = logprocessor(LogPath, KeywordPath)
	my_logprocessor.Check()
	
	pass

