import random
import pygame
import sys
#render given list(map)
#A*
def xrender(ex):
	boi=""#boi
	for i in range(len(ex[0])):
		for j in range(len(ex)):
			if(type(ex[j][i]) is tuple):
				boi+=str(ex[j][i][0])
			else:
				boi+=str(ex[j][i])		#boi get map
		boi+="\n"
	print(boi)#boi is print
#map generate class
class mapgen():
	#make base for map creation(mx=map width,my = map height)
	def base(self,mx,my):
		x=[]
		for i in range(mx):
			y = []
			for j in range(my):
				y.append('.')
			x.append(y)
		rmap = x
		return rmap
	def base2(self,mx,my):
		x=[]
		for i in range(mx):
			y = []
			for j in range(my):
				y.append(0)
			x.append(y)
		rmap = x
		return rmap
	#coordinate: x: left to right y: top to bottom
	def checkclip(self,rs,rsp,sm):
		for i in range(rs[1]):
			for j in range(rs[0]):
				if(sm[rsp[0]+j][rsp[1]+i]!='.'):
					return 0
		return 1

	#make rooms roomsize includes wall block
	def roomm(self,roomsetting,selmap):
		maxr = roomsetting[0]
		maxx = roomsetting[1]
		maxy = roomsetting[2]	
		
		r = []
		for e in range(maxr):
			roomsize = (random.randint(3,maxx),random.randint(3,maxy))
			Roomsp = (random.randint(0,len(selmap)-roomsize[0]),random.randint(0,len(selmap[0])-roomsize[1]))
			if(self.checkclip(roomsize,Roomsp,selmap)==0):
				while(self.checkclip(roomsize,Roomsp,selmap)!=1):
					roomsize = (random.randint(3,maxx),random.randint(3,maxy))
					Roomsp = (random.randint(0,len(selmap)-roomsize[0]),random.randint(0,len(selmap[0])-roomsize[1]))
			for i in range(roomsize[1]):
				for j in range(roomsize[0]):
					selmap[Roomsp[0]+j][Roomsp[1]+i] = 'r'
			roominfo = (Roomsp[0],Roomsp[1],Roomsp[0]+roomsize[0]-1,Roomsp[1]+roomsize[1]-1,roomsize[0],roomsize[1])
			r.append(roominfo)
		return r
	def RGStage2(self,bs,rd):
		for v in range(len(rd)):
			for i in range(rd[v][5]):
				for j in range(rd[v][4]):
					bs[rd[v][0]+j][rd[v][1]+i] = 'r'
					if(i==0 or i==rd[v][5]-1 or j==0 or j==rd[v][4]-1):
						bs[rd[v][0]+j][rd[v][1]+i] = 'w'
		return bs
	def makedoor(self,bs,rd):
		temap = bs
		dorta = []
		for i in range(len(rd)):
			c=1
			chance = 2*(rd[i][4]+rd[i][5])
			while(c==1):
				chance -= 1
				if(chance<=0):
					break
				v=random.randint(0,3)
				if(rd[i][v]==0 or rd[i][v]==len(temap)-1 or rd[i][v]==len(temap[0])-1):
					while(rd[i][v]==0 or rd[i][v]==len(temap)-1 or rd[i][v]==len(temap[0])-1):
						v=random.randint(0,3)
				if(v==0 or v==2):
					dx = rd[i][v]
					reee = random.randint(rd[i][1]+1,rd[i][3]-1)
					xr = 0
					fx = dx-1+v
					if(temap[dx-1+v][reee]!='.'):
						while(temap[dx-1+v][reee]!='.' and xr<3):
							reee = random.randint(rd[i][1]+1,rd[i][3]-1)
							xr +=1
					if(xr>=3):
						c=1
						continue
					dy = reee
					fy =dy
					xde = 0
				if(v==1 or v==3):
					dy = rd[i][v]
					reee = random.randint(rd[i][0]+1,rd[i][2]-1)
					xr = 0
					fy = dy-2+v
					if(temap[reee][dy]!='.'):
						while(temap[reee][fy]!='.' and xr<3):
							reee = random.randint(rd[i][0]+1,rd[i][2]-1)
							xr +=1
					if(xr>=3):
						c=1
						continue
					dx = reee
					fx = dx
					xde = 1
				dorta.append((dx,dy,fx,fy,v,i))
				c=0
		return dorta



	def makepath(self,bs,dd,time):
		for i in range(len(dd)):
			bs[dd[i][0]][dd[i][1]] = 'd'
			bs[dd[i][2]][dd[i][3]] = 'g'
		histori = []
		global dump
		for i in range(len(dd)):
			king = 'x'
			nummax = 9000#
			for j in range(len(dd)):
				if(time==0):
					if(dd[i][5] == dd[j][5]):
						continue
				if(time==1):
					if(dd[i][5] == dd[j][5] or (dd[i][5],dd[j][5]) in histori or (dd[j][5],dd[i][5]) in histori):
						continue
				if(dd[j][2]+dd[j][3]<nummax):
					nummax = dd[j][2]+dd[j][3]
					king = j
			histori.append((dd[i][5],dd[j][5]))
			if(king=='x'):
				continue
			boi = king
			loc = [dd[i][2],dd[i][3]]
			starter = loc
			target =[dd[king][2],dd[king][3]]
			bc = bs
			blacklist=[]
			blacktime=0
			while(loc!=target):
				king = 'x'
				nummax = 9000
				prevway = 50
				for j in range(4):
					if(j==0):
						think=(loc[0]+1,loc[1])
					if(j==1):
						think=(loc[0],loc[1]+1)
					if(j==2):
						think=(loc[0]-1,loc[1])
					if(j==3):
						think=(loc[0],loc[1]-1)
					if(think[0]>=len(bc) or think[0]<0 or think[1]>=len(bc[0]) or think[1]<0):
						continue
					if(bc[think[0]][think[1]]!='.' and bc[think[0]][think[1]]!='g' ):
						continue
					test = abs(think[0]-target[0])+abs(think[1]-target[1])
					if(test<nummax):
						king = think
						nummax = test
						wae = j
					elif(test==nummax):
						if(random.randint(0,1)==1):
							king = think
							nummax = test
							wae = j
				wae = prevway
				if(king=='x'):
					blacklist.append(tuple(loc))
					blacktime+=1
					bc = bs
					if(blacktime>=500):
						dump.append((dd[i][4],dd[i][5]))
						break
					for p in blacklist:
						bc[p[0]][p[1]]='rx'
					loc = starter
				else:
					loc = [king[0],king[1]]
					bc[loc[0]][loc[1]]='wt'
			bc[starter[0]][starter[1]] = 'wt'
			if(loc==target):
				bs=bc
				for j in range(len(bs[0])):
					for k in range(len(bs)):
						if(bs[k][j]=='wt'):
							bs[k][j]='g'
						if(bs[k][j]=='rx'):
							bs[k][j]='.'
		for j in range(len(bs[0])):
			for k in range(len(bs)):
				if(bs[k][j]=='wt'):
					bs[k][j]='g'
				if(bs[k][j]=='rx'):
					bs[k][j]='.'
		return bs


	def makedoorvar(self,bs,rd,dd):
		global dump
		temap = bs
		dorta = []
		for i in dump:
			chance = 4
			c=1
			while(c==1):
				chance -= 1
				if(chance<=0):
					break
				v=random.randint(0,3)
				if(v==i[0] or rd[i[1]][v]==0 or rd[i[1]][v]==len(temap)-1 or rd[i[1]][v]==len(temap[0])-1):
					while(v==i[0] or rd[i[1]][v]==0 or rd[i[1]][v]==len(temap)-1 or rd[i[1]][v]==len(temap[0])-1):
						v=random.randint(0,3)
				if(v==0 or v==2):
					dx = rd[i[1]][v]
					reee = random.randint(rd[i[1]][1]+1,rd[i[1]][3]-1)
					xr = 0
					fx = dx-1+v
					if(temap[fx][reee]!='.' and temap[fx][reee]!='g'):
						while(temap[fx][reee]!='.' and temap[fx][reee]!='g' and xr<3):
							reee = random.randint(rd[i[1]][1]+1,rd[i[1]][3]-1)
							xr +=1
					if(xr>=3):
						c=1
						continue
					dy = reee
					fy =dy
					xde = 0
				if(v==1 or v==3):
					dy = rd[i[1]][v]
					reee = random.randint(rd[i[1]][0]+1,rd[i[1]][2]-1)
					xr = 0
					fy = dy-2+v
					if(temap[reee][fy]!='.'and temap[reee][fy]!='g'):
						while(temap[reee][fy]!='.'and temap[reee][fy]!='g' and xr<3):
							reee = random.randint(rd[i[1]][0]+1,rd[i[1]][2]-1)
							xr +=1
					if(xr>=3):
						c=1
						continue
					dx = reee
					fx = dx
					xde = 1
				dorta.append((dx,dy,fx,fy,v,i[1]))
				c=0
		return dd+dorta
	
	def MR(self,mx,my,rd,dd):
		x=[]
		for i in range(mx):
			y = []
			for j in range(my):
				y.append('.')
			x.append(y)
		rmap = x
		for v in range(len(rd)):
			for i in range(rd[v][5]):
				for j in range(rd[v][4]):
					rmap[rd[v][0]+j][rd[v][1]+i] = v
					if(i==0 or i==rd[v][5]-1 or j==0 or j==rd[v][4]-1):
						rmap[rd[v][0]+j][rd[v][1]+i] = ('w',v)
		for i in dd:
			rmap[i[0]][i[1]] = ('d',i[5])
		return rmap

	def spawnpoint(self,rd):
		eeta = []
		v = random.randint(0,len(rd)-1)
		vx = random.randint(rd[v][0]+1,rd[v][2]-1)
		vy = random.randint(rd[v][1]+1,rd[v][3]-1)
		eeta.append((vx,vy,v))
		while(v==eeta[0][2]):
			v = random.randint(0,len(rd)-1)
		vx = random.randint(rd[v][0]+1,rd[v][2]-1)
		vy = random.randint(rd[v][1]+1,rd[v][3]-1)
		eeta.append((vx,vy,v))
		return eeta



	def truemap(self,bs,rd,dd,veta):
		for v in range(len(rd)):
			for i in range(rd[v][5]):
				for j in range(rd[v][4]):
					if(i==0 and j==0):
						bs[rd[v][0]+j][rd[v][1]+i] = 'wc1'
					elif(i==0 and j==rd[v][4]-1):
						bs[rd[v][0]+j][rd[v][1]+i] = 'wc2'
					elif(i==rd[v][5]-1 and j==0):
						bs[rd[v][0]+j][rd[v][1]+i] = 'wc3'
					elif(i==rd[v][5]-1 and j==rd[v][4]-1):
						bs[rd[v][0]+j][rd[v][1]+i] = 'wc4'
					elif(i==0 or i==rd[v][5]-1):
						bs[rd[v][0]+j][rd[v][1]+i] = 'wx1'
					elif(j==0 or j==rd[v][4]-1):
						bs[rd[v][0]+j][rd[v][1]+i] = 'wx2'
					else:
						bs[rd[v][0]+j][rd[v][1]+i] = 'g'
		for i in range(len(dd)):
			bs[dd[i][0]][dd[i][1]] = 'd'
		bs[veta[0]][veta[1]] = 'exit'
		return bs


'''		
	def doorlabel(bs,dd):
						
class avatar():
	loc = [0,0]
	hp = 100
	score = 0
	attackpower=0
	items=[]
'''




pygame.init()
pygame.font.init()
size = width, height = 910,651
screen = pygame.display.set_mode(size)
gmap = mapgen()
sizex = 70
sizey = 30
floor = 0
consfont = pygame.font.SysFont('Lucida Console',20)
xvalue = {'wc1':('╔',(255,255,255)),'wc2':('╗',(255,255,255)),
'wc3':('╚',(255,255,255)),'wc4':('╝',(255,255,255)),
'wx1':('═',(255,255,255)),'wx2':('║',(255,255,255)),
'd':('▒',(255,255,255)),'g':('.',(255,255,255)),
'.':(' ',(255,255,255)),'me':('@',(255,0,0)),'exit':('#',(64,64,255))}
screen.fill((0,0,0))
path = ('d','g','exit')


while(1):
	#makemap
	floor+=1
	if(floor==61):
		break
	level = floor//10+1
	roomsetg = [level*5,20-(level-1)*2,10-(level-1)]
	dump= []
	basemap = gmap.base(sizex,sizey)
	roomdata= gmap.roomm(roomsetg,basemap)
	basemap = gmap.RGStage2(basemap,roomdata)
	doordata = gmap.makedoor(basemap,roomdata)
	testmap = basemap
	basemap = gmap.makepath(basemap,doordata,0)
	doordata = gmap.makedoorvar(testmap,roomdata,doordata)
	basemap = gmap.makepath(testmap,doordata,1)
	reeeta = gmap.spawnpoint(roomdata)
	meloc = [reeeta[0][0],reeeta[0][1]]
	endloc = (reeeta[1][0],reeeta[1][1])
	endmap = gmap.truemap(basemap,roomdata,doordata,endloc)
	roommap = gmap.MR(sizex,sizey,roomdata,doordata)
	viewmap = gmap.base2(sizex,sizey)
	viewarea = [reeeta[0][2]]
	prevloc=(meloc[0],meloc[1])
	#mapcreate end
	ap = 2800
	gamestate = 1
	out = 0
	pygame.key.set_repeat(1,100)
	while(gamestate):
		if(ap<=0):
			gamestate=0
			break
		if(endmap[meloc[0]][meloc[1]]=='exit'):
			break
		if(type(roommap[meloc[0]][meloc[1]]) is tuple):
			viewarea = roommap[meloc[0]][meloc[1]][1]
		elif(type(roommap[meloc[0]][meloc[1]]) is int):
			viewarea = roommap[meloc[0]][meloc[1]]
		else:
			viewarea = 'gro'
		viewmap[prevloc[0]][prevloc[1]]=1
		for i in range(5):
			x=meloc[0]-2+i
			if(x<0 or x>=len(viewmap)):
				continue
			for j in range(5):
				y=meloc[1]-2+j
				if(y<0 or y>=len(viewmap[0])):
					continue
				if(type(roommap[x][y]) is tuple):
					if(roommap[x][y][1]==viewarea or viewarea=='gro'):
						viewmap[x][y]=1
				elif(roommap[x][y]==viewarea):
					viewmap[x][y]=1
				elif(viewarea=='gro'):
					if(type(roommap[x][y]) is str):
						viewmap[x][y]=1		
		viewmap[meloc[0]][meloc[1]] = 2
		screen.fill((0,0,0))
		screen.blit(consfont.render('floor:'+str(floor)+' AP:'+str(ap),False,(255,255,255)),(j*13,0))
		for i in range(len(endmap[0])):
			for j in range(len(endmap)):
				if(viewmap[j][i]==1):
					r = xvalue[endmap[j][i]]
					textmaprend = consfont.render(r[0],False,r[1])
				elif(viewmap[j][i]==2):
					r = xvalue['me']
					textmaprend = consfont.render(r[0],False,r[1])
				elif(viewmap[j][i]==0):
					textmaprend = consfont.render(' ',False,(255,255,255))
				screen.blit(textmaprend,(j*13,(i+1)*21))
		pygame.display.flip()
		prevloc = (meloc[0],meloc[1])
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if(event.key == pygame.K_UP and basemap[meloc[0]][meloc[1]-1] in path):
					meloc[1]-=1
					ap-=1
					#break
				if(event.key == pygame.K_DOWN and meloc[1]!=len(viewmap[0])-1 and basemap[meloc[0]][meloc[1]+1] in path):
					meloc[1]+=1
					ap-=1
					#break
				if(event.key == pygame.K_LEFT and meloc[0]!=0 and basemap[meloc[0]-1][meloc[1]] in path):
					meloc[0]-=1
					ap-=1
					#break
				if(event.key == pygame.K_RIGHT and meloc[0]!=len(viewmap)-1 and basemap[meloc[0]+1][meloc[1]] in path):
					meloc[0]+=1
					ap-=1
					#break
				if event.key == pygame.K_ESCAPE:
					raise SystemExit
	if(gamestate==0):
		screen.fill((0,0,0))
		screen.blit(consfont.render('game is over, press enter to quit(last floor:'+str(floor)+')',False,(255,255,255)),(0,0))
		pygame.display.flip()
		pygame.key.set_repeat(0,0)
		while(1):
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.KEYDOWN: raise SystemExit


screen.fill((0,0,0))
screen.blit(consfont.render('winner, press enter to  quit (60 floors cleared)',False,(255,255,255)),(0,0))
pygame.display.flip()
pygame.key.set_repeat(0,0)
while(1):
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN: raise SystemExit