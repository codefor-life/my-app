# Copyright (c) 2024,   and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BOQ(Document):
	def validate(self):
		print(self.raw_material_list[0].item)
		print(self.raw_material_list[0].standard_buying_price)
		print(self.raw_material_list[0].quantity)
		print(self.raw_material_list[0].price)

		for i in range(0,len(self.raw_material_list)):
			self.raw_material_list[i].price = self.raw_material_list[i].standard_buying_price * self.raw_material_list[i].quantity 

	


