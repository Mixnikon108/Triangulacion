import numpy as np 
import matplotlib.pyplot as plt



def radianes(grados):
	return grados * (np.pi/180)


def what_is_triangular_I():
	print('When both alpha and betha are less than 90º degrees.')
	print('Here is an example of how should looks like')

	
	plt.figure('Example of triangular I') 
	x = [1, 3, 2.25, 1]
	y = [1, 1,  2.5, 1]

	plt.plot(x, y, 'r--')

	x = [2.25, 2.25]
	y = [1,  2.5]

	plt.plot(x, y, 'g--')
		
	plt.grid()
	plt.show()	



def what_is_triangular_II():
	print('When at least alpha or betha is bigger than 90º degrees.')
	print('Here is an example of how should looks like')

	
	plt.figure('Example of triangular II')
	x = [1, 3, 5, 1]
	y = [1, 1, 4, 1]

	plt.plot(x, y, 'r--')

	x = [3, 5, 5]
	y = [1, 1, 4]

	plt.plot(x, y, 'g--')
		
	plt.grid()
	plt.show()	



def triangular_I(alpha, betha, lenght):
	senAlpha = np.sin(alpha)
	senBetha = np.sin(betha)

	tanAlpha = np.tan(alpha)
	tanBetha = np.tan(betha)

	dist_inter_alpha = (lenght * tanBetha) / (tanAlpha + tanBetha) 
	high = tanAlpha * dist_inter_alpha	
		
	dist_to_alpha = high / senAlpha
	dist_to_betha = high / senBetha

	return high, dist_to_alpha, dist_to_betha, dist_inter_alpha	


def triangular_II(alpha, betha, lenght):
	senAlpha = np.sin(alpha)
	senBetha = np.sin(betha)

	tanAlpha = np.tan(alpha)
	tanBetha = np.tan(betha)

	dist_inter_alpha = (lenght * tanAlpha) / (tanBetha - tanAlpha)
	high = tanBetha * dist_inter_alpha	
		
	dist_to_alpha = high / senAlpha
	dist_to_betha = high / senBetha

	return high, dist_to_alpha, dist_to_betha, dist_inter_alpha	


def norma(A_vector:tuple, B_vector:tuple):
	X_a = A_vector[0]
	Y_a = A_vector[1]

	X_b = B_vector[0]
	Y_b = B_vector[1]

	return np.sqrt(((X_a - X_b))**2 + ((Y_a - Y_b))**2)



class Triangular_plotter:
	def __init__(self, dist_to_inter, triangle_height, lenght, dist_to_alpha, dist_to_betha):
		self.dist_to_inter   = dist_to_inter
		self.triangle_height = triangle_height
		self.dist_to_alpha   = dist_to_alpha
		self.dist_to_betha   = dist_to_betha
		self.lenght = lenght
	
	def __C_pnt_I(self, A_vector:tuple, B_vector:tuple, twist_side):
		X_a = A_vector[0]
		Y_a = A_vector[1]

		X_b = B_vector[0]
		Y_b = B_vector[1]

		vect_X = X_b - X_a
		vect_Y = Y_b - Y_a

		norma = np.sqrt((vect_X)**2 +  (vect_Y)**2)

		vect_uni_X = vect_X/norma
		vect_uni_Y = vect_Y/norma

		inter_X = vect_uni_X * self.dist_to_inter + X_a
		inter_Y = vect_uni_Y * self.dist_to_inter + Y_a

		if twist_side == False:
			vect_uni_Y = -vect_uni_Y
			vect_uni_X = -vect_uni_X

		X_c = -vect_uni_Y * self.triangle_height + inter_X  
		Y_c =  vect_uni_X * self.triangle_height + inter_Y

		return X_c, Y_c, inter_X, inter_Y

	def __C_pnt_II(self, A_vector:tuple, B_vector:tuple, twist_side):
		X_a = A_vector[0]
		Y_a = A_vector[1]

		X_b = B_vector[0]
		Y_b = B_vector[1]

		vect_X = X_b - X_a
		vect_Y = Y_b - Y_a

		norma = np.sqrt((vect_X)**2 +  (vect_Y)**2)

		vect_uni_X = vect_X/norma
		vect_uni_Y = vect_Y/norma

		inter_X = vect_uni_X * (self.lenght + self.dist_to_inter) + X_a
		inter_Y = vect_uni_Y * (self.lenght + self.dist_to_inter) + Y_a
			
		if twist_side == False:
			vect_uni_Y = -vect_uni_Y
			vect_uni_X = -vect_uni_X

		X_c = -vect_uni_Y * self.triangle_height + inter_X  
		Y_c =  vect_uni_X * self.triangle_height + inter_Y
			
		return X_c, Y_c, inter_X, inter_Y


	def plot(self, A_vector:tuple, B_vector:tuple, Triangulation_type, twist_side=True, path=None, X_size=900, Y_size=600, fontsize=10, title='Map', figure_title='Triangulacion geodesica'):
		X_a = A_vector[0]
		Y_a = A_vector[1]

		X_b = B_vector[0]
		Y_b = B_vector[1]

		if Triangulation_type   == 'I':
			X_c, Y_c, inter_X, inter_Y = self.__C_pnt_I(A_vector, B_vector, twist_side)

		elif Triangulation_type == 'II':
			X_c, Y_c, inter_X, inter_Y = self.__C_pnt_II(A_vector, B_vector, twist_side)
		


		fig, ax = plt.subplots()
		ax.set_title(title)
		fig.canvas.set_window_title(figure_title) 

		if path != None:
			img = plt.imread(path)
			ax.imshow(img, extent=[0, X_size, 0, Y_size])
		else:
			plt.gca().set_aspect('equal')


		x = [X_a, X_b, X_c, X_a]
		y = [Y_a, Y_b, Y_c, Y_a]

		ax.text(X_a, Y_a,  f'A({X_a:.2f}, {Y_a:.2f})', fontsize=fontsize)
		ax.text(X_b, Y_b,  f'B({X_b:.2f}, {Y_b:.2f})', fontsize=fontsize)
		ax.text(X_c, Y_c,  f'C({X_c:.2f}, {Y_c:.2f})', fontsize=fontsize)

		mid_AB_X = (X_b - X_a)/2 + X_a 
		mid_AB_Y = (Y_b - Y_a)/2 + Y_a 
		ax.text(mid_AB_X, mid_AB_Y, f'{self.lenght:.2f}', fontsize=fontsize)

		mid_AX_c = (X_c - X_a)/2 + X_a 
		mid_AY_c = (Y_c - Y_a)/2 + Y_a 
		ax.text(mid_AX_c, mid_AY_c, f'{self.dist_to_alpha:.2f}', fontsize=fontsize)

		mid_BX_c = (X_c - X_b)/2 + X_b 
		mid_BY_c = (Y_c - Y_b)/2 + Y_b 
		ax.text(mid_BX_c, mid_BY_c, f'{self.dist_to_betha:.2f}', fontsize=fontsize)

		ax.plot(x, y, 'r--')

		if Triangulation_type   == 'I':
			x = [inter_X, X_c]
			y = [inter_Y, Y_c]

		elif Triangulation_type == 'II':
			x = [X_b, inter_X, X_c]
			y = [Y_b, inter_Y, Y_c]

		mid_KX_c = (inter_X - X_c)/2 + X_c 
		mid_KY_c = (inter_Y - Y_c)/2 + Y_c 
		ax.text(mid_KX_c, mid_KY_c, f'{self.triangle_height:.2f}', fontsize=fontsize)

		ax.plot(x, y, 'g--')
		
		plt.grid()
		plt.show()


lenght = norma((204,259), (275,492))

high, dist_to_alpha, dist_to_betha, dist_inter_alpha = triangular_I(radianes(60), radianes(76), lenght)


triangular = Triangular_plotter(dist_inter_alpha, high, lenght, dist_to_alpha, dist_to_betha)

triangular.plot((204,259), (275,492), Triangulation_type='I', twist_side=False, path='plano.png')

