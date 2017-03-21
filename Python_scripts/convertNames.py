import os

def main():
	workDir = "../txt_files/"
	for filename in os.listdir(workDir):
		print filename
		if not filename.endswith('.txt') and not filename.startswith('.'):
			actualName = filename[:-3]
			fullName = actualName + '.txt'
			print fullName
			print
			os.rename(workDir+filename, workDir+fullName)

if __name__ == '__main__':
	main()