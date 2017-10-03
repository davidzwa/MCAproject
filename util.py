import os
from datetime import datetime
from openpyxl import Workbook

def createTimeFolder():
	reldir = datetime.now().strftime('run-%d-%m/%H-%M-%S')
	fulldir = os.path.join(os.getcwd(), reldir)
	os.makedirs(fulldir)
	return (fulldir,reldir)

def createFolder(subFolder):
	os.makedirs(subFolder)
	return subFolder

def writeClusters(lines, numClusters):
	for index3, line in enumerate(lines):
		if numClusters[0] in line:
			lines[index3] = numClusters[0] + ' ' + str(numClusters[1]) + '\n'
			print('--Compiler flag found and updated: ' + numClusters[0] + ' ' + str(numClusters[1]))
	return lines

def replaceLine(strAttribute, numVal, lines):
	
	for index3, line in enumerate(lines):
		# Remove double spaces and force single spaces
		strAttribute = ' ' + ' '.join(strAttribute.split()) + ' '
		
		# Check if attribute found
		if strAttribute in line:
			line_spl = ' '.join(line.split()).split(strAttribute)
			
			# Expect two splitted indices in line_spl
			if len(line_spl) == 2:
				lines[index3] = line_spl[0] + strAttribute + str(numVal) + '\n'
				return lines
			else:
				print('Failed split in line. Line 2be replaced: [' + line + '] with [name:' + strAttribute + ',numVal:' + str(numVal) +']')
				return False
	
	print('Could not find [name:' + strAttribute + ',numVal:' + str(numVal) +'] in configuration.mm')
	return False

def findLogLine(strAttribute, log_fname):
	
	with open(log_fname,'r') as f:
		sim_lines = f.readlines()
		for sim_line in sim_lines:
			if strAttribute in sim_line:
				log_line_str = ' '.join(sim_line.split()).split(strAttribute)[1].replace(' ','')
				log_line_int = int(log_line_str.split('(')[0])				
				return log_line_int
	return False

def findLogLines(strAttributes, log_fname):
	
	result = list()	 
	with open(log_fname,'r') as f:
		sim_lines = f.readlines()
		for sim_line in sim_lines:
			for strAttribute in strAttributes:
				attr = strAttribute[0]
				title = strAttribute[1]
				if attr in sim_line:
					log_val_str = ' '.join(sim_line.split()).split(attr)[1].replace(' ','')
					log_val = log_val_str.split('(')[0]
					result.append(log_val)
					break
	return result

def findConfigLines(lines):
	
	result_attr = list()
	result_val = list()
	for line in lines:
		# Find every line with RES or REG
		attr = ''
		if 'REG:' in line: 
			attr = 'REG:'
		elif 'RES:' in line:
			attr = 'RES:'
			
		if attr != '':
			config_str = ' '.join(line.split()).split(attr)[1]
			result_attr.append(config_str.split()[0])
			result_val.append(config_str.split()[1])
	return(result_attr,result_val)
			