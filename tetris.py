#############################################################################
#                                                                           #
#   tetris.py is Copyright, Nathan Dumont 2007                              #
#       email: hairymnstr@gmail.com                                         #
#       website: http://www.nathandumont.com/node/167                       #
#                                                                           #
#   tetris.py is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   tetris.py is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with Remote Control.  If not, see <http://www.gnu.org/licenses/>. #
#                                                                           #
#############################################################################

import curses, random, time

class game_piece:
	def __init__(self):
		self.change_shape()
	
	def change_shape(self):
		shapes=[]
		shapes.append([[1,1,0,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]])
		shapes.append([[0,1,1,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]])
		shapes.append([[1,1,1,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
		shapes.append([[1,1,0,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]])
		shapes.append([[1,1,1,0],[0,0,1,0],[0,0,0,0],[0,0,0,0]])
		shapes.append([[1,1,1,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]])
		widths=[]
		widths.append(3)
		widths.append(3)
		widths.append(4)
		widths.append(2)
		widths.append(3)
		widths.append(3)
		heights=[]
		heights.append(2)
		heights.append(2)
		heights.append(1)
		heights.append(2)
		heights.append(2)
		heights.append(2)
		s=random.randint(0,5)
		self.shape=shapes[s]
		self.height=heights[s]
		self.width=widths[s]
		d=random.randint(0,3)
		self.direction=d

	def clear_left(self):
		return self.cleft
	
	def clear_right(self):
		return self.cright
	
	def turn_c(self,bits):
		overlap=0
		self.direction=self.direction+1
		if self.direction>3:
			self.direction=0
		
		if self.overlap(bits):
			self.direction=self.direction-1
			if self.direction<0:
				self.direction=3

	def overlap(self,bits):
		ovl=0
		for h in range(self.height):
			for w in range(self.width):
				if self.shape[h][w]==1:
					if self.direction==0:
						yt=y+h
						xt=x+w
					elif self.direction==1:
						yt=y+w
						xt=x+((self.height-1)-h)
					elif self.direction==2:
						yt=y+((self.height-1)-h)
						xt=x+((self.width-1)-w)
					elif self.direction==3:
						yt=y+((self.width-1)-w)
						xt=x+h
					if xt-4<0:
						ovl=1
					elif xt-4>9:
						ovl=1
					elif bits[yt-3][xt-4]==1:
						ovl=1
		return ovl

	def turn_ac(self,bits):
		self.direction=self.direction-1
		if self.direction<0:
			self.direction=3
		
		if self.overlap(bits):
			self.direction=self.direction-1
			if self.direction>3:
				self.direction=0

	
	def draw(self,y,x,screen,bits):
		self.cleft=1
		self.cright=1
		self.falling=1
		for h in range(self.height):
			for w in range(self.width):
				if self.shape[h][w]==1:
					if self.direction==0:
						yt=y+h
						xt=x+w
					elif self.direction==1:
						yt=y+w
						xt=x+((self.height-1)-h)
					elif self.direction==2:
						yt=y+((self.height-1)-h)
						xt=x+((self.width-1)-w)
					elif self.direction==3:
						yt=y+((self.width-1)-w)
						xt=x+h
					screen.addstr(yt,xt,"@")
					if bits[yt-2][xt-4]==1:
						self.falling=0
					if xt-5<0:
						self.cleft=0
					elif bits[yt-3][xt-5]==1:
						self.cleft=0
					if xt-3>9:
						self.cright=0
					elif bits[yt-3][xt-3]==1:
						self.cright=0

	def update_bits(self,y,x,bits):
		for h in range(self.height):
			for w in range(self.width):
				if self.shape[h][w]==1:
					if self.direction==0:
						bits[y+h-3][x+w-4]=1
					elif self.direction==1:
						bits[y+w-3][x+((self.height-1)-h)-4]=1
					elif self.direction==2:
						bits[y+((self.height-1)-h-3)][x+((self.width-1)-w)-4]=1
					elif self.direction==3:
						bits[y+((self.width-1)-w)-3][x+h-4]=1
		return bits

	def get_width(self):
		if self.direction==1 or self.direction==3:
			return self.height
		elif self.direction==0 or self.direction==2:
			return self.width

def draw_frame():
	myscreen.addstr(2,3,"############")
	for n in range(3,15):
		myscreen.addstr(n,3,"#          #")
	myscreen.addstr(15,3,"############")

myscreen=curses.initscr()

curses.noecho()
curses.curs_set(0)
piece=game_piece()
qui=1
while qui:
	n=0
	x=8
	y=3
	points=0
	
	bits=[[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]]
	curses.halfdelay(1)
	t=time.time()
	while 1:
		c=myscreen.getch()
		if c==ord('q'):
			break
		elif c==ord('w'):
			piece.turn_c(bits)
		elif c==ord('a'):
			x=x-piece.cleft
		elif c==ord('d'):
			x=x+piece.cright
		elif c==ord('s'):
			if piece.falling and fall_temp:
				y=y+1
		fall_temp=1
		draw_frame()
		try:
			piece.draw(y,x,myscreen,bits)
		except:
			break
		for j in range(12):
			for i in range(10):
				if bits[j][i]==1:
					myscreen.addstr(j+3,i+4,"%")
		if time.time()-t>0.5:
			if piece.falling==0:
				bits=piece.update_bits(y,x,bits)
				x=8
				y=3
				piece.change_shape()
				if piece.overlap(bits):
					break
			y=y+piece.falling
			fall_temp=not piece.falling
			t=time.time()
			tpoints=0
			for j in range(12):
				if bits[j]==[1,1,1,1,1,1,1,1,1,1]:
					for k in range(j,0,-1):
						bits[k]=bits[k-1]
						bits[0]=[0,0,0,0,0,0,0,0,0,0]
					if tpoints:
						tpoints=tpoints*2
					else:
						tpoints=1
			points=points+tpoints
			myscreen.addstr(1,3,"Score: "+str(points))

	myscreen.refresh()

	myscreen.addstr(8,3,"            ")
	myscreen.addstr(9,3," You Loose  ")
	myscreen.addstr(10,3,"            ")
	myscreen.addstr(11,3," q to quit  ")
	myscreen.addstr(12,3,"            ")
	myscreen.addstr(13,3," p to play  ")
	myscreen.addstr(14,3,"            ")
	while 1:
		c=myscreen.getch()
		if c==ord('q'):
			qui=0
			break
		elif c==ord('p'):
			break
	myscreen.refresh()
curses.echo()
curses.endwin()