import re
import random

gb_instructions = 0

MIN_OP = 0
MAX_OP = 31	# lhu
MAX_12_BIT_NUMBER = 4095

def main():
	operation = random.randint(MIN_OP, MAX_OP)	#random operation
	obtainInput()
	operationType = gb_instructions[operation][1]
	#getting random registers
	regChs1 = ['s', 't']
	reg1 = regChs1[random.randint(0, len(regChs1)-1)]
	reg1 += str(random.randint(0, 11 if reg1=='s' else 6))	
	reg2 = regChs1[random.randint(0, len(regChs1)-1)]
	reg2 += str(random.randint(0, 11 if reg2=='s' else 6))
	if operationType == 'I':
		optr3 = random.randint(0, 4095)	# Generate a 12 bit number
	else: # R type. Creation of the 3rd register
		optr3 = regChs1[random.randint(0, len(regChs1)-1)]
		optr3 += str(random.randint(0, 11 if reg2=='s' else 6))
		while(optr3 == reg2 and optr3 == reg1): 
			optr3 = regChs1[random.randint(0, len(regChs1)-1)]
			optr3 += str(random.randint(0, 11 if reg2=='s' else 6))
	print(
		"Indicar el tipo de operación y las secuencias de bits correspondientes a la siguiente instruccion: \n\t\t" + 
		gb_instructions[operation][0] + ' ' + reg1 + ', ' + reg2 + ', ' + get3rdOptr(optr3)
	)
	#getting answers from the terminal
	print("Ingresar informacion: ")
	opType = input("\t\tTipo de operacion: ")
	opCode = bin(int(input("\t\tCodigo de operacion en binario: "), 2))
	if operationType != 'S' or operationType != 'B':
		rd = bin(int(input("\t\tNumero del registro destino en binario: "), 2))
	if operationType != 'J' or operationType != 'U':
		func3 = bin(int(input("\t\tCodigo de funcion de 3 bits en binario: "), 2))
		rs1 = bin(int(input("\t\tNumero del registro fuente 1 en binario: "), 2))
	if operationType == 'R' or operationType == 'I' or operationType == 'S' or operationType == 'B':
		if operationType == 'I':
			rs2 = bin(int(input("\t\tInmediato de 12 bits en binario: "), 2))
		else:
			rs2 = bin(int(input("\t\tNumero del registro fuente 2 en binario: "), 2))
		if operationType == 'R':
			func7 = bin(int(input("\t\tCodigo de funcion de 7 bits en binario: "), 2))
	#verifing the if the answers are correct.
	print("Resultados: ")
	if opType == operationType:
		print("\t\tTipo de operacion correcto")
	else:
		print("\t\tIncorrecto. Tipo de operacion correcto: "+operationType)

	verifingAns(opCode, operation, "\t\tCodigo de operacion correcto", "\t\tIncorrecto. Codigo de operacion correcto: ", False, 2, 2)
	
	verifingAns(rd, reg1, "\t\tNumero del registro destino correcto", "\t\tIncorrecto. Numero del registro destino correcto: ", True)
	
	verifingAns(func3, operation, "\t\tCodigo de funcion de 3 bits correcto", "\t\tIncorrecto.  odigo de funcion de 3 bits correcto: ", False, 3, 16)
	
	verifingAns(rs1, reg2, "\t\tNumero del registro fuente 1 correcto", "\t\tIncorrecto. Numero del registro fuente 1 correcto: ", True)
	
	if operationType == 'R' or operationType == 'I' or operationType == 'S' or operationType == 'B':
		if operationType == 'I':
			verifingAns(rs2, optr3, "\t\tInmediato de 12 bits correcto", "\t\tIncorrecto. Inmediato de 12 bits correcto: ", False)
		else:
			verifingAns(rs2, optr3, "\t\tNumero del registro fuente 2 correcto", "\t\tIncorrecto. Numero del registro fuente 2 correcto: ", True)

		
		if operationType == 'R':
			verifingAns(func7, operation, "\t\tCodigo de funcion de 7 bits correcto", "\t\tIncorrecto. Codigo de funcion de 7 bits correcto: ", False, 4, 16)
	

# Verify an asnwer
#	datInsEle: number of element that contains a data of the instruccion
#	numRep: representation of the data to parse
#	isReg: is to indicate if the aswer its about a register
#	operation: works to indicate the random risc-v operation. if isReg is true, is used to pass the register
def verifingAns(answer, operation, goodAnsMsj, badAnsMsj, isReg, datInsEle = False, numRep = False):
	if not isReg:
		if (type(operation) is int and bin(operation) == answer) or answer == bin(int(gb_instructions[operation][datInsEle], numRep)):
			print(goodAnsMsj)
		else:
			print(badAnsMsj+str(bin(int(gb_instructions[operation][datInsEle], numRep))))
		return 0

	if answer == bin(obtainRegNum(operation)):
		print(goodAnsMsj)
	else:
		print(badAnsMsj+str(bin(obtainRegNum(operation))))

# Get the instructions form the "instructions.txt." file and saved then into a tuple
def obtainInput():
	global gb_instructions
	variableRegex = re.compile(r'(\w+) (\w+) (\w+) (\w+) (\w+)')
	with open("instrucions.txt", 'r') as iF:
		gb_instructions = variableRegex.findall(iF.read())

# Returns the respective number of the alias of a register. Only 32 bit registers for not floating point numbers
#	regAl: string that contains the alias of a register
def obtainRegNum(regAl):
	ch1of2 = regAl[0]
	ch2of2 = regAl[1:]
	match ch1of2:
		case "z": 
			return 0	#zero
		case "r": 
			return 1	#ra
		case "s":
			match ch2of2:
				case "p": 
					return 2	#sp
				case "0": 
					return 8	#s0
				case "1": 
					return 9	#s1
				case _:	
					return int(ch2of2)+16	#s2-s11
		case "g": 
			return 3	#gp
		case "t":
			match ch2of2:
				case "p": 
					return 4	#tp
				case _:	
					return (int(ch2of2)+5 if int(ch2of2)<3 else	int(ch2of2)+25) #t0-t2 and t3-t6
		case "a":
			match ch2of2:
				case "0": 
					return 10	#a0
				case "1": 
					return 11	#a1
				case _:	
					return int(ch2of2)+10	#a2-a7
				

# Return something depending on the type of the parameter, if is str means its a register so there's no changes, if is not a str return a positive number, or a negative number, or a hex number
def get3rdOptr(optr3):
	if type(optr3) is str:
		return optr3
	else:
		if random.randint(0,1):
			return str(optr3)
		else:
			return str(optr3-2**12 if optr3>2**11 else (str(optr3) if random.randint(0,1) else hex(optr3)))

main()