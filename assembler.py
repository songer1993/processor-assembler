#! /usr/bin/python

#//////////////////////////////////////////////////////////////////////////////////
# // Company: University of Edinburgh
# // Engineer: Qisong Wang (s1364207)
# //
# // Create Date: 01.03.2016 17:58:47
# // Design Name: Mouse_Processor_Demo_Assembly
# // Project Name: Mouse_Processor_Demo
# // Target Devices: Basys3
# // Tool Versions: Python 2.7 or 3
# // Description: This is a assembler in Python, whcih takes the input from a file
# //              and converts it to the machine code (ROM) and constants (RAM) for
# //              a simple micro-controller implementation in Verilog on a Xilinx FPGA
# //		  It supports:
# //			- Multiple labels
# //			- Inputs and outputs aliasing
# //			- Loading actual value $, and create and linke to RAM file
# //
# // Dependencies: - None
# //
# // Revision:
# // Revision 0.01 - File Created
# // Additional Comments: "python assembler.py -i input_file -o output_file" will
# //                      process the target file.
# //
# //////////////////////////////////////////////////////////////////////////////////


import re
import sys
import getopt

# Instruction   ->  Encoding
#----------------|-------------------
# LOAD R, M 		-> 0000000r, mmmmmmmm
# LOAD R, $V		-> 0000000r, mmmmmmmm (RAM address where vvvvvvvv is stored)
# STORE R, M 		-> 0000001r, mmmmmmmm
#############ALU###################
# ADD R 		-> 0000010r
# SUB R 		-> 0001010r
# MUTIPLY R             -> 0010010r
# SHIFTL R          -> 0011010r
# SHIFTR R         -> 0100010r
# INCREMENT R           -> 0101010r
# DECREMENT R           -> 0110010r
# IS_EQUAL R            -> 0111010r
# GREATER_THAN R        -> 1000010r
# LESS_THAN R           -> 1001010r
# AND R                 -> 1010010r
# OR R                  -> 1011010r
# XOR R                 -> 1100010r
###################################
# BREQ A                -> 10010110, aaaaaaaa
# BRTQ A                -> 10100110, aaaaaaaa
# BLTQ A                -> 10110110, aaaaaaaa
# GOTO A                -> 00000111, aaaaaaaa
# GOTO_IDLE             -> 00001000
# FUNCTION_CALL A       -> 00001001, aaaaaaaa
# RETURN                -> 00001010
# DEREF R         -> 00001011+r

ROM_SIZE = 256          # Instruction Memory of 256 bytes
RAM_SIZE = 128          # RAM of 128 bytes

constants = {}		# label list
inputs = {}		# inputs list
outputs = {}		# outputs list

def createROMfile(out_filename, memory_vals):
	'''
	Creates a dat file containing just the values of memory at
	their locations
	'''
	out_filename = out_filename +  '_ROM.txt'
	with open(out_filename, 'w') as f:
		for mem_address in range(0,ROM_SIZE):
			# Start writing the memory values to the proper
			# memory locations
			if memory_vals.has_key(mem_address):
				f.write(str(memory_vals[mem_address])+'\n')
				#print'Address:{} Value:{}'.format(mem_address, memory_vals[mem_address])

			else:
				f.write('00\n')
		f.write('')


def createRAMfile(out_filename, memory_vals):
	'''
	Creates a dat file containing just the values of memory at
	their locations
	'''
	out_filename = out_filename + '_RAM.txt'
	with open(out_filename, 'w') as f:
		for mem_address in range(0,RAM_SIZE):
			# Start writing the memory values to the proper
			# memory locations
			if constants.has_key(mem_address):
				f.write(str(constants[mem_address])+'\n')
				#print'Address:{} Value:{}'.format(mem_address, memory_vals[mem_address])

			else:
				f.write('00\n')
		f.write('')


def readfile(in_path, out_filename, type):
	'''
	Reads every line in the file and saves it to a list
	'''
	with open(in_path, 'rb') as filehandle:
		lines = [line.rstrip() for line in filehandle]
	labels = getLabelAddresses(lines)
	memory_vals = getMemoryValues(lines, labels)
	memory_vals[0xFE] = labels["TIMER_ISR"]
	memory_vals[0xFF] = labels["MOUSE_ISR"]

	# strip any file indicators from out_filename
	if '.' in out_filename:
		out_filename = out_filename.replace(out_filename[out_filename.index('.'):],'')

	if 'debug' in type:
		# Some Things for debugging
		sortedList = [x for x in memory_vals.iteritems()]
		sortedList.sort(key=lambda x:x[0])
		for item in sortedList:
			print('Address: {} :: Value: {}'.format(item[0],item[1]))
		sys.exit(0)
	elif 'coe' in type:
		# produce a coe type file
		createROMfile(out_filename, memory_vals)
	elif 'dat' in type:
		# produce a dat file, which is just barebones and no comments
		createRAMfile(out_filename, memory_vals)
	elif 'both' in type:
		# produce both dat file and coe file
		createROMfile(out_filename, memory_vals)
		createRAMfile(out_filename, memory_vals)


def getLabelAddresses(instructions):
	'''
	Parses the lines in the Instruction file, in this run, records all label
	addresses and input and output mapping
	'''
	# Create empty dictionary
        # Initalise label dictionary
	labels = {"TIMER_ISR": 0xFC, "MOUSE_ISR": 0xFD}
	global inputs
	global outputs

	# Create variables for keeping track of memory blocks
	offset = 0
	increment = 1
	lineNumber = 0

	for line in instructions:
		lineNumber+=1
		line = line.upper()
		tokens = re.split(r'[,\s]\s*',line)

		# count required memory
		if len(tokens) == 1 and tokens[0] == '':
			increment = 0
			continue

		elif '#' in tokens[0]:
			increment = 0
			continue

		elif 'IN' in tokens:
			inputs[tokens[2]] = tokens[1]
			print("Inputs lists appended: ")
			print inputs
			increment = 0
			continue

		elif 'OUT' in tokens:
			outputs[tokens[2]] = tokens[1]
			print("Output lists appended ")
			print outputs
			increment = 0
			continue

		elif 'LOAD' in tokens:
			increment = 2

		elif 'WRITE' in tokens:
			increment = 2

		elif 'ADD' in tokens:
			increment = 1

		elif 'SUB' in tokens:
			increment = 1

		elif 'MUL' in tokens:
			increment = 1

		elif 'SHIFTL' in tokens:
			increment = 1

		elif 'SHIFTR' in tokens:
			increment = 1

		elif 'INCRA' in tokens:
			increment = 1

		elif 'INCRB' in tokens:
			increment = 1

		elif 'DECA' in tokens:
			increment = 1

		elif 'DECB' in tokens:
			increment = 1

		elif 'IS_EQUAL' in tokens:
			increment = 1

		elif 'GREATER_THAN' in tokens:
			increment = 1

		elif 'LESS_THAN' in tokens:
			increment = 1

		elif 'AND' in tokens:
			increment = 1

		elif 'OR' in tokens:
			increment = 1

		elif 'XOR' in tokens:
			increment = 1

		elif 'BREQ' in tokens:
			increment = 2

		elif 'BGTQ' in tokens:
			increment = 2

		elif 'BLTQ' in tokens:
			increment = 2

		elif 'GOTO' in tokens:
			increment = 2

		elif 'GOTO_IDLE' in tokens:
			increment = 1

		elif 'FUNCTION_CALL' in tokens:
			increment = 2

		elif 'RETURN' in tokens:
			increment = 1

		elif 'DEREF' in tokens:
			increment = 1

		elif 'TIMER_ISR' in tokens[0]:
			labels["TIMER_ISR"] = hex(offset)[2:].zfill(2)
			print("Label list updated")
			print labels
			increment = 0

		elif 'MOUSE_ISR' in tokens[0]:
			labels["MOUSE_ISR"] = hex(offset)[2:].zfill(2)
			print("Label list updated")
			print labels
			increment = 0

		else:
			print("Label list updated")
			labels[tokens[0].strip(':')] = hex(offset)[2:].zfill(2)
			print labels
			increment = 0

		offset += increment
	return labels


def getMemoryValues(instructions, labels):
	'''
	Parses the lines in the Instruction file and stores the
	contents of the memory address with the address in a
	dictionary. This dictionary is returned
	'''
	# Create empty dictionary
	memorydict = {}
	global constants
	global inputs
	global outputs

	# Create variables for keeping track of memory blocks
	offset = 0
	increment = 1
	offset1 = 0
	increment1 = 1
	lineNumber = 0

	for line in instructions:
		lineNumber+=1
		line = line.upper()
		tokens = re.split(r'[,\s]\s*',line)

		#print tokens
		if len(tokens) == 1 and tokens[0] == '':
			# print('Empty Line {}'.format(lineNumber))
			increment = 0
			increment1 = 0
			continue

		elif '#' in tokens[0]:
			increment = 0
			increment1 = 0
			continue

		elif 'IN' in tokens:
			increment = 0
			continue

		elif 'OUT' in tokens:
			increment = 0
			continue

		elif 'LOAD' in tokens:
			# assign and convert an value to its corresponding RAM address
			if '$' in tokens[2]:
				constants[offset1] = tokens[2][1:]
				increment1 = 1
				instruction2 = hex(offset1)[2:].zfill(2)
			else:
				# map an alias to its memory address
				if  tokens[2] in inputs:
					print "load an alias"
					print inputs[tokens[2]]
					tokens[2] = inputs[tokens[2]]

				# convert it to integer
				try:
					tokens[2] = int(tokens[2], 16)
					increment1 = 0
					instruction2 = hex(tokens[2])[2:].zfill(2)
			    	except ValueError:
					print('Error at Line {}'.format(lineNumber))
					print('LOAD memory location is not a number')
					sys.exit(1)

			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'

		 	# Put together instructions
			binary_instruction = int(('0000000'+ r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)

			# Store in memorydict
		 	memorydict[offset+0] = instruction1
		 	memorydict[offset+1] = instruction2
			increment = 2

		elif 'STORE' in tokens:
			# convert an alias to its memory address
			if tokens[2] in outputs:
				tokens[2] = outputs[tokens[2]]
			# convert it to integer
			try:
				tokens[2] = int(tokens[2], 16)
			except ValueError:
				print('Error at Line {}'.format(lineNumber))
				print('STOR memory location is not a number')
				sys.exit(1)
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
		 	# Put together instructions
			binary_instruction = int(('0000001'+ r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			instruction2 = hex(tokens[2])[2:].zfill(2)

			# Store in memorydict
			memorydict[offset+0] = instruction1
		 	memorydict[offset+1] = instruction2
			increment = 2
			increment1 = 0

		elif 'ADD' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('0000010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'SUB' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('0001010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'MUL' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('0010010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'SHIFTL' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('0011010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'SHIFTR' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('0100010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'INCRA' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('0101010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'INCRB' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('0110010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0


		elif 'DECA' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('0111010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'DECB' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('1000010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0



		elif 'IS_EQUAL' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('1001010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'GREATER_THAN' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('1010010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0


		elif 'LESS_THAN' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('1011010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'AND' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('1100010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'OR' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('1101010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'XOR' in tokens:
			# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				# Set bit representing the register
				r = '0' if 'A' in tokens[1] else '1'
			binary_instruction = int(('1110010' + r), 2)
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'BREQ' in tokens:
			if tokens[1] in labels:
				instruction2 = labels[tokens[1]]
			else:
				try:
					tokens[1] = int(tokens[1], 16)
					instruction2 = hex(tokens[1])[2:].zfill(2)
				except ValueError:
					print('Error at Line {}'.format(lineNumber))
					print('Address ADDR is not a number')
					sys.exit(1)

			binary_instruction = 0b10010110
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			# Store in memorydict
			memorydict[offset+0] = instruction1
		 	memorydict[offset+1] = instruction2
			increment = 2
			increment1 = 0

		elif 'BGTQ' in tokens:
			if tokens[1] in labels:
				instruction2 = labels[tokens[1]]
			else:
				try:
					tokens[1]	= int(tokens[1], 16)
				except ValueError:
					print('Error at Line {}'.format(lineNumber))
					print('Address ADDR is not a number')
					sys.exit(1)
				instruction2 = hex(tokens[1])[2:].zfill(2)

			binary_instruction = 0b10100110
			instruction1 = hex(binary_instruction)[2:].zfill(2)

			# Store in memorydict
			memorydict[offset+0] = instruction1
		 	memorydict[offset+1] = instruction2
			increment = 2
			increment1 = 0

		elif 'BLTQ' in tokens:
			if tokens[1] in labels:
				instruction2 = labels[tokens[1]]
			else:
				try:
					tokens[1] = int(tokens[1], 16)
					instruction2 = hex(tokens[1])[2:].zfill(2)
				except ValueError:
					print('Error at Line {}'.format(lineNumber))
					print('Address ADDR is not a number')
					sys.exit(1)

			binary_instruction = 0b10110110
			instruction1 = hex(binary_instruction)[2:].zfill(2)

			# Store in memorydict
			memorydict[offset+0] = instruction1
		 	memorydict[offset+1] = instruction2
			increment = 2
			increment1 = 0


		elif 'GOTO' in tokens:
			if tokens[1] in labels:
				instruction2 = labels[tokens[1]]
			else:
				try:
					tokens[1] = int(tokens[1], 16)
				except ValueError:
					print('Error at Line {}'.format(lineNumber))
					print('Address ADDR is not a number')
					sys.exit(1)
				instruction2 = hex(tokens[1])[2:].zfill(2)

			binary_instruction = 0b00000111
			instruction1 = hex(binary_instruction)[2:].zfill(2)

			# Store in memorydict
			memorydict[offset+0] = instruction1
		 	memorydict[offset+1] = instruction2
			increment = 2
			increment1 = 0

		elif 'GOTO_IDLE' in tokens:
			binary_instruction = 0b00001000
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0


		elif 'FUNCTION_CALL' in tokens:
			if tokens[1] in labels:
				instruction2 = labels[tokens[1]]
			else:
				try:
					tokens[1] = int(tokens[1], 16)
				except ValueError:
					print('Error at Line {}'.format(lineNumber))
					print('Address ADDR is not a number')
					sys.exit(1)
				instruction2 = hex(tokens[1])[2:].zfill(2)

			binary_instruction = 0b00001001
			instruction1 = hex(binary_instruction)[2:].zfill(2)

			# Store in memorydict
			memorydict[offset+0] = instruction1
		 	memorydict[offset+1] = instruction2
			increment = 2
			increment1 = 0

		elif 'RETURN' in tokens:
			binary_instruction = 0b00001010
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		elif 'DEREF' in tokens:
		# Set bit representing the register
			if 'A' not in tokens[1] and 'B' not in tokens[1]:
				print('ERROR at Line {}'.format(lineNumber))
				print('Unknown Register {}'.format(tokens[1]))
				sys.exit(1)
			else:
				binary_instruction = 0b00001011 if 'A' in tokens[1] else 0b00001100
			instruction1 = hex(binary_instruction)[2:].zfill(2)
			memorydict[offset+0] = instruction1
			increment = 1
			increment1 = 0

		else:
			increment = 0
			increment1 = 0

		offset += increment
		offset1 += increment1
		#print "Offset {} at line {}".format(offset, lineNumber)

	return memorydict


def main(argv):
	# Default file names options
	inFILE = 'mouse_demo.asm'
	outFILE= 'Complete_Demo'
	type = 'both'
	try:
		opts, args = getopt.getopt(argv, 'i:o:ht:',['inFILE','outFILE','help','type'])

	except getopt.GetoptError:
		print('Nothing you entered was correct... try again bud')
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-i', '--inFILE'):
			inFILE = arg
		elif opt in ('-o','--outFILE'):
			outFILE = arg
		elif opt in ('-t', '--type'):
			type = arg
		elif opt in ('-h','--help'):
			print('*======================================================*')
			print('|                  Simple Assembler Help:              |')
			print('*======================================================*')
			print('This program is meant to be a simple assembler that takes')
			print('the input from a file and converts it to the machine code')
			print('for a simple micro-controller implementation in Verilog ')
			print('on a Xilinx FPGA.')
			print('Target Python Version: 2.7')
			print('')
			print('Acceptable Arguments: ')
			print('\t-t or --type ')
			print('\t\tdefines the type of output file')
			print('\t\tchoices are coe or dat debug or both(default)')
			print('')
			print('\t-o or --outFILE')
			print('\t\tdefines the name of the output file')
			print('\t\tdefault is Encoding, which produces')
			print('\t\tEncoding.coe and Encoding.dat with')
			print('\t\tthe both switch activated')
			print('')
			print('\t-i or --inFILE')
			print('\t\tdefines the name of the input file')
			print('\t\tdefault is Instructions.dat')
			print('')
			print(' The Instructions implemented so far are listed bellow:')
			print('Instruction   ->  Encoding')
			print('----------------|-------------------')
			print('Load R, M 		-> 0000000r, mmmmmmmm')
			print('Load R, $V 		-> 0000000r, mmmmmmmm (store vvvvvvvv in an autolocated RAM address')
			print('STORE M, R 		-> 0000001r, mmmmmmmm')
			print('#############ALU###################')
			print('ADD R 			-> 0000010r')
			print('SUB R 			-> 0001010r')
			print('MUTIPLY R             	-> 0010010r')
			print('SHIFTL R          	-> 0011010r')
			print('SHIFTR R         	-> 0100010r')
			print('INCREMENT R           	-> 0101010r')
			print('DECREMENT R           	-> 0110010r')
			print('IS_EQUAL R            	-> 0111010r')
			print('GREATER_THAN R        	-> 1000010r')
			print('LESS_THAN R           	-> 1001010r')
			print('AND R                 	-> 1010010r')
			print('OR R                  	-> 1011010r')
			print('XOR R                 	-> 1100010r')
			print('###################################')
			print('BREQ A               	 -> 10010110, aaaaaaaa')
			print('BRTQ A                	-> 10100110, aaaaaaaa')
			print('BLTQ A                	-> 10110110, aaaaaaaa')
			print('GOTO A                	-> 00000111, aaaaaaaa')
			print('GOTO_IDLE             	-> 00001000')
			print('FUNCTION_CALL A       	-> 00001001, aaaaaaaa')
			print('RETURN                	-> 00001010')
			print('DEREF R         	-> 00001011+r')
			sys.exit(0)




	readfile(inFILE, outFILE, type)
	print('Successful Conversion')






if __name__ == '__main__':
	main(sys.argv[1:])
