'''
if not pagination.has_prev
page=pagination.prev_num
for p in pagination.iter_pages()
if p == pagination.page
if not pagination.has_next
'''

class Pagination:
	def __init__(self, all):
		self.all = all
	def paginate(self, page, per_page):
		self.page = page
		self.per_page = per_page
		self.has_prev = False if page <= 1 else True
		self.prev_num = page - 1
		self.has_next = False if (page+1)*per_page > len(self.all) else True
		if self.has_next:
			self.items = self.all[page*per_page: (page+1)*per_page]
		else:
			self.items = self.all[page*per_page:]
		self.page_num = int(len(self.all)/per_page) + (1 if self.has_next else 0)
	def iter_pages(self):
		if not self.page_num:
			return []
		items = [0] * self.page_num
		items[0] = 1
		items[-1] = self.page_num
		if self.has_next:
			items[self.page] = self.page+1
		if self.has_prev:
			items[self.page] = self.page-1

		return items
