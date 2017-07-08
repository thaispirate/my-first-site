import math,cairo

########################### Desenha uma pessoa chave na familia
#piStartX: canto superior esquerdo
#piStartY: canto superior esquerdo
#piSize: dimensao do desenho (sempre um canvas quadrado)
#pbIndex: e a pessoa indice? (True | False)
#pbMan: homem (True), mulher (False)
#pbDead: pessoa falecida? (True | False)
#pstrBirthDate: ano de nascimento
def drawPersonOfInterst(piStartX,piStartY,piSize,pbIndex,pbMan,pbDead,pstrBirthDate,pstrDeathDate,pstrNome):
	ctx.set_line_width(0.1)
	ctx.set_source_rgb(0, 0, 0)
	if pbMan:
		ctx.rectangle(piStartX,piStartY,piSize,piSize) 
		if pbIndex:
			ctx.rectangle(piStartX+4,piStartY+4,piSize-8,piSize-8)
		if pbDead:
			ctx.move_to(piStartX,piStartY)
			ctx.line_to(piStartX+piSize,piStartY+piSize)
			ctx.move_to(piStartX,piStartY+piSize)
			ctx.line_to(piStartX+piSize,piStartY)
	else :
		ctx.move_to((piStartX+piSize),(piStartY+piSize/2))
		ctx.arc((piStartX+piSize/2),(piStartY+piSize/2),piSize/2,0,2*math.pi)
		if pbIndex:
			ctx.move_to((piStartX+piSize-3),(piStartY+piSize/2))
			ctx.arc((piStartX+piSize/2),(piStartY+piSize/2),piSize/2-3,0,2*math.pi)
		if pbDead:
			iDelta = ((math.sqrt(2)-1)*piSize/2)*math.sin(math.radians(45))
			ctx.move_to(piStartX+iDelta,piStartY+iDelta)
			ctx.line_to(piStartX+piSize-iDelta,piStartY+piSize-iDelta)
			ctx.move_to(piStartX+iDelta,piStartY+piSize-iDelta)
			ctx.line_to(piStartX+piSize-iDelta,piStartY+iDelta)
	ctx.stroke()
	ctx.select_font_face("Times", cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_NORMAL)
	ctx.set_font_size(8)
	if pstrDeathDate == "":
		ctx.move_to(piStartX,piStartY-2)
		ctx.show_text(pstrBirthDate)
	else:
		ctx.move_to(piStartX-10,piStartY-2)
		ctx.show_text(pstrBirthDate + "-" + pstrDeathDate)
	ctx.move_to(piStartX,piStartY+piSize+9)
	ctx.show_text(pstrNome)

########################### Desenha a pessoa qualquer
def drawPerson(piStartX,piStartY,piSize,pbMan):
	ctx.set_line_width(0.1)
	ctx.set_source_rgb(0, 0, 0)
	if pbMan:
		ctx.rectangle(piStartX,piStartY,piSize,piSize) 
	else :
		ctx.move_to((piStartX+piSize),(piStartY+piSize/2))
		ctx.arc((piStartX+piSize/2),(piStartY+piSize/2),piSize/2,0,2*math.pi)
	ctx.stroke()

########################### Desenha a familia de avos paternos
def drawFatherParents(piStartX,piStartY,piSize,pstrRelation,piMaleOffSpring,piFemaleOffSpring,
pbManHadPreviousRelation,piManPreviousMaleOffspring,piManPreviousFemaleOffspring,
pbManHadNextRelation,piManNextMaleOffspring,piManNextFemaleOffspring,
pbWomanHadPreviousRelation,piWomanPreviousMaleOffspring,piWomanPreviousFemaleOffspring,
pbWomanHadNextRelation,piWomanNextMaleOffspring,piWomanNextFemaleOffspring,
pbDeadGrandfather,pstrGrandfatherBirthDate,pstrGrandfatherDeathDate,pstrGrandfatherName,
pbDeadGrandmother,pstrGrandmotherBirthDate,pstrGrandmotherDeathDate,pstrGrandmotherName):
	#inicializacoes
	iX = iY = 0
	iTic = 4
	ctx.set_line_width(0.1)
	ctx.set_source_rgb(0, 0, 0)
	ctx.stroke()
	iFinalFatherX = 0
	iFinalFatherY = 0
	if (pbManHadNextRelation or pbWomanHadPreviousRelation):
		iMaxY = 4*piSize
	else:#nao existem outros relacionamentos
		iMaxY = 2*piSize
	#Comeca a desenha, da esquerda para direita	
	if pbManHadPreviousRelation: #Relacionamento anterior do Homem
		drawPerson(piStartX,piStartY,piSize,False)
		iX = piStartX + int(piSize/2)
		iY = piStartY + piSize
		ctx.move_to(iX,iY)
		iY = iY+iMaxY
		ctx.line_to(iX,iY)
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
		i=0
		while (i < piManPreviousMaleOffspring): #Filhos homens do relacionamento anterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piManPreviousFemaleOffspring): #Filhas mulheres do relacionamento anterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		ctx.move_to(iX,iY)
		if((piManPreviousMaleOffspring+piManPreviousFemaleOffspring)>0):
			iX = iX + int(1.5*piSize)
		else:
			iX = iX + 3*piSize
		ctx.line_to(iX,iY)
		piStartX = iX-int(piSize/2)
		ctx.move_to(piStartX,piStartY)
	#end if
	#O homem
	drawPersonOfInterst(piStartX,piStartY,piSize,False,True,pbDeadGrandfather,pstrGrandfatherBirthDate,pstrGrandfatherDeathDate,pstrGrandfatherName)
	iX = piStartX + int(piSize/2)			
	iY = piStartY + int(piSize+12)
	ctx.move_to(iX,iY)
	iY = iY+iMaxY-12
	ctx.line_to(iX,iY)
	iXAux = iX
	iYAux = iY
	#Relacionamento posterior do homem
	iY = piStartY + int(piSize+12) + piSize
	ctx.move_to(iX,iY)
	if pbManHadNextRelation: #Relacionamento posterior do Homem
		i = 0
		while (i < piManNextMaleOffspring): #Filhos homens do relacionamento posteiror
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piManNextFemaleOffspring): #Filhas mulheres do relacionamento posterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		ctx.move_to(iX,iY)
		if((piManNextMaleOffspring+piManNextFemaleOffspring)>0):
			iX = iX + int(1.5*piSize)
		else:
			iX = iX + 3*piSize
		ctx.line_to(iX,iY)
		ctx.line_to(iX,iY-iTic)
		drawPerson(iX-int(piSize/2),iY-piSize-iTic,piSize,False)
	iSizeOffspringBranch = int((piMaleOffSpring + piFemaleOffSpring)*1.5*piSize)
	if pbWomanHadPreviousRelation: #Relacionamento anterior da Mulher
		iDelta = iSizeOffspringBranch - int(1.5*(piWomanPreviousMaleOffspring+piWomanPreviousFemaleOffspring+piManNextMaleOffspring+piManNextFemaleOffspring)*piSize)
		if iDelta > 0:
			iX = iX + iDelta
		else:
			iX = iX-int(piSize/2) + 2*piSize
		iY = iY-piSize-iTic
		drawPerson(iX,iY,piSize,True)
		iX = iX + int(piSize/2) 
		iY = iY + piSize
		ctx.move_to(iX,iY)
		iY = iY + iTic
		ctx.line_to(iX,iY)
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
		i = 0
		while (i < piWomanPreviousMaleOffspring): #Filhos homens do relacionamento anterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piWomanPreviousFemaleOffspring): #Filhas mulheres do relacionamento anterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		ctx.move_to(iX,iY)
		if((piWomanPreviousMaleOffspring+piWomanPreviousFemaleOffspring)>0):
			iX = iX + int(1.5*piSize)
		else:
			iX = iX + 3*piSize
		ctx.line_to(iX,iY)
		iY = piStartY + int(piSize+12)
		ctx.line_to(iX,iY)
		iX = iX - int(piSize/2)
		iY = piStartY
	#Os filhos do casal
	if (pbManHadNextRelation or pbWomanHadPreviousRelation):
		iXWoman = iX + int(piSize/2) + 15
	else:
		iXWoman = iX + int((piMaleOffSpring + piFemaleOffSpring)*1.5*piSize) +2*piSize + 15
	iX = iXAux
	iY = iYAux
	if(pbManHadNextRelation or pbWomanHadNextRelation):
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
	i = 0
	while (i < piMaleOffSpring): #Filhos homens do casal
		ctx.move_to(iX,iY)
		iX = iX + int(1.5*piSize)
		ctx.line_to(iX,iY)
		ctx.line_to(iX,iY+iTic)
		if i==0:
			iFinalFatherX = iX-int(piSize/2)
			iFinalFatherY = iY+iTic
		else:
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
		i = i+1
	i = 0
	while (i < piFemaleOffSpring): #Filhas mulheres do casal
		ctx.move_to(iX,iY)
		iX = iX + int(1.5*piSize)
		ctx.line_to(iX,iY)
		ctx.line_to(iX,iY+iTic)
		drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
		i = i+1	
	ctx.move_to(iX,iY)
	ctx.line_to(iXWoman,iY)
	iYWoman = iY
	iY = piStartY + piSize + 12
	ctx.line_to(iXWoman,iY)
	piStartX = iXWoman - int(piSize/2)
	drawPersonOfInterst(piStartX,piStartY,piSize,False,False,pbDeadGrandmother,pstrGrandmotherBirthDate,pstrGrandmotherDeathDate,pstrGrandmotherName)
	#Relacionamento posterior da Mulher	
	if pbWomanHadNextRelation:
		i = 0
		iX = iXWoman
		iY = iYWoman
		while (i < piWomanNextMaleOffspring): #Filhos homens do relacionamento posterior da mulher
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piWomanNextFemaleOffspring): #Filhas mulheres do relacionamento posterior da mulher
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1	
		ctx.move_to(iX,iY)
		if((piWomanNextMaleOffspring+piWomanNextFemaleOffspring)>0):
			iX = iX + int(1.5*piSize)
		else:
			iX = iX + 3*piSize
		ctx.line_to(iX,iY)
		piStartX = iX-int(piSize/2)
		ctx.move_to(piStartX,piStartY)
		drawPerson(piStartX,piStartY,piSize,True)
		iX = piStartX + int(piSize/2)			
		iY = piStartY + int(piSize)
		ctx.move_to(iX,iY)
		iY = iY+iMaxY
		ctx.line_to(iX,iY)
	ctx.stroke()
	iFinalX = piStartX
	iFinalY = piStartY 
	return iFinalX,iFinalY,iFinalFatherX,iFinalFatherY
	

########################### Desenha a familia de avos maternos
def drawMotherParents(piStartX,piStartY,piSize,pstrRelation,piMaleOffSpring,piFemaleOffSpring,
pbManHadPreviousRelation,piManPreviousMaleOffspring,piManPreviousFemaleOffspring,
pbManHadNextRelation,piManNextMaleOffspring,piManNextFemaleOffspring,
pbWomanHadPreviousRelation,piWomanPreviousMaleOffspring,piWomanPreviousFemaleOffspring,
pbWomanHadNextRelation,piWomanNextMaleOffspring,piWomanNextFemaleOffspring,
pbDeadGrandfather,pstrGrandfatherBirthDate,pstrGrandfatherDeathDate,pstrGrandfatherName,
pbDeadGrandmother,pstrGrandmotherBirthDate,pstrGrandmotherDeathDate,pstrGrandmotherName):
	#inicializacoes
	iX = iY = 0
	iTic = 4
	ctx.set_line_width(0.1)
	ctx.set_source_rgb(0, 0, 0)
	ctx.stroke()
	iFinalMotherX = 0
	iFinalMotherY = 0
	if (pbManHadNextRelation or pbWomanHadPreviousRelation):
		iMaxY = 4*piSize
	else:#nao existem outros relacionamentos
		iMaxY = 2*piSize
	#Comeca a desenha, da esquerda para direita	
	if pbManHadPreviousRelation: #Relacionamento anterior do Homem
		drawPerson(piStartX,piStartY,piSize,False)
		iX = piStartX + int(piSize/2)
		iY = piStartY + piSize
		ctx.move_to(iX,iY)
		iY = iY+iMaxY
		ctx.line_to(iX,iY)
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
		i = 0
		while (i < piManPreviousMaleOffspring): #Filhos homens do relacionamento anterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piManPreviousFemaleOffspring): #Filhas mulheres do relacionamento anterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		ctx.move_to(iX,iY)
		if((piManPreviousMaleOffspring+piManPreviousFemaleOffspring)>0):
			iX = iX + int(1.5*piSize)
		else:
			iX = iX + 3*piSize
		ctx.line_to(iX,iY)
		piStartX = iX-int(piSize/2)
		ctx.move_to(piStartX,piStartY)
	#end if
	#O homem
	drawPersonOfInterst(piStartX,piStartY,piSize,False,True,pbDeadGrandfather,pstrGrandfatherBirthDate,pstrGrandfatherDeathDate,pstrGrandfatherName)
	iX = piStartX + int(piSize/2)			
	iY = piStartY + int(piSize+12)
	ctx.move_to(iX,iY)
	iY = iY+iMaxY-12
	ctx.line_to(iX,iY)
	iXAux = iX
	iYAux = iY
	#Relacionamento posterior do homem
	iY = piStartY + int(piSize+12) + piSize
	ctx.move_to(iX,iY)
	if pbManHadNextRelation: #Relacionamento posterior do Homem
		i = 0
		while (i < piManNextMaleOffspring): #Filhos homens do relacionamento posteiror
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piManNextFemaleOffspring): #Filhas mulheres do relacionamento posterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		ctx.move_to(iX,iY)
		if((piManNextMaleOffspring+piManNextFemaleOffspring)>0):
			iX = iX + int(1.5*piSize)
		else:
			iX = iX + 3*piSize
		ctx.line_to(iX,iY)
		ctx.line_to(iX,iY-iTic)
		drawPerson(iX-int(piSize/2),iY-piSize-iTic,piSize,False)
	iSizeOffspringBranch = int((piMaleOffSpring + piFemaleOffSpring)*1.5*piSize)
	if pbWomanHadPreviousRelation: #Relacionamento anterior da Mulher
		iDelta = iSizeOffspringBranch - int(1.5*(piWomanPreviousMaleOffspring+piWomanPreviousFemaleOffspring+piManNextMaleOffspring+piManNextFemaleOffspring)*piSize)
		if iDelta > 0:
			iX = iX + iDelta
		else:
			iX = iX-int(piSize/2) + 2*piSize
		iY = iY-piSize-iTic
		drawPerson(iX,iY,piSize,True)
		iX = iX + int(piSize/2) 
		iY = iY + piSize
		ctx.move_to(iX,iY)
		iY = iY + iTic
		ctx.line_to(iX,iY)
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
		i = 0
		while (i < piWomanPreviousMaleOffspring): #Filhos homens do relacionamento anterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piWomanPreviousFemaleOffspring): #Filhas mulheres do relacionamento anterior
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		ctx.move_to(iX,iY)
		if((piWomanPreviousMaleOffspring+piWomanPreviousFemaleOffspring)>0):
			iX = iX + int(1.5*piSize)
		else:
			iX = iX + 3*piSize
		ctx.line_to(iX,iY)
		iY = piStartY + int(piSize+12)
		ctx.line_to(iX,iY)
		iX = iX - int(piSize/2)
		iY = piStartY
	#Os filhos do casal
	if (pbManHadNextRelation or pbWomanHadPreviousRelation):
		iXWoman = iX + int(piSize/2) + 15
	else:
		iXWoman = iX + int((piMaleOffSpring + piFemaleOffSpring)*1.5*piSize) +2*piSize + 15
	iX = iXAux
	iY = iYAux
	if(pbManHadNextRelation or pbWomanHadNextRelation):
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
	i = 0
	while (i < piMaleOffSpring): #Filhos homens do casal
		ctx.move_to(iX,iY)
		iX = iX + int(1.5*piSize)
		ctx.line_to(iX,iY)
		ctx.line_to(iX,iY+iTic)
		drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
		i = i+1
	i = 0
	while (i < piFemaleOffSpring): #Filhas mulheres do casal
		ctx.move_to(iX,iY)
		iX = iX + int(1.5*piSize)
		ctx.line_to(iX,iY)
		ctx.line_to(iX,iY+iTic)
		if i==0:
			iFinalMotherX = iX-int(piSize/2)
			iFinalMotherY = iY+iTic
		else:
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
		i = i+1	
	ctx.move_to(iX,iY)
	ctx.line_to(iXWoman,iY)
	iYWoman = iY
	iY = piStartY + piSize + 12
	ctx.line_to(iXWoman,iY)
	piStartX = iXWoman - int(piSize/2)
	drawPersonOfInterst(piStartX,piStartY,piSize,False,False,pbDeadGrandmother,pstrGrandmotherBirthDate,pstrGrandmotherDeathDate,pstrGrandmotherName)
	#Relacionamento posterior da Mulher	
	if pbWomanHadNextRelation:
		i = 0
		iX = iXWoman
		iY = iYWoman
		while (i < piWomanNextMaleOffspring): #Filhos homens do relacionamento posterior da mulher
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piWomanNextFemaleOffspring): #Filhas mulheres do relacionamento posterior da mulher
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1	
		ctx.move_to(iX,iY)
		if((piWomanNextMaleOffspring+piWomanNextFemaleOffspring)>0):
			iX = iX + int(1.5*piSize)
		else:
			iX = iX + 3*piSize
		ctx.line_to(iX,iY)
		piStartX = iX-int(piSize/2)
		ctx.move_to(piStartX,piStartY)
		drawPerson(piStartX,piStartY,piSize,True)
		iX = piStartX + int(piSize/2)			
		iY = piStartY + int(piSize)
		ctx.move_to(iX,iY)
		iY = iY+iMaxY
		ctx.line_to(iX,iY)
	ctx.stroke()
	iFinalX = piStartX
	iFinalY = piStartY
	return iFinalX,iFinalY,iFinalMotherX,iFinalMotherY


########################### Desenha a familia anterior (pai, mae e irmaos)
def drawBeginingFamily(piFatherX,piFatherY,piMotherX,piMotherY,piSize,pstrRelation,piMaleOffSpring,piFemaleOffSpring,pbIndexIsMale,
pbManHadPreviousRelation,piManPreviousMaleOffspring,piManPreviousFemaleOffspring,
pbManHadNextRelation,piManNextMaleOffspring,piManNextFemaleOffspring,
pbWomanHadPreviousRelation,piWomanPreviousMaleOffspring,piWomanPreviousFemaleOffspring,
pbWomanHadNextRelation,piWomanNextMaleOffspring,piWomanNextFemaleOffspring):
	#inicializacoes
	iX = iY = 0
	iTic = 4
	ctx.set_line_width(0.1)
	ctx.set_source_rgb(0, 0, 0)
	ctx.stroke()
	if (pbManHadNextRelation or pbWomanHadPreviousRelation):
		iMaxY = 4*piSize
	else:#nao existem outros relacionamentos
		iMaxY = 2*piSize
	#Desenha os irmaos diretos
	iX = piFatherX + int(piSize/2)
	iY = piFatherY + 2*piSize + 6
	if(piFatherY < piMotherY):
		iVerticalLine = abs(piFatherY-piMotherY)
	else:
		iVerticalLine = 0
	ctx.move_to(iX,iY)
	ctx.line_to(iX,iY+iMaxY+iVerticalLine)
	iX = piMotherX + int(piSize/2)
	iY = piMotherY + 2*piSize + 6
	if(piMotherY < piFatherY):
		iVerticalLine = abs(piFatherY-piMotherY)
	else:
		iVerticalLine = 0
	ctx.line_to(iX,iY+iMaxY+iVerticalLine)
	ctx.line_to(iX,iY)
	iX = piFatherX + int(piSize/2)
	iY = piFatherY + 2*piSize + 6 + iMaxY
	if((pstrRelation == "Separado") or (pstrRelation == "Divorciado")):
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		if(pstrRelation == "Divorciado"):
			ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
			ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
	i = 0
	while (i < piMaleOffSpring): #Filhos homens do relacionamento
		iX = iX + int(1.5*piSize)
		ctx.move_to(iX,iY)
		ctx.line_to(iX,iY+iTic)		
		if(pbIndexIsMale and (i==0)):		
			iIndexPersonX = iX-int(piSize/2)
			iIndexPersonY = iY+iTic
		else:
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
		i = i+1
	i = 0
	while (i < piFemaleOffSpring): #Filhas mulheres do relacionamento
		iX = iX + int(1.5*piSize)
		ctx.move_to(iX,iY)
		ctx.line_to(iX,iY+iTic)
		if((not pbIndexIsMale) and (i==0)):		
			iIndexPersonX = iX-int(piSize/2)
			iIndexPersonY = iY+iTic
		else:
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
		i = i+1
	#Relacionamento anterior do pai
	if pbManHadPreviousRelation:
		iX = piFatherX + int(piSize/2)
		iY = piFatherY + 2*piSize + 6 + iMaxY
		ctx.move_to(iX,iY)
		i = 0
		while (i < piManPreviousFemaleOffspring): #Filhas mulheres do relacionamento
			ctx.move_to(iX,iY)
			iX = iX - int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		i = 0
		while (i < piManPreviousMaleOffspring): #Filhos homens do relacionamento
			ctx.move_to(iX,iY)
			iX = iX - int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)		
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		ctx.move_to(iX,iY)
		iX = iX - 2*piSize
		ctx.line_to(iX,iY)
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
		ctx.move_to(iX,iY)
		iY = iY - 2.5*piSize - 12
		ctx.line_to(iX,iY)
		drawPerson(iX-int(piSize/2),iY-piSize,piSize,False)
	#Relacionamento posterior do pai
	if pbManHadNextRelation:
		iX = piFatherX + int(piSize/2)
		iY = piFatherY - 0.5*piSize - 6 + iMaxY
		ctx.move_to(iX,iY)
		i = 0
		while (i < piManNextMaleOffspring): #Filhos homens do relacionamento
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)		
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piManNextFemaleOffspring): #Filhas mulheres do relacionamento
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		ctx.move_to(iX,iY)
		iX = iX + 2*piSize
		ctx.line_to(iX,iY)
		ctx.move_to(iX,iY)
		iY = iY - iTic
		ctx.line_to(iX,iY)
		drawPerson(iX-int(piSize/2),iY-piSize,piSize,False)
	#Relacionamento anterior da mae
	if pbWomanHadPreviousRelation:
		iX = piMotherX + int(piSize/2)
		iY = piMotherY - 0.5*piSize - 6 + iMaxY
		ctx.move_to(iX,iY)
		i = 0
		while (i < piWomanPreviousFemaleOffspring): #Filhas mulheres do relacionamento
			ctx.move_to(iX,iY)
			iX = iX - int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		i = 0
		while (i < piWomanPreviousMaleOffspring): #Filhos homens do relacionamento
			ctx.move_to(iX,iY)
			iX = iX - int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)		
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		ctx.move_to(iX,iY)
		iX = iX - 2*piSize
		ctx.line_to(iX,iY)
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
		ctx.move_to(iX,iY)
		iY = iY - iTic
		ctx.line_to(iX,iY)
		drawPerson(iX-int(piSize/2),iY-piSize,piSize,True)
	#Relacionamento posterior da mae
	if pbWomanHadNextRelation:
		iX = piMotherX + int(piSize/2)
		iY = piMotherY + 2*piSize + 6 + iMaxY
		ctx.move_to(iX,iY)
		i = 0
		while (i < piWomanNextMaleOffspring): #Filhos homens do relacionamento
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)		
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
			i = i+1
		i = 0
		while (i < piWomanNextFemaleOffspring): #Filhas mulheres do relacionamento
			ctx.move_to(iX,iY)
			iX = iX + int(1.5*piSize)
			ctx.line_to(iX,iY)
			ctx.line_to(iX,iY+iTic)
			drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
			i = i+1
		ctx.move_to(iX,iY)
		iX = iX + 2*piSize
		ctx.line_to(iX,iY)
		ctx.move_to(iX,iY)
		iY = iY - 2.5*piSize - 12
		ctx.line_to(iX,iY)
		drawPerson(iX-int(piSize/2),iY-piSize,piSize,True)	
	ctx.stroke()
	return iIndexPersonX,iIndexPersonY


########################### Desenha a familia da pessoa indice
def drawIndexFamily(piIndexX,piIndexY,pbIndexIsMale,piSize,pstrRelation,piMaleOffSpring,piFemaleOffSpring,
pbIndexHadPreviousRelation,piIndexPreviousMaleOffspring,piIndexPreviousFemaleOffspring,
pbIndexHadNextRelation,piIndexNextMaleOffspring,piIndexNextFemaleOffspring,
pbSposeHadPreviousRelation,piSposePreviousMaleOffspring,piSposePreviousFemaleOffspring,
pbSposeHadNextRelation,piSposeNextMaleOffspring,piSposeNextFemaleOffspring):
	#inicializacoes
	iX = iY = 0
	iTic = 4
	iSposeX = 0
	iSposeY = 0
	ctx.set_line_width(0.1)
	ctx.set_source_rgb(0, 0, 0)
	ctx.stroke()
	if pbIndexIsMale:
		if (pbIndexHadNextRelation or pbSposeHadPreviousRelation):
			iMaxY = 4*piSize
		else:#nao existem outros relacionamentos
			iMaxY = 3*piSize
	else:
		if (pbIndexHadPreviousRelation or pbSposeHadNextRelation):
			iMaxY = 4*piSize
		else:#nao existem outros relacionamentos
			iMaxY = 3*piSize
	if(not(pstrRelation == "Nao se aplica")):	
		#Representa os filhos do relacionamento
		iX = piIndexX + int(piSize/2)
		iY = piIndexY + 2*piSize + 6
		ctx.move_to(iX,iY)
		ctx.line_to(iX,iY+iMaxY)
		iY = iY+iMaxY
		if pbIndexIsMale:
			if((pstrRelation == "Separado") or (pstrRelation == "Divorciado")):
				ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
				if(pstrRelation == "Divorciado"):
					ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
					ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
		ctx.move_to(iX,iY)
		if pbIndexIsMale: #O relacionamento principal
			i = 0
			while (i < piMaleOffSpring): #Filhos homens do relacionamento
				ctx.move_to(iX,iY)
				iX = iX + int(1.5*piSize)
				ctx.line_to(iX,iY)
				ctx.line_to(iX,iY+iTic)		
				drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
				i = i+1
			i = 0
			while (i < piFemaleOffSpring): #Filhas mulheres do relacionamento
				ctx.move_to(iX,iY)
				iX = iX + int(1.5*piSize)
				ctx.line_to(iX,iY)
				ctx.line_to(iX,iY+iTic)
				drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
				i = i+1
		else:
			i = 0
			while (i < piFemaleOffSpring): #Filhas mulheres do relacionamento
				ctx.move_to(iX,iY)
				iX = iX - int(1.5*piSize)
				ctx.line_to(iX,iY)
				ctx.line_to(iX,iY+iTic)
				drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
				i = i+1
			i = 0
			while (i < piMaleOffSpring): #Filhos homens do relacionamento
				ctx.move_to(iX,iY)
				iX = iX - int(1.5*piSize)
				ctx.line_to(iX,iY)
				ctx.line_to(iX,iY+iTic)		
				drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
				i = i+1
		ctx.move_to(iX,iY)
		if pbIndexIsMale:
			iDelta = piIndexNextMaleOffspring + piIndexNextFemaleOffspring + piSposePreviousMaleOffspring + piSposePreviousFemaleOffspring
		else:
			iDelta = piSposeNextMaleOffspring + piSposeNextFemaleOffspring + piIndexPreviousMaleOffspring + piIndexPreviousFemaleOffspring
		iDelta = iDelta * piSize + 40	
		if pbIndexIsMale:		
			iX = iX + 2*piSize + iDelta
		else:
			iX = iX - 2*piSize - iDelta
		ctx.line_to(iX,iY)
		ctx.move_to(iX,iY)
		if not pbIndexIsMale:
			if((pstrRelation == "Separado") or (pstrRelation == "Divorciado")):
				ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
				if(pstrRelation == "Divorciado"):
					ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
					ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
		ctx.move_to(iX,iY)
		iSposeRelationsX = iX
		iSposeRelationsY = iY
		iY = iY - piSize - 12
		ctx.line_to(iX,iY)
		iSposeX = iX-int(piSize/2)
		iSposeY = iY-piSize
		if pbIndexIsMale: #O conjunge e mulher
			#Relacionamento anterior do conjuge (mulher)
			if pbSposeHadPreviousRelation: #Representa os filhos do relacionamento anterior do conjuge (mulher)
				iX = iSposeRelationsX
				iY = iSposeRelationsY - 2*piSize
				i = 0
				while (i < piSposePreviousFemaleOffspring): #Filhas mulheres do relacionamento
					ctx.move_to(iX,iY)
					iX = iX - int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
					i = i+1
				i = 0
				while (i < piSposePreviousMaleOffspring): #Filhos homens do relacionamento
					ctx.move_to(iX,iY)
					iX = iX - int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)		
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
					i = i+1
				ctx.move_to(iX,iY)
				iX = iX - 2*piSize
				ctx.line_to(iX,iY)
				ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
				ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
				ctx.move_to(iX,iY)			
				iY = iY - iTic
				ctx.line_to(iX,iY)
				drawPerson(iX-int(piSize/2),iY-piSize,piSize,pbIndexIsMale)
			
			#Relacionamento posterior do conjuge (mulher)
			if pbSposeHadNextRelation: #Representa os filhos do relacionamento posterior do conjuge  (mulher)
				iX = iSposeRelationsX
				iY = iSposeRelationsY
				i = 0
				while (i < piSposeNextMaleOffspring): #Filhos homens do relacionamento
					ctx.move_to(iX,iY)
					iX = iX + int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
					i = i+1
				i = 0
				while (i < piSposeNextFemaleOffspring): #Filhas mulheres do relacionamento
					ctx.move_to(iX,iY)
					iX = iX + int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)		
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
					i = i+1
				ctx.move_to(iX,iY)
				iX = iX + 2*piSize
				ctx.line_to(iX,iY)			
				ctx.move_to(iX,iY)			
				iY = iY - 2*piSize - 12
				ctx.line_to(iX,iY)
				drawPerson(iX-int(piSize/2),iY-piSize,piSize,pbIndexIsMale)
			
			#Relacionamento anterior (homem)
			if pbIndexHadPreviousRelation: #Representa os filhos do relacionamento anterior  (homem)
				iX = piIndexX + int(piSize/2)
				iY = piIndexY + 2*piSize + 6 + iMaxY
				i = 0
				while (i < piIndexPreviousFemaleOffspring): #Filhas mulheres do relacionamento
					ctx.move_to(iX,iY)
					iX = iX - int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
					i = i+1
				i = 0
				while (i < piIndexPreviousMaleOffspring): #Filhos homens do relacionamento
					ctx.move_to(iX,iY)
					iX = iX - int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)		
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
					i = i+1
				ctx.move_to(iX,iY)
				iX = iX - 2*piSize
				ctx.line_to(iX,iY)
				ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
				ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
				ctx.move_to(iX,iY)			
				iY = iY - 2*piSize - 12
				ctx.line_to(iX,iY)
				drawPerson(iX-int(piSize/2),iY-piSize,piSize,not pbIndexIsMale)
			
			# Relacionamento posterior (homem)
			if pbIndexHadNextRelation: #Representa os filhos do relacionamento posterior  (homem)
				iX = piIndexX + int(piSize/2)
				iY = piIndexY + 6 + iMaxY
				i = 0
				while (i < piIndexNextMaleOffspring): #Filhos homens do relacionamento
					ctx.move_to(iX,iY)
					iX = iX + int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
					i = i+1
				i = 0
				while (i < piIndexNextFemaleOffspring): #Filhas mulheres do relacionamento
					ctx.move_to(iX,iY)
					iX = iX + int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)		
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
					i = i+1
				ctx.move_to(iX,iY)
				iX = iX + 2*piSize
				ctx.line_to(iX,iY)			
				ctx.move_to(iX,iY)			
				iY = iY - iTic
				ctx.line_to(iX,iY)
				drawPerson(iX-int(piSize/2),iY-piSize,piSize,not pbIndexIsMale)
		else: #O conjunge e homem
			#Relacionamento anterior do conjuge (homem)
			if pbSposeHadPreviousRelation: #Representa os filhos do relacionamento anterior do conjuge  (homem)
				iX = iSposeRelationsX
				iY = iSposeRelationsY
				i = 0
				while (i < piSposePreviousFemaleOffspring): #Filhas mulheres do relacionamento
					ctx.move_to(iX,iY)
					iX = iX - int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
					i = i+1
				i = 0
				while (i < piSposePreviousMaleOffspring): #Filhos homens do relacionamento
					ctx.move_to(iX,iY)
					iX = iX - int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)		
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
					i = i+1
				ctx.move_to(iX,iY)
				iX = iX - 2*piSize
				ctx.line_to(iX,iY)
				ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
				ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
				ctx.move_to(iX,iY)			
				iY = iY - 2*piSize - 12
				ctx.line_to(iX,iY)
				drawPerson(iX-int(piSize/2),iY-piSize,piSize,pbIndexIsMale)
			
			#Relacionamento posterior do conjuge (homem)
			if pbSposeHadNextRelation: #Representa os filhos do relacionamento posterior do conjuge  (homem)
				iX = iSposeRelationsX
				iY = iSposeRelationsY - 2*piSize
				i = 0
				while (i < piSposeNextMaleOffspring): #Filhos homens do relacionamento
					ctx.move_to(iX,iY)
					iX = iX + int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
					i = i+1
				i = 0
				while (i < piSposeNextFemaleOffspring): #Filhas mulheres do relacionamento
					ctx.move_to(iX,iY)
					iX = iX + int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)		
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
					i = i+1
				ctx.move_to(iX,iY)
				iX = iX + 2*piSize
				ctx.line_to(iX,iY)			
				ctx.move_to(iX,iY)			
				iY = iY - iTic
				ctx.line_to(iX,iY)
				drawPerson(iX-int(piSize/2),iY-piSize,piSize,not pbIndexIsMale)
			
			#Relacionamento anterior (mulher)
			if pbIndexHadPreviousRelation: #Representa os filhos do relacionamento anterior  (mulher)
				iX = piIndexX + int(piSize/2)
				iY = piIndexY + 6 + iMaxY
				i = 0
				while (i < piIndexPreviousFemaleOffspring): #Filhas mulheres do relacionamento
					ctx.move_to(iX,iY)
					iX = iX - int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
					i = i+1
				i = 0
				while (i < piIndexPreviousMaleOffspring): #Filhos homens do relacionamento
					ctx.move_to(iX,iY)
					iX = iX - int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)		
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
					i = i+1
				ctx.move_to(iX,iY)
				iX = iX - 2*piSize
				ctx.line_to(iX,iY)
				ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
				ctx.move_to(iX+int(piSize*0.6),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.9),iY-int(piSize*0.3))
				ctx.move_to(iX,iY)			
				iY = iY - iTic
				ctx.line_to(iX,iY)
				drawPerson(iX-int(piSize/2),iY-piSize,piSize,not pbIndexIsMale)
			
			#Relacionamento posterior (mulher)
			if pbIndexHadNextRelation: #Representa os filhos do relacionamento posterior  (mulher)
				iX = piIndexX + int(piSize/2)
				iY = piIndexY + 2*piSize + 6 + iMaxY
				i = 0
				while (i < piIndexNextMaleOffspring): #Filhos homens do relacionamento
					ctx.move_to(iX,iY)
					iX = iX + int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,False)
					i = i+1
				i = 0
				while (i < piIndexNextFemaleOffspring): #Filhas mulheres do relacionamento
					ctx.move_to(iX,iY)
					iX = iX + int(1.5*piSize)
					ctx.line_to(iX,iY)
					ctx.line_to(iX,iY+iTic)		
					drawPerson(iX-int(piSize/2),iY+iTic,piSize,True)
					i = i+1
				ctx.move_to(iX,iY)
				iX = iX + 2*piSize
				ctx.line_to(iX,iY)			
				ctx.move_to(iX,iY)			
				iY = iY - 2*piSize - 12
				ctx.line_to(iX,iY)
				drawPerson(iX-int(piSize/2),iY-piSize,piSize,not pbIndexIsMale)
	
	ctx.stroke()
	return iSposeX,iSposeY


########################### Principal
def main():
	width, height = 950,580
	surface = cairo.PDFSurface ("draw.pdf", width, height)
	global ctx
	ctx = cairo.Context (surface)
	ctx.set_source_rgb(1,1,1)
	ctx.rectangle(0,0,width,height)
	ctx.fill()

	#iFinalX,iFinalY,iFinalFatherX,iFinalFatherY = drawFatherParents(170,50,16,"Casado",2,2,True,2,1,True,1,1,True,1,1,True,1,1,True,"1930","2004","Mello",True,"1930","2012","Triani")

	#iFinalX,iFinalY,iFinalMotherX,iFinalMotherY = drawMotherParents(iFinalX+40,iFinalY,16,"Casado",2,2,True,2,1,True,1,1,True,1,1,True,1,1,True,"1917","2004","Pagliotti",True,"1936","1990","Aisenberg")

	#drawPersonOfInterst(iFinalFatherX,iFinalFatherY+8,16,False,True,False,"1950","","Luiz")
	#drawPersonOfInterst(iFinalMotherX,iFinalMotherY+8,16,False,False,False,"1950","","Carmen")
	
	#iSubjectX,iSubjectY = drawBeginingFamily(iFinalFatherX,iFinalFatherY,iFinalMotherX,iFinalMotherY,16,"Separado",2,2,True,True,1,1,True,1,1,True,1,1,True,1,2)

	#drawPersonOfInterst(iSubjectX,iSubjectY+10,16,True,True,False,"1976","","Flavio")

	#iSposeX,iSposeY = drawIndexFamily(iSubjectX,iSubjectY,True,16,"Casado",1,2,True,1,1,True,2,2,True,1,1,True,2,1)
	
	#drawPersonOfInterst(iSposeX,iSposeY-10,16,False,False,False,"1973","","Giovana")




	#piStartX,piStartY,piSize,pstrRelation,piMaleOffSpring,piFemaleOffSpring,
	#pbManHadPreviousRelation,piManPreviousMaleOffspring,piManPreviousFemaleOffspring,
	#pbManHadNextRelation,piManNextMaleOffspring,piManNextFemaleOffspring,
	#pbWomanHadPreviousRelation,piWomanPreviousMaleOffspring,piWomanPreviousFemaleOffspring,
	#pbWomanHadNextRelation,piWomanNextMaleOffspring,piWomanNextFemaleOffspring,
	#pbDeadGrandfather,pstrGrandfatherBirthDate,pstrGrandfatherDeathDate,pstrGrandfatherName,
	#pbDeadGrandmother,pstrGrandmotherBirthDate,pstrGrandmotherDeathDate,pstrGrandmotherName
	iFinalX,iFinalY,iFinalFatherX,iFinalFatherY = drawFatherParents(170,50,16,"Separado",2,0,False,0,0,True,1,2,False,0,0,True,1,0,True,"1930","2004","Mello",True,"1930","2012","Triani")
	#piStartX,piStartY,piSize,pstrRelation,piMaleOffSpring,piFemaleOffSpring,
	#pbManHadPreviousRelation,piManPreviousMaleOffspring,piManPreviousFemaleOffspring,
	#pbManHadNextRelation,piManNextMaleOffspring,piManNextFemaleOffspring,
	#pbWomanHadPreviousRelation,piWomanPreviousMaleOffspring,piWomanPreviousFemaleOffspring,
	#pbWomanHadNextRelation,piWomanNextMaleOffspring,piWomanNextFemaleOffspring,
	#pbDeadGrandfather,pstrGrandfatherBirthDate,pstrGrandfatherDeathDate,pstrGrandfatherName,
	#pbDeadGrandmother,pstrGrandmotherBirthDate,pstrGrandmotherDeathDate,pstrGrandmotherName
	iFinalX,iFinalY,iFinalMotherX,iFinalMotherY = drawMotherParents(iFinalX+40,iFinalY,16,"Casado",0,1,False,0,0,False,0,0,False,0,0,False,0,0,True,"1917","2004","Pagliotti",True,"1936","1990","Aisenberg")

	#piStartX,piStartY,piSize,pbIndex,pbMan,pbDead,pstrBirthDate,pstrDeathDate,pstrNome
	drawPersonOfInterst(iFinalFatherX,iFinalFatherY+8,16,False,True,False,"1950","","Luiz")
	#piStartX,piStartY,piSize,pbIndex,pbMan,pbDead,pstrBirthDate,pstrDeathDate,pstrNome
	drawPersonOfInterst(iFinalMotherX,iFinalMotherY+8,16,False,False,False,"1950","","Carmen")
	#piFatherX,piFatherY,piMotherX,piMotherY,piSize,pstrRelation,piMaleOffSpring,piFemaleOffSpring,pbIndexIsMale,
	#pbManHadPreviousRelation,piManPreviousMaleOffspring,piManPreviousFemaleOffspring,
	#pbManHadNextRelation,piManNextMaleOffspring,piManNextFemaleOffspring,
	#pbWomanHadPreviousRelation,piWomanPreviousMaleOffspring,piWomanPreviousFemaleOffspring,
	#pbWomanHadNextRelation,piWomanNextMaleOffspring,piWomanNextFemaleOffspring	
	iSubjectX,iSubjectY = drawBeginingFamily(iFinalFatherX,iFinalFatherY,iFinalMotherX,iFinalMotherY,16,"Casado",1,1,True,False,0,0,False,0,0,False,0,0,False,0,0)

	#piStartX,piStartY,piSize,pbIndex,pbMan,pbDead,pstrBirthDate,pstrDeathDate,pstrNome
	drawPersonOfInterst(iSubjectX,iSubjectY+10,16,True,True,False,"1976","","Flavio")
	#piIndexX,piIndexY,pbIndexIsMale,piSize,pstrRelation,piMaleOffSpring,piFemaleOffSpring,
	#pbIndexHadPreviousRelation,piIndexPreviousMaleOffspring,piIndexPreviousFemaleOffspring,
	#pbIndexHadNextRelation,piIndexNextMaleOffspring,piIndexNextFemaleOffspring,
	#pbSposeHadPreviousRelation,piSposePreviousMaleOffspring,piSposePreviousFemaleOffspring,
	#pbSposeHadNextRelation,piSposeNextMaleOffspring,piSposeNextFemaleOffspring
	iSposeX,iSposeY = drawIndexFamily(iSubjectX,iSubjectY,True,16,"Casado",0,0,True,0,0,False,0,0,False,0,0,False,0,0)

	#piStartX,piStartY,piSize,pbIndex,pbMan,pbDead,pstrBirthDate,pstrDeathDate,pstrNome
	drawPersonOfInterst(iSposeX,iSposeY-10,16,False,False,False,"1973","","Giovana")


	ctx.show_page()



main()







