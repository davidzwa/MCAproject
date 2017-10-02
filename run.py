import errno
import os
from datetime import datetime
import subprocess

def createTimeStampFolder():
	reldir = datetime.now().strftime('run-%H-%M-%S')
	fulldir = os.path.join(os.getcwd(), reldir)
	os.makedirs(fulldir)
	return (fulldir,reldir)

def createFolder(subFolder):
	os.makedirs(subFolder)
	return subFolder

(fulldir,reldir) = createTimeStampFolder()
fname = 'configuration.mm-default'
fname_new = 'configuration'
ext = '.mm'

# Read default configuration
with open(fname) as f:
	lines = f.readlines()

# List of tuples to keep order as wanted
sim_alter = [
			('IssueWidth.0',	[4,8]),
			 ]

iter_algs = ['crc','greyscale']
sim_results = []
compiler_flag = ['# ***Clusters***', 1]		# Single setting, because otherwise simulation becomes too heavy

i = 0	# Simulation iterator index
optimal_exec_cycles = [-1,-1]
optimal_sim_i = [-1,-1]
compiler_flag_set = False
out_keyword = "Execution Cycles:"

for vals in sim_alter:
	property = vals[0]
	vals = vals[1]
	for val in vals:
		i+=1
		pass_string = 'NONE'
		for index3, line in enumerate(lines):
			# remove double and add single whitespace
			property = ' ' + ' '.join(property.split()) + ' '
			if property in line:
				line_spl = ' '.join(line.split()).split(property)
				if len(line_spl) == 2:
					# replace line
					backup_line = [index3,line]
					line = line_spl[0] + property + str(val) + '\n'
					lines[index3] = line
					pass_string = 'CHANGE: [name:' + property + ', val:' + str(val) + ' ]'
					break
				else:
					print('A line failed: ' + line + ' with [name:' + property + ',val:' + str(val) +']')
					pass_string = 'FAIL'
					break
			elif compiler_flag[0] in line and compiler_flag_set == False:
				lines[index3] = compiler_flag[0] + ' ' + str(compiler_flag[1])
				compiler_flag_set = True
				print('--Compiler flag found and updated: ' + compiler_flag[0] + ' ' + str(compiler_flag[1]))
	
		out_execpath = reldir + "/config" + str(i) + "/"
		out_fpath = out_execpath + "/" + fname_new + ext
		createFolder(out_execpath)
		with open(out_fpath,'w+') as f:
			f.writelines(lines)
		
		if os.path.isdir(out_execpath):
			#print(pass_string)
			sim_result_string = '[' + str(i) + '] '
			for index,iter_alg in enumerate(iter_algs):
				cmd = ["run", iter_alg, "-O3"]
				p = subprocess.Popen(cmd,cwd=out_execpath, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				p.wait()
				
				sim_result_file = out_execpath + "output-" + iter_alg + ".c/ta.log.000" 
				try:
					with open(sim_result_file,'r') as f:
						sim_lines = f.readlines()
						for sim_line in sim_lines:
							if out_keyword in sim_line:
								exec_cycles_str = ' '.join(sim_line.split()).split(out_keyword)[1].replace(' ','')
								exec_cycles = int(exec_cycles_str.split('(')[0])
					if (optimal_exec_cycles[index] == -1 or exec_cycles < optimal_exec_cycles[index]):
						optimal_exec_cycles[index] = exec_cycles
						optimal_sim_i[index] = i
					sim_result_string += iter_alg  + ': ' + str(exec_cycles) + ' ' 
				except IOError:
					print('This simulation failed (files not created). Reverting ALTER to succesful sim config.')
					lines[backup_line[0]] = backup_line[1]
			print(sim_result_string + ' ' + pass_string)

		else:
			print('Directory not found, internal program error. Breaking sim.')
			break

print('\n--Simulation finished--')
print(iter_algs)
print(optimal_exec_cycles)
print(optimal_sim_i)