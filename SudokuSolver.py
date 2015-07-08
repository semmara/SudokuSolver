import sys

DEBUG = False

class Values(object):
	def __init__(self):
		pass

	@staticmethod
	def check_array_for_duplicate_values(arr):
		while True:
			try:
				arr.remove(None)
			except:
				break
		if len(arr) != len(set(arr)):
			return False
		return True


class Block(object):
	"""
	0 1 2
	3 4 5
	6 7 8
	"""
	def __init__(self, edge_len=3):
		self.edge_len = edge_len
		self.fields = [None for _ in range(self.edge_len*self.edge_len)]

	def _check_row_numb(self, numb):
		if numb > self.edge_len-1 or numb < 0:
			return False
		return True

	def _check_col_numb(self, numb):
		if numb > self.edge_len-1 or numb < 0:
			return False
		return True

	def get_row(self, numb):
		if not self._check_row_numb(numb):
			raise
		return self.fields[self.edge_len*numb:self.edge_len*numb+self.edge_len]

	def get_col(self, numb):
		if not self._check_col_numb(numb):
			raise
		return [self.fields[i] for i in range(self.edge_len*self.edge_len) if i%self.edge_len == numb]

	def get_field(self, field_numb):
		return self.fields[field_numb]

	def set_field(self, field_numb, value):
		if self.fields[field_numb] is None:
			self.fields[field_numb] = value
			return True
		return False

	def set_total(self, list_of_values):
		if not isinstance(list_of_values, list):
			return False
		if len(list_of_values) != self.edge_len*self.edge_len:
			return False
		self.fields = list_of_values[:]
		return True

	def check(self):
		return Values.check_array_for_duplicate_values(self.fields[:])

	def check_for_empty_fields(self):
		f = self.fields[:]
		while True:
			try:
				f.remove(None)
			except:
				break
		return self.edge_len*self.edge_len-len(f)

	def get_list_of_empty_fields(self):
		return [i for i in range(self.edge_len*self.edge_len) if self.fields[i] is None]

	def get_list_of_empty_fields_in_row(self, row_numb):
		if not self._check_row_numb(row_numb):
			raise
		return [i for i in range(row_numb*self.edge_len, (row_numb+1)*self.edge_len) if self.fields[i] is None]

	def get_list_of_empty_fields_in_col(self, col_numb):
		if not self._check_col_numb(col_numb):
			raise
		return [i for i in range(col_numb, self.edge_len*self.edge_len, self.edge_len) if self.fields[i] is None]

	def has_value(self, value):
		return value in self.fields

	def row_has_value(self, row_numb, value):
		return value in self.get_row(row_numb)

	def col_has_value(self, col_numb, value):
		return value in self.get_col(col_numb)

class Gamefield(object):
	"""
	Block0 Block1 Block2
	Block3 Block4 Block5
	Block6 Block7 Block8
	"""
	def __init__(self, list_of_list_of_values):
		self.blocks = [Block() for _ in range(9)]
		self.set(list_of_list_of_values)

	def set(self, list_of_list_of_values):
		for i in range(9):
			self.blocks[i].set_total(list_of_list_of_values[i])

	def set_field_by_row_and_col(self, value, row_numb, col_numb):
		block_idx, block_row, block_col = self.get_block_by_row_and_col(row_numb, col_numb)
		self.blocks[block_idx].set_field(block_row*3+block_col, value)

	def set_field_by_blockidx_and_blockfield(self, value, block_idx, block_field):
		self.blocks[block_idx].set_field(block_field, value)

	def draw(self):
		for i in range(9):
			for elem in self.get_row(i):
				if elem is None:
					print "-",
				else:
					print elem,
			print

	def get_block(self, block_numb):
		return self.blocks[block_numb]

	def get_row(self, row_numb):
		if row_numb > 8 or row_numb < 0:
			raise
		blocks_row = row_numb/3
		block_row = row_numb%3
		row = self.blocks[blocks_row*3].get_row(block_row)
		row.extend(self.blocks[blocks_row*3+1].get_row(block_row))
		row.extend(self.blocks[blocks_row*3+2].get_row(block_row))
		return row

	def get_col(self, col_numb):
		if col_numb > 8 or col_numb < 0:
			raise
		blocks_col = col_numb/3
		block_col = col_numb%3
		col = self.blocks[blocks_col].get_col(block_col)
		col.extend(self.blocks[blocks_col+3].get_col(block_col))
		col.extend(self.blocks[blocks_col+6].get_col(block_col))
		return col

	def row_has_value(self, row_numb, value):
		if value in self.get_row(row_numb):
			return True
		return False

	def col_has_value(self, col_numb, value):
		if value in self.get_col(col_numb):
			return True
		return False

	def has_value(self, row_numb, col_numb):
		return self.get_value_by_row_and_col(row_numb, col_numb) is not None

	def check_row(self, row_numb):
		return Values.check_array_for_duplicate_values(self.get_row(row_numb))

	def check_col(self, col_numb):
		return Values.check_array_for_duplicate_values(self.get_col(col_numb))

	def check(self):
		for i in range(9):
			if not self.check_row(i):
				return False
			if not self.check_col(i):
				return False
			if not self.get_block(i).check():
				return False
		return True

	def get_block_by_row_and_col(self, row, col):
		el = self.blocks[0].edge_len
		blocks_row = row/el
		blocks_col = col/el
		block_row = row%el
		block_col = col%el
		block = blocks_row*el+blocks_col
		return (block, block_row, block_col)

	def get_rows_and_cols_by_block(self, block_numb):
		el = self.blocks[0].edge_len
		rows = range(block_numb/el*el, block_numb/el*el+el)
		cols = range(block_numb%el*el, block_numb%el*el+el)
		return rows, cols

	def get_value_by_row_and_col(self, row, col):
		block_idx, block_row, block_col = self.get_block_by_row_and_col(row, col)
		return self.blocks[block_idx].get_field(block_row*3+block_col)

	def get_numb_of_empty_fields(self):
		n = 0
		for i in range(9):
			n += len(self.blocks[i].get_list_of_empty_fields())
		return n

class Solver(object):
	def __init__(self, gamefield_or_solver):
		if isinstance(gamefield_or_solver, Gamefield):
			self.gf = gamefield_or_solver
		elif isinstance(gamefield_or_solver, Solver):
			self.gf = gamefield_or_solver.gf
		else:
			raise

	def draw(self):
		self.gf.draw()

	def run(self):
		pass


class Solver1(Solver):
	def run(self):
		while True:
			ret = False
			for v in range(1,10):
			#for v in [5]:
				if self.foo(v):
					ret = True
			if not self.gf.check():
				print "Error occurred"
				return
			if DEBUG:
				print '#'
			if not ret:
				break
		return

	def foo(self, n):
		ret = False
		block_idx_list = range(9)
		while len(block_idx_list) > 0:
			block_idx = block_idx_list.pop(0)
			b = self.gf.get_block(block_idx)
			locked_rows = []
			locked_cols = []
			if not b.has_value(n):
				rows, cols = self.gf.get_rows_and_cols_by_block(block_idx)

				# Check if n is in line. If .. lock line.
				for row in rows:
					if self.gf.row_has_value(row, n):
						locked_rows.append(row)
				for col in cols:
					if self.gf.col_has_value(col, n):
						locked_cols.append(col)
				#print "locked (do not use for fill):", locked_rows, locked_cols

				if DEBUG:
					if block_idx == 3 and n == 4:
						#print "possible rows and cols:", pos_rows, pos_cols
						print "locked rows and cols:", locked_rows, locked_cols

				# search lines, which are not already locked
				pos_rows = rows[:]
				for row in locked_rows:
					pos_rows.remove(row)
				#print "possible rows:", pos_rows
				pos_cols = cols[:]
				for col in locked_cols:
					pos_cols.remove(col)
				#print "possible cols:", pos_cols

				if DEBUG:
					if block_idx == 3 and n == 4:
						print "possible rows and cols:", pos_rows, pos_cols

				# filter lines by searching for empty fields
				for pos_row in pos_rows[:]:
					if len(b.get_list_of_empty_fields_in_row(pos_row%3)) == 0:
						pos_rows.remove(pos_row)
				for pos_col in pos_cols[:]:
					if len(b.get_list_of_empty_fields_in_col(pos_col%3)) == 0:
						pos_cols.remove(pos_col)

				if DEBUG:
					if block_idx == 3 and n == 4:
						print "possible rows and cols:", pos_rows, pos_cols
						print "empty fields:", b.get_list_of_empty_fields()
						print "locked rows and cols:", locked_rows, locked_cols

				# fill, if two parallel lines are blocked and only one field is empty
				if len(pos_rows) == 1:
					empty_fields_in_row = b.get_list_of_empty_fields_in_row(pos_rows[0]%3)
					if len(empty_fields_in_row) == 1:
						self.gf.set_field_by_blockidx_and_blockfield(n, block_idx, empty_fields_in_row[0])
						ret = True
						block_idx_list.append(block_idx)
						if DEBUG:
							print "break at 1"
						continue
				if len(pos_cols) == 1:
					empty_fields_in_col = b.get_list_of_empty_fields_in_col(pos_cols[0]%3)
					if len(empty_fields_in_col) == 1:
						self.gf.set_field_by_blockidx_and_blockfield(n, block_idx, empty_fields_in_col[0])
						ret = True
						block_idx_list.append(block_idx)
						if DEBUG:
							print "break at 2"
						continue

				pos_list = []
				for r in pos_rows:
					for c in pos_cols:
						if not self.gf.has_value(r, c):
							pos_list.append( (r, c) )

				#print pos_rows, pos_cols
				if len(pos_list) == 1:
					r = pos_list[0][0]
					c = pos_list[0][1]
					self.gf.set_field_by_row_and_col(n, r, c)
					ret = True
					block_idx_list.append(block_idx)
					if DEBUG:
						print "break at 3"
					continue
		return ret


def main(game):
	gf = Gamefield(game)
	#for i in range(9):
	#	print gf.check_col(i)
	#	print gf.check_row(i)
	s = Solver1(gf)
	s.draw()
	s.run()
	print "-"*40
	s.draw()
	if DEBUG:
		print "number of empty fields:", s.gf.get_numb_of_empty_fields()


def test(game):
	gf = Gamefield(game)

	if not gf.check():
		print "Error"
		raise


if __name__ == '__main__':
	game1 = [[None, None, 5, 4, None, 3, None, None, 8], [None, None, None, 9, None, None, 1, None, 5], [None, None, 1, 2, 5, None, None, None, None],
			[3, None, None, 2, None, 6, 1, None, None], [None, 1, 8, None, 3, None, 6, 4, None], [None, None, 5, 1, None, 7, None, None, 9],
			[None, None, None, None, 9, 2, 6, None, None], [8, None, 1, None, None, 3, None, None, None], [3, None, None, 7, None, 6, 5, None, None]]

	test(game1)
	main(game1)

	print '='*60
	DEBUG = True
	game2 = [[None, 1, None, 2, None, None, 8, None, None],
			 [4, 8, None, 3, 5, None, None, None, None],
			 [None, None, None, None, 4, None, 5, 1, None],
			 [None, None, 9, None, 6, None, None, None, None],
			 [6, None, 5, None, 7, None, 9, None, 8],
			 [None, None, None, None, 5, None, 3, None, None],
			 [None, 2, 6, None, 7, None, None, None, None],
			 [None, None, None, None, 6, 9, None, 1, 2],
			 [None, None, 9, None, None, 5, None, 3, None]]

	test(game2)
	main(game2)
