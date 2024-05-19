import re
import random

gb_instructions = 0

MIN_OP = 0
MAX_OP = 9	# sltu

def main():
	operation = random.randint(MIN_OP, MAX_OP)	#random register operation
	obtainInput()
	#getting random registers
	regChs1 = ['s', 't']
	reg1 = regChs1[random.randint(0, len(regChs1)-1)] + str(random.randint(0, 11))		
	reg2 = regChs1[random.randint(0, len(regChs1)-1)] + str(random.randint(0, 11))
	reg3 = regChs1[random.randint(0, len(regChs1)-1)] + str(random.randint(0, 11))
	while(reg3 == reg2 and reg3 == reg1): reg3 = regChs1[random.randint(0, len(regChs1)-1)] + str(random.randint(0, 11))
	print(
		"Indicar las secuencias de bits correspondientes a la siguiente instruccion: \n\t\t" + 
		gb_instructions[operation][0] + ' ' + reg1 + ', ' + reg2 + ', ' + reg3
	)
	#getting answers from the terminal
	opCode = bin(int(input("\t\tCodigo de operacion en binario: "), 2))
	rd = bin(int(input("\t\tNumero del registro destino en binario: "), 2))
	func3 = bin(int(input("\t\tCodigo de funcion de 3 bits en binario: "), 2))
	rs1 = bin(int(input("\t\tNumero del registro fuente 1 en binario: "), 2))
	rs2 = bin(int(input("\t\tNumero del registro fuente 2 en binario: "), 2))
	func7 = bin(int(input("\t\tCodigo de funcion de 7 bits en binario: "), 2))
	#verifing the if the answers are correct.
	verifingAns(opCode, operation, "Codigo de operacion correcto", "Incorrecto.  Codigo de operacion correcto: ", False, 2, 2)
	
	verifingAns(rd, reg1, "Numero del registro destino correcto", "Incorrecto.  Numero del registro destino correcto: ", True)
	
	verifingAns(func3, operation, "Codigo de funcion de 3 bits correcto", "Incorrecto.  Codigo de funcion de 3 bits correcto: ", False, 3, 16)
	
	verifingAns(rs1, reg2, "Numero del registro fuente 1 correcto", "Incorrecto.  Numero del registro fuente 1 correcto: ", True)
	
	verifingAns(rs2, reg3, "Numero del registro fuente 2 correcto", "Incorrecto.  Numero del registro fuente 2 correcto: ", True)
	
	verifingAns(func7, operation, "Codigo de funcion de 7 bits correcto", "Incorrecto.  Codigo de funcion de 7 bits correcto: ", False, 4, 16)
	

# Verify an asnwer
#	datInsEle: number of element that contains a data of the instruccion
#	numRep: representation of the data to parse
#	isReg: is to indicate if the aswer its about a register
#	operation: works to indicate the random risc-v operation. if isReg is true, is used to pass the register
def verifingAns(answer, operation, goodAnsMsj, badAnsMsj, isReg, datInsEle = False, numRep = False):
	print(isReg)
	if not isReg:
		if answer == bin(int(gb_instructions[operation][datInsEle], numRep)):
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
				

main()