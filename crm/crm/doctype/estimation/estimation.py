# Copyright (c) 2024,   and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from crm.crm.whitelist_methods.estimation_and_labour import calculate_cost_for_each_table_row
from crm.crm.whitelist_methods.estimation_and_labour import update_total_labour_and_material_cost


class Estimation(Document):

	@frappe.whitelist()
	def redirect_to_labour_and_material(estimation_doc):
		estimation = frappe.get_doc(estimation_doc)
		estimation.save()

		# Create a new Labour and Material document
		labour_and_material = frappe.new_doc('Labour And Material')
		labour_and_material.estimation = estimation.name
		labour_and_material.insert()
		labour_and_material.save()

		# Return the name of the new Labour and Material document
		return {'labour_and_material_name': labour_and_material.name}

	# Redirect back to the Estimation document after saving Labour and Material
	@frappe.whitelist()
	def save_labour_and_material(labour_and_material_doc):
		labour_and_material = frappe.get_doc(labour_and_material_doc)
		labour_and_material.save()

		# Return the name of the associated Estimation document
		return {'estimation_name': labour_and_material.estimation}

	def validate(doc):
		for i in range(0,len(doc.table_hpqs)):
			row = doc.table_hpqs[i]
			if(doc.table_hpqs[i].width_meter and doc.table_hpqs[i].width_meter > 0 and doc.table_hpqs[i].height_meter and doc.table_hpqs[i].height_meter > 0 and doc.table_hpqs[i].quantity and doc.table_hpqs[i].quantity>0):
				doc.table_hpqs[i].area = doc.table_hpqs[i].width_meter * doc.table_hpqs[i].height_meter * doc.table_hpqs[i].quantity
				doc.table_hpqs[i].perimeter = 2 * (doc.table_hpqs[i].width_meter + doc.table_hpqs[i].height_meter) *  doc.table_hpqs[i].quantity

			         

		
		

	



