#!/usr/bin/python
# -*- coding: utf-8 -*-
class Output(object):
	def __init__(self):
		self.bloco = '................'
		self.estado = '0000'
		self.esquerda = '____________________'
		self.cabecote = '(e)'
		self.direita = '____________________'
		self.fita2 = '_'

	def newLineClear(self):
		return self.bloco+'.'+self.estado+': '+self.esquerda+self.cabecote+self.direita+' : '+self.fita2

	# pega o cabeçote (e) e retorna o 'e'
	def getCabecote(self, line):
		stra = line[4]
		return stra[1]

	def moveCabecote(self, line, direcao):
		# print('Antigo: ', self.esquerda+' - '+self.cabecote+' - '+self.direita)
		# print('Novo: ', esquerda+' - '+cabecote+' - '+direita)
		esquerda = line[3]
		cabecote = line[4]
		direita  = line[5]
		# move para esquerda
		if direcao == 'e':
			self.direita  = cabecote[1] + direita
			self.cabecote = '%s%s%s' %(cabecote[0], esquerda[len(esquerda)-1], cabecote[2])
			self.esquerda = esquerda[:len(esquerda)-1]
		# move para direita
		elif direcao == 'd':
			self.esquerda  = esquerda + cabecote[1]
			self.cabecote  = '%s%s%s' %(cabecote[0], direita[0], cabecote[2])
			self.direita   = direita[1:]
		elif direcao == 'i':
			pass

		# cria uma nova linha para poder atualizar a string line[0]
		return self.newLine(line[1], line[2], self.esquerda,self.cabecote,self.direita, self.fita2)

	# copia na fita 2
	def copiar(self, line, head):
		if (head[1] != '*'):
			self.fita2 = head[1]
			return self.newLine(line[1], line[2], line[3], head, line[5], self.fita2)
		else:
			print('Cabecote - Erro de Leitura!')
			exit()

	#cola da fita 2 para a fita 1
	def colar(self, line, head):
		self.cabecote = '%s%s%s' %(head[0], line[6], head[2])
		self.fita2 = line[6]
		return self.newLine(line[1], line[2], line[3], self.cabecote, line[5], line[6])		

	def alteraCabecoteCochete(self, line, read, write):
		cabecote = line[4]
		if (write != '*'):
			self.cabecote = '%s%s%s' %(cabecote[0], write, cabecote[2])
		return self.newLine(line[1], line[2], line[3], self.cabecote, line[5], line[6])

	def alteraCabecote(self, line, read, write):
		# se o que está lendo é diferente do que está no cabeçote
		if (read != '*') and (self.getCabecote(line) != read):
			print('Cabecote - Erro de Leitura!')
			print('Cabecote('+self.getCabecote(line)+') - read('+read+')')
			exit()

		cabecote = line[4]
		if (write != '*'):
			self.cabecote = '%s%s%s' %(cabecote[0], write, cabecote[2])
		return self.newLine(line[1], line[2], line[3], self.cabecote, line[5], line[6])

	def newLine(self, bloco, estado, esquerda, cabecote, direita, fita2):
		bloco = '{0:>16}'.format(bloco)
		self.bloco = bloco.replace(' ','.')

		self.estado = '%04d' %(int(estado))

		self.esquerda = '{:_>30}'.format(esquerda)
		#self.esquerda = esquerda.replace(' ','_')

		# cabecote = cabecote.split()
		# self.cabecote = '%s%s%s' %(cabecote[0], direita[0], cabecote[1])
		if len(cabecote) == 2:
			self.cabecote = '%s%s%s' %(cabecote[0], direita[0], cabecote[1])
			direita = direita[:0] + direita[1:]
		else:
			self.cabecote = cabecote

		# direita = direita[:0] + direita[1:]
		# self.direita = direita + '____________________'
		#direita = '{0:20}'.format(direita)
		self.direita = '{:_<30}'.format(direita)

		model = '{Bloco}.{Estado}: {Esquerda}{Cabecote}{Direita} : {Fita2}'
		model = model.format(Bloco=self.bloco, Estado=self.estado, Esquerda=self.esquerda, Cabecote=self.cabecote, Direita=self.direita, Fita2=self.fita2)

		itens = [model, self.bloco, self.estado, self.esquerda, self.cabecote, self.direita, self.fita2]
		return itens
