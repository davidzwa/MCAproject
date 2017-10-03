# Default configuration settings - initial DSE point
fname = 'configuration.mm-default'
fname_new = 'configuration'
ext = '.mm'

# Simulation settings
iter_algs = ['crc','greyscale']
CONST_NUM_CLUSTERS = ['# ***Clusters***', 1]

# Simulation progression settings - 1 clusters
CONST_SIM_ALTER = list()
CONST_SIM_ALTER.append([
			('IssueWidth.0',	[2,8], 'skip'),
			('Alu.0',			[2]),
			('IssueWidth.0',	[2]),
			('IssueWidth.0',	[2]),
			#('Alu.0',	[2,4,6,8]),
			 ])

# Simulation progression settings - 2 clusters
CONST_SIM_ALTER.append([
			('IssueWidth.0',	[2,8], 'skip'),
			('Alu.0',			[2]),
			('IssueWidth.0',	[2]),
			('IssueWidth.0',	[2]),
			#('Alu.0',	[2,4,6,8]),
			 ])

# Simulation progression settings - 4 clusters
CONST_SIM_ALTER.append([
			('IssueWidth.0',	[2,8], 'skip'),
			('Alu.0',			[2]),
			('IssueWidth.0',	[2]),
			('IssueWidth.0',	[2]),
			#('Alu.0',	[2,4,6,8]),
			 ])

### data to be gathered
CONST_DATA_OUT = "Execution Cycles:"
CONST_DATA_MULTI = [
					("Total Cycles:", 							"Cyc Total"),
					("Execution Cycles:", 						"Cyc Exec"),
					("Nops:", 									"Cyc Nops"),
					("Executed operations:",					"Ops"),
					("Percentage Bus Bandwidth Consumed:",		"Bus BW"),
					("Avg. IPC (no stalls):",					"IPC (no stalls)"),
					("Avg. IPC (with stalls):",					"IPC (stalls)"),
					]

CONST_DATA_NAMES = list()
for iter_alg in iter_algs:
	for name in CONST_DATA_MULTI:
		CONST_DATA_NAMES.append(name[1] + ' (' + iter_alg + ')')