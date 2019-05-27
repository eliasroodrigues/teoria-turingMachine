# -*- coding: utf-8 -*-

import Regex
import Output

class Machine(object):

	
	def __init__(self):
		self.regex = Regex.Regex()
		self.outLine = Output.Output()
		self.instrucaoAtual = None
		self.paramBloco = []
		self.blocosCod = []
		self.estadoAtual = ''
		self.listaDePrints = []
		self.contInteracoes = 0
		self.blocoAtual = None
		self.fita1 = []
		self.fita2 = '_'
		self.pilhaBloco = []


	def getBloco(self, opcao):
		for b in self.blocosCod:
			if b[0] == opcao:
				# print('####  achou o bloco = '+b[0])
				# print(b)
				return b

	def getInicioBloco(self, nomeBloco):
		for b in self.blocosCod:
			if b[0] == nomeBloco:
				return b[2]

	# monta o bloco de codigo a partir das linhas recebidas
	def separaBloco(self, opcao, param):
		# inicio de bloco
		# bloco <identificador do bloco> <estado inicial>
		# bloco main 1
		if opcao == 'iniBloco':
			self.paramBloco = []
			nomeBloco = param.split()
			self.paramBloco.insert(0, nomeBloco[1])
			self.paramBloco.append(param)
		elif opcao == 'fimBloco':
			self.paramBloco.append(param)
			return self.paramBloco
		else:
			self.paramBloco.append(param)
		return None

	# Separa o codigo em blocos de codigo a serem executados
	def separaCodEmBlocos(self, linesFile):
		bloco = []
		for l in linesFile:
			bloco = self.separaBloco(self.regex.aplicaRegex(l), l)
			if (bloco != None):
				self.blocosCod.append(bloco)

		return self.blocosCod


	def getInstrucoes(self, bloco, estado):
		instr = []
		#print('GETInstricoes: '+estado)
		#print('GETInstricoes: '+bloco[0])
		#print(bloco)
		for b in bloco:
			#print('linha: '+b)
			if (self.regex.aplicaRegex(b) == 'comando') and (int(b.split()[0]) == int(estado)):
				instr.append(b)
			elif (self.regex.aplicaRegex(b) == 'copy') and (int(b.split()[0]) == int(estado)):
				instr.append(b)
			elif (self.regex.aplicaRegex(b) == 'chaBloco') and (int(b.split()[0]) == int(estado)):
				instr.append(b)
			#print('imprime o comando')
			#print(instr)
		return instr



	# Executa ate o fim
	def run(self, palavra, head, linesFile):
		#print(palavra)
		self.listaDePrints = []
		self.blocosCod = self.separaCodEmBlocos(linesFile)
		self.blocoAtual = self.getBloco('main')
		self.instrucaoAtual = self.blocoAtual[1]
		self.fita1 = self.outLine.newLine(self.blocoAtual[0], self.blocoAtual[1].split()[2], '', head, palavra, self.fita2)
		#print(self.fita1)
		# print(self.fita[0])
		# print(self.blocoAtual[0])
		self.contInteracoes = 0
		if self.instrucaoAtual is not None:
			instrucaoPilha = None
			estadoPilha = ''
			while(True):
				# print('PILHA')
				# print(self.pilhaBloco)
				finalizou = self.execBloco(self.blocoAtual, estadoPilha)
				self.contInteracoes += 1
				# print(self.contInteracoes)
				if(self.contInteracoes == 500):
					return None
				# finaliza a execucao da maquina
				if (finalizou == 'pare') or (finalizou == 'aceite'):
					print('Programa FINALIZADO!')
					break
				# volta a executar o ultimo bloco da pilha (continua de onde parou)
				elif finalizou == 'retorne':
					# print('RETORNOU')
					instrucaoPilha = self.pilhaBloco.pop()
					self.blocoAtual = self.getBloco(instrucaoPilha[0])
					estadoPilha = instrucaoPilha[1]
					if (estadoPilha == 'pare') or (finalizou == 'aceite'):
						print('Programa FINALIZADO!')
						break
				# retorna o nome do proximo bloco a ser executado
				else:
					# print('EMPILHOU')
					self.blocoAtual = self.getBloco(finalizou)
					estadoPilha = ''
				# x = input()
			self.listaDePrints.append(self.fita1[0])
		else:
 			print('Bloco *main* nao identificado!')
		return self.listaDePrints

	# retorna a lista das proximas possiveis instrucoes
	def execBloco(self, bloco, estadoAtual):
		if estadoAtual == '':
			# print('Estado Atual eh None')
			#print('Bloco[1]split[2] em execucao: '+bloco[1].split()[2])
			self.estadoAtual = bloco[1].split()[2]
			#print('Estado Atual eh '+self.estadoAtual)
		else:
			self.estadoAtual = estadoAtual
			# print('Estado Atual eh '+self.estadoAtual)
		self.fita1[1] = bloco[0]
		self.fita1[2] = self.estadoAtual
		# print('Bloco em execucao: '+bloco[0])
		#print(self.estadoAtual)
		# print(self.fita1)
		sair = False
		while(True):
			#print('bloco atual '+ (self.blocoAtual[0]))
			#print('###### Estado Atual: '+self.estadoAtual)
			# x = input()
			#print('###################################')
			#print(bloco)
			#print('###################################')
			instrucoes = self.getInstrucoes(bloco, self.estadoAtual)

			cabecote = self.outLine.getCabecote(self.fita1)
			#print('###### Instrucoes: ')
			#print(instrucoes)
			if(instrucoes == []):
				exit(1)
			# x = input()
			for i in instrucoes:
				
				#print('###### Instrucao: '+i)
				# <estado atual> <simbolo atual> -- <novo simbolo> <movimento> <novo estado>
				# eh um comando && estado da instrucao corresponde
				if (self.regex.aplicaRegex(i) == 'comando'):
					#print('entrou no comando')
					#print((i.split()[1])[0])

					if ((i.split()[1])[0] == '['):
						#print(self.fita2)
						#print((i.split()[1])[1])
						if((i.split()[1])[1] == self.fita2) or ((i.split()[1])[1] == '*'):
							#print('ricochete')
							self.fita1[2] = self.estadoAtual
							# le o que está na fita 2
							#if(self.fita2 == '.'):
							#	exit(1)
							self.fita1 = self.outLine.alteraCabecoteCochete(self.fita1, self.fita2, i.split()[3])
							self.listaDePrints.append(self.fita1[0])
							#print(self.fita1[0])
							self.fita1 = self.outLine.moveCabecote(self.fita1, i.split()[4])
							if (i.split()[5] == 'retorne'):
								return 'retorne'
							elif ((i.split()[5] == 'pare') or (i.split()[5] == 'aceite')):
								# print('pare')
								return i.split()[5]
							else:
								# estado atual eh atualizado para proximo estado
								self.estadoAtual = i.split()[5]
								break

					# letra do cabecote corresponde
					elif (i.split()[1] == cabecote) or (i.split()[1] == '*'):
						#print('###Executa ### Instrucao: '+i)
						x = i.split()
						for s in x:
							if s is '!':
								sair = True

						self.fita1[2] = self.estadoAtual
						self.fita1 = self.outLine.alteraCabecote(self.fita1, i.split()[1], i.split()[3])
						self.listaDePrints.append(self.fita1[0])
						#print('antes'+self.fita1[0])
						self.fita1 = self.outLine.moveCabecote(self.fita1, i.split()[4])
						#print('depois'+self.fita1[0])
						if (i.split()[5] == 'retorne'):
							return 'retorne'
						elif ((i.split()[5] == 'pare') or (i.split()[5] == 'aceite')):
							# print('pare')
							return i.split()[5]
						else:
							# estado atual eh atualizado para proximo estado
							self.estadoAtual = i.split()[5]
							break

				# <estado atual> <identificador do bloco> <estado de retorno>
				# 10 moveFim 11

				elif (self.regex.aplicaRegex(i) == 'chaBloco'):
					#print('chamou um bloco')
					
					atual = i.split()[0]
					nomeBloco = i.split()[1]
					retorno = i.split()[2]

					x = i.split()
					for s in x:
						if s is '!':
							sair = True
					# print('chamou bloco: '+i)

					# estado atual eh atualizado para proximo estado
					self.pilhaBloco.append([bloco[0], retorno])
					#print('Empilhou: '+bloco[0]+' - '+retorno)
					return nomeBloco

				# 02 copiar 10
				elif (self.regex.aplicaRegex(i) == 'copy'):
					#print('copiar ou colar ' + str(self.fita1) + ' split ' + str(i.split()))
					if(i.split()[1] == 'copiar'):
						self.fita1[2] = self.estadoAtual
						self.fita1 = self.outLine.copiar(self.fita1, self.fita1[4])
					elif(i.split()[1] == 'colar'):
						self.fita1[2] = self.estadoAtual
						self.fita1 = self.outLine.colar(self.fita1, self.fita1[4])
					# atualiza estado atual
					self.listaDePrints.append(self.fita1[0])
					self.fita2 = self.fita1[6]
					self.estadoAtual = i.split()[2]
					#print('copiar ou colar ' + str(self.fita1) + ' split ' + str(i.split()))
					# exit(1)

				if sair is True:
					for x in self.listaDePrints:
						print(x)
						exit(1)
		return None

