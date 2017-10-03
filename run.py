import errno, os, subprocess
import sys; sys.dont_write_bytecode = True
from util import *				# Directory creation
from settings import *			# Simulation settings, output requirements and initial values
from openpyxl import Workbook

(fulldir,reldir) = createTimeFolder()

# Read default configuration
with open(fname) as f:
	lines = f.readlines()
CONFIG_HEADERS = findConfigLines(lines)[0]
writeClusters(lines, CONST_NUM_CLUSTERS)	# Set amount of clusters before simulation

# Initialize simulation containers
i = 0
optimal_exec_cycles = [-1,-1]
optimal_sim_i = [-1,-1]
sim_results = []
wb = Workbook()
ws1 = wb.active
ws1.title = 'Sim Data'
ws1.append(['CLUSTER_SIZE: ' + str(CONST_NUM_CLUSTERS)])
CONST_DATA_NAMES.extend(CONFIG_HEADERS)
ws1.append(CONST_DATA_NAMES)

for ALTER_PROPERTY in CONST_SIM_ALTER:
	strAttribute = ALTER_PROPERTY[0]
	numVals = ALTER_PROPERTY[1]
	if len(ALTER_PROPERTY) == 3 and ALTER_PROPERTY[2] == 'skip':
		new_config = replaceLine(strAttribute, numVals[0], lines)
		if new_config:
			print('[' + str(i) + '] SKIP AND SET: [name:' + strAttribute + ', numVal:' + str(numVals[0]) + ' ]')
			lines = new_config
		continue
		
	for numVal in numVals:
		i+=1
		pass_string = 'NO ACTION PERFORMED'
	
		old_lines = lines # backup
		new_config = replaceLine(strAttribute, numVal, lines)
		if not new_config:
			continue	# Line error, skip sim
		else:
			lines = new_config
			pass_string = 'CHANGE: [name:' + strAttribute + ', numVal:' + str(numVal) + ' ]'
			
			# Create folder to store files in
			out_execpath = reldir + "/config" + str(i) + "/"
			out_fpath = out_execpath + "/" + fname_new + ext
			createFolder(out_execpath)
			with open(out_fpath,'w+') as f:
				f.writelines(lines)
		
			sim_result_string = '[' + str(i) + '] '
			LOG_DATA = list()
			for index, iter_alg in enumerate(iter_algs):
				
				# Execute subprocess
				cmd = ["run", iter_alg, "-O3"]
				p = subprocess.Popen(cmd,cwd=out_execpath, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				p.wait()
				
				try:
					log_file = out_execpath + "output-" + iter_alg + ".c/ta.log.000" 
					log_data = findLogLines(CONST_DATA_MULTI, log_file)
				
					exec_cycles = findLogLine(CONST_DATA_OUT, log_file)
					if not exec_cycles:
						print('Log property ' + CONST_DATA_OUT + ' not found')
						continue
					
					# Analyze optimal execution cycles value
					if (optimal_exec_cycles[index] == -1 or exec_cycles < optimal_exec_cycles[index]):
						optimal_exec_cycles[index] = exec_cycles
						optimal_sim_i[index] = i
					sim_result_string += iter_alg  + ': ' + str(exec_cycles) + ' ' 
					
					LOG_DATA.extend(log_data)
				except IOError:
					sim_result_string += 'FAILED [' + iter_alg + '] '
					lines = old_lines
			LOG_DATA.extend(findConfigLines(lines)[1])
			ws1.append(LOG_DATA)
			print(sim_result_string + pass_string)

wb.save(reldir + '/results.xlsx')
print('\n--Simulation finished-- Excel at: ' + reldir + '/results.xlsx')
print(iter_algs)
print(optimal_exec_cycles)
print(optimal_sim_i)