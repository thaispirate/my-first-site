import math
import cairo
from .models import Familia,Paciente,Relacionamento

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

	if((pstrRelation == "Separados") or (pstrRelation == "Divorciados")):
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		if(pstrRelation == "Divorciados"):
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

	if((pstrRelation == "Separados") or (pstrRelation == "Divorciados")):
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		if(pstrRelation == "Divorciados"):
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
	if((pstrRelation == "Separados") or (pstrRelation == "Divorciados")):
		ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
		ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
		if(pstrRelation == "Divorciados"):
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
			if((pstrRelation == "Separado(a)") or (pstrRelation == "Divorciado(a)")):
				ctx.move_to(iX+int(piSize*0.4),iY+int(piSize*0.3))
				ctx.line_to(iX+int(piSize*0.7),iY-int(piSize*0.3))
				if(pstrRelation == "Divorciado(a)"):
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
def main(paciente_id,analise_id):
	paciente_id=paciente_id
	analise_id=analise_id
	width, height = 950,580
	surface = cairo.PDFSurface ("genograma-"+paciente_id+"-"+analise_id+".pdf", width, height)
	global ctx
	ctx = cairo.Context (surface)
	ctx.set_source_rgb(1,1,1)
	ctx.rectangle(0,0,width,height)
	ctx.fill()

	paciente= Paciente.objects.get(usuario_id=paciente_id)


	avoPaterno = Familia.objects.get(usuario_id=paciente.id,parente="avoPaterno")
	avoPaterno_nome = avoPaterno.nome.split(" ")[0]
	nascimento=str(avoPaterno.nascimento)
	avoPaterno_ano = nascimento.split("-")[0]
	if avoPaterno.falecimento == None:
		avoPaterno_falecimento = False
		avoPaterno_falecimento_ano = ""
	else:
		avoPaterno_falecimento=True
		falecimento=str(avoPaterno.falecimento)
		avoPaterno_falecimento_ano = falecimento.split("-")[0]

	avoPaterna = Familia.objects.get(usuario_id=paciente.id,parente="avoPaterna")
	avoPaterna_nome = avoPaterna.nome.split(" ")[0]
	nascimento=str(avoPaterna.nascimento)
	avoPaterna_ano = nascimento.split("-")[0]
	if avoPaterna.falecimento == None:
		avoPaterna_falecimento = False
		avoPaterna_falecimento_ano = ""
	else:
		avoPaterna_falecimento=True
		falecimento=str(avoPaterna.falecimento)
		avoPaterna_falecimento_ano = falecimento.split("-")[0]

	avoPaternoR = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterno")
	if avoPaternoR.relacaoAntes == "Sim":
		avoPaternoR_relacaoAntes = True
		avoPaternoR_filhosAntes = avoPaternoR.filhosAntes
		avoPaternoR_filhasAntes = avoPaternoR.filhasAntes
	else:
		avoPaternoR_relacaoAntes = False
		avoPaternoR_filhosAntes =0
		avoPaternoR_filhasAntes = 0

	avoPaternoR_relacaoDepois = False
	avoPaternoR_filhosDepois = 0
	avoPaternoR_filhasDepois = 0
	if avoPaternoR.relacao == "Separados" or avoPaternoR.relacao == "Divorciados":
		if avoPaternoR.filhosDepois != 0 and avoPaternoR.filhosDepois != None:
			avoPaternoR_relacaoDepois = True
			avoPaternoR_filhosDepois = avoPaternoR.filhosDepois
			avoPaternoR_filhasDepois =  avoPaternoR.filhasDepois


	avoPaternaR = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterna")
	if avoPaternaR.relacaoAntes == "Sim":
		avoPaternaR_relacaoAntes = True
		avoPaternaR_filhosAntes = avoPaternaR.filhosAntes
		avoPaternaR_filhasAntes = avoPaternaR.filhasAntes
	else:
		avoPaternaR_relacaoAntes = False
		avoPaternaR_filhosAntes =0
		avoPaternaR_filhasAntes = 0

	avoPaternaR_relacaoDepois = False
	avoPaternaR_filhosDepois = 0
	avoPaternaR_filhasDepois = 0
	if avoPaternaR.relacao == "Separados" or avoPaternaR.relacao == "Divorciados":
		if avoPaternaR.filhosDepois != 0 and avoPaternaR.filhosDepois != None:
			avoPaternaR_relacaoDepois = True
			avoPaternaR_filhosDepois = avoPaternaR.filhosDepois
			avoPaternaR_filhasDepois =  avoPaternaR.filhasDepois

	iFinalX,iFinalY,iFinalFatherX,iFinalFatherY = drawFatherParents(170,50,16,avoPaternoR.relacao,
																	avoPaternoR.filhos,avoPaternoR.filhas,
																	avoPaternoR_relacaoAntes,avoPaternoR_filhosAntes,avoPaternoR.filhasAntes,
																	avoPaternoR_relacaoDepois,avoPaternoR_filhosDepois,avoPaternoR_filhasDepois,
																	avoPaternaR_relacaoAntes,avoPaternaR_filhosAntes,avoPaternaR_filhasAntes,
																	avoPaternaR_relacaoDepois,avoPaternaR_filhosDepois,avoPaternaR_filhasDepois,
																	avoPaterno_falecimento,avoPaterno_ano,avoPaterno_falecimento_ano,avoPaterno_nome,avoPaterna_falecimento,avoPaterna_ano,avoPaterna_falecimento_ano,avoPaterna_nome)

	avoMaterno = Familia.objects.get(usuario_id=paciente.id,parente="avoMaterno")
	avoMaterno_nome = avoMaterno.nome.split(" ")[0]
	nascimento=str(avoMaterno.nascimento)
	avoMaterno_ano = nascimento.split("-")[0]
	if avoMaterno.falecimento == None:
		avoMaterno_falecimento = False
		avoMaterno_falecimento_ano = ""
	else:
		avoMaterno_falecimento=True
		falecimento=str(avoMaterno.falecimento)
		avoMaterno_falecimento_ano = falecimento.split("-")[0]

	avoMaterna = Familia.objects.get(usuario_id=paciente.id,parente="avoMaterna")
	avoMaterna_nome = avoMaterna.nome.split(" ")[0]
	nascimento=str(avoMaterna.nascimento)
	avoMaterna_ano = nascimento.split("-")[0]
	if avoMaterna.falecimento == None:
		avoMaterna_falecimento = False
		avoMaterna_falecimento_ano = ""
	else:
		avoMaterna_falecimento=True
		falecimento=str(avoMaterna.falecimento)
		avoMaterna_falecimento_ano = falecimento.split("-")[0]

	avoMaternoR = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterno")
	if avoMaternoR.relacaoAntes == "Sim":
		avoMaternoR_relacaoAntes = True
		avoMaternoR_filhosAntes = avoMaternoR.filhosAntes
		avoMaternoR_filhasAntes = avoMaternoR.filhasAntes
	else:
		avoMaternoR_relacaoAntes = False
		avoMaternoR_filhosAntes =0
		avoMaternoR_filhasAntes = 0

	avoMaternoR_relacaoDepois = False
	avoMaternoR_filhosDepois = 0
	avoMaternoR_filhasDepois = 0
	if avoMaternoR.relacao == "Separados" or avoMaternoR.relacao == "Divorciados":
		if avoPaternoR.filhosDepois != 0 and avoPaternoR.filhosDepois != None:
			avoMaternoR_relacaoDepois = True
			avoMaternoR_filhosDepois = avoMaternoR.filhosDepois
			avoMaternoR_filhasDepois =  avoMaternoR.filhasDepois


	avoMaternaR = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterna")
	if avoMaternaR.relacaoAntes == "Sim":
		avoMaternaR_relacaoAntes = True
		avoMaternaR_filhosAntes = avoMaternaR.filhosAntes
		avoMaternaR_filhasAntes = avoMaternaR.filhasAntes
	else:
		avoMaternaR_relacaoAntes = False
		avoMaternaR_filhosAntes =0
		avoMaternaR_filhasAntes = 0

	avoMaternaR_relacaoDepois = False
	avoMaternaR_filhosDepois = 0
	avoMaternaR_filhasDepois = 0
	if avoMaternaR.relacao == "Separados" or avoMaternaR.relacao == "Divorciados":
		if avoMaternaR.filhosDepois != 0 and avoMaternaR.filhosDepois != None:
			avoMaternaR_relacaoDepois = True
			avoMaternaR_filhosDepois = avoMaternaR.filhosDepois
			avoMaternaR_filhasDepois =  avoMaternaR.filhasDepois


	iFinalX,iFinalY,iFinalMotherX,iFinalMotherY = drawMotherParents(iFinalX+40,iFinalY,16,avoMaternoR.relacao,
																	avoMaternoR.filhos,avoMaternoR.filhas,
																	avoMaternoR_relacaoAntes,avoMaternoR_filhosAntes,avoMaternoR.filhasAntes,
																	avoMaternoR_relacaoDepois,avoMaternoR_filhosDepois,avoMaternoR_filhasDepois,
																	avoMaternaR_relacaoAntes,avoMaternaR_filhosAntes,avoMaternaR_filhasAntes,
																	avoMaternaR_relacaoDepois,avoMaternaR_filhosDepois,avoMaternaR_filhasDepois,
																	avoMaterno_falecimento,avoMaterno_ano,avoMaterno_falecimento_ano,avoMaterno_nome,avoMaterna_falecimento,avoMaterna_ano,avoMaterna_falecimento_ano,avoMaterna_nome)


	pai = Familia.objects.get(usuario_id=paciente.id,parente="pai")
	pai_nome = pai.nome.split(" ")[0]
	nascimento=str(pai.nascimento)
	pai_ano = nascimento.split("-")[0]
	if pai.falecimento == None:
		pai_falecimento = False
		pai_falecimento_ano = ""
	else:
		pai_falecimento=True
		falecimento=str(pai.falecimento)
		pai_falecimento_ano = falecimento.split("-")[0]

	mae = Familia.objects.get(usuario_id=paciente.id,parente="mae")
	mae_nome = mae.nome.split(" ")[0]
	nascimento=str(mae.nascimento)
	mae_ano = nascimento.split("-")[0]
	if mae.falecimento == None:
		mae_falecimento = False
		mae_falecimento_ano = ""
	else:
		mae_falecimento=True
		falecimento=str(mae.falecimento)
		mae_falecimento_ano = falecimento.split("-")[0]

	drawPersonOfInterst(iFinalFatherX,iFinalFatherY,16,False,True,pai_falecimento,pai_ano,pai_falecimento_ano,pai_nome)
	drawPersonOfInterst(iFinalMotherX,iFinalMotherY+8,16,False,False,mae_falecimento,mae_ano,mae_falecimento_ano,mae_nome)

	paiR = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Pai")
	if paiR.relacaoAntes == "Sim":
		paiR_relacaoAntes = True
		paiR_filhosAntes = paiR.filhosAntes
		paiR_filhasAntes = paiR.filhasAntes
	else:
		paiR_relacaoAntes = False
		paiR_filhosAntes =0
		paiR_filhasAntes = 0

	paiR_relacaoDepois = False
	paiR_filhosDepois = 0
	paiR_filhasDepois = 0
	if paiR.relacao == "Separados" or paiR.relacao == "Divorciados":
		if paiR.filhosDepois != 0 and paiR.filhosDepois != None:
			paiR_relacaoDepois = True
			paiR_filhosDepois = paiR.filhosDepois
			paiR_filhasDepois =  paiR.filhasDepois


	maeR = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Mae")
	if maeR.relacaoAntes == "Sim":
		maeR_relacaoAntes = True
		maeR_filhosAntes = maeR.filhosAntes
		maeR_filhasAntes = maeR.filhasAntes
	else:
		maeR_relacaoAntes = False
		maeR_filhosAntes =0
		maeR_filhasAntes = 0

	maeR_relacaoDepois = False
	maeR_filhosDepois = 0
	maeR_filhasDepois = 0
	if maeR.relacao == "Separados" or maeR.relacao == "Divorciados":
		if maeR.filhosDepois != 0 and maeR.filhosDepois != None:
			maeR_relacaoDepois = True
			maeR_filhosDepois = maeR.filhosDepois
			maeR_filhasDepois =  maeR.filhasDepois

	if paciente.sexo == "Masculino":
		paciente_sexo = True
	else:
		paciente_sexo = False



	iSubjectX,iSubjectY = drawBeginingFamily(iFinalFatherX,iFinalFatherY,iFinalMotherX,iFinalMotherY,16,paiR.relacao,paiR.filhos,paiR.filhas,
											 paciente_sexo,paiR_relacaoAntes,paiR_filhosAntes,paiR_filhasAntes,
											 paiR_relacaoDepois,paiR_filhosDepois,paiR_filhasDepois,
											 maeR_relacaoAntes,maeR_filhosAntes,maeR_filhasAntes,
											 maeR_relacaoDepois,maeR_filhosDepois,maeR_filhasDepois)

	nome = paciente.nome.split(" ")[0]
	if paciente.sexo == "Feminino":
		sexo = False
	else:
		sexo = True
	nascimento=str(paciente.nascimento)
	ano = nascimento.split("-")[0]

	drawPersonOfInterst(iSubjectX,iSubjectY+10,16,True,sexo,False,ano,"",nome)


	pacienteR = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Paciente")
	if pacienteR.relacaoAntes == "Sim":
		pacienteR_relacaoAntes = True
		pacienteR_filhosAntes = pacienteR.filhosAntes
		pacienteR_filhasAntes = pacienteR.filhasAntes
	else:
		pacienteR_relacaoAntes = False
		pacienteR_filhosAntes =0
		pacienteR_filhasAntes = 0

	pacienteR_relacaoDepois = False
	pacienteR_filhosDepois = 0
	pacienteR_filhasDepois = 0
	if pacienteR.relacao == "Separado(a)" or pacienteR.relacao == "Divorciado(a)":
		if pacienteR.filhosDepois != 0 and pacienteR.filhosDepois != None:
			pacienteR_relacaoDepois = True
			pacienteR_filhosDepois = pacienteR.filhosDepois
			pacienteR_filhasDepois =  pacienteR.filhasDepois


	conjugeR = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Conjuge")
	if conjugeR.relacaoAntes == "Sim":
		conjugeR_relacaoAntes = True
		conjugeR_filhosAntes = conjugeR.filhosAntes
		conjugeR_filhasAntes = conjugeR.filhasAntes
	else:
		conjugeR_relacaoAntes = False
		conjugeR_filhosAntes =0
		conjugeR_filhasAntes = 0

	conjugeR_relacaoDepois = False
	conjugeR_filhosDepois = 0
	conjugeR_filhasDepois = 0
	if conjugeR.relacao == "Separado(a)" or conjugeR.relacao == "Divorciado(a)":
		if conjugeR.filhosDepois != 0 and conjugeR.filhosDepois != None:
			conjugeR_relacaoDepois = True
			conjugeR_filhosDepois = conjugeR.filhosDepois
			conjugeR_filhasDepois =  conjugeR.filhasDepois


	iSposeX,iSposeY = drawIndexFamily(iSubjectX,iSubjectY,paciente_sexo,16,pacienteR.relacao,
									  pacienteR.filhos,pacienteR.filhas,
									  pacienteR_relacaoAntes,pacienteR_filhosAntes,pacienteR_filhasAntes,
									  pacienteR_relacaoDepois,pacienteR_filhosDepois,pacienteR_filhasDepois,
									  conjugeR_relacaoAntes,conjugeR_filhosAntes,conjugeR_filhasAntes,
									  conjugeR_relacaoDepois,conjugeR_filhosDepois,conjugeR_filhasDepois)



	conjuge = Familia.objects.get(usuario_id=paciente.id,parente="conjuge")
	conjuge_nome = conjuge.nome.split(" ")[0]
	nascimento=str(conjuge.nascimento)
	conjuge_ano = nascimento.split("-")[0]
	if conjuge.sexo == "Masculino":
		conjuge_sexo =  True
	else:
		conjuge_sexo = False

	drawPersonOfInterst(iSposeX,iSposeY-10,16,False,conjuge_sexo,False,conjuge_ano,"",conjuge_nome)

	ctx.show_page()

