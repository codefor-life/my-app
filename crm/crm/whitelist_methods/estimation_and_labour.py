
import frappe
import uuid




@frappe.whitelist()
def get_labour_and_material(doc):
    id = frappe.parse_json(doc)


    labour_and_material = frappe.get_doc("Labour And Material",id)

    return frappe.parse_json(labour_and_material)


@frappe.whitelist()
def create_labour_and_material(doc):
    data = frappe.parse_json(doc)


    labourDoc = frappe.new_doc(data.get("doctype")) #Labour And Material
    # labourDoc.estimation_id = data.get("estimation_id")
    labourDoc.idx= data.get("idx")
    labourDoc.category= data.get("category")                  
    labourDoc.type= data.get("type")
    # labourDoc.item= data.get("item")
    # labourDoc.item_code= generate_username()
    # labourDoc.est =  data.get("estimation_id") 
    # labourDoc.table_labour.append(data.get("items"))
    # arr = []
    # arr = data.get("items")


    

    for item in data.get("items", []):
        amt = 0
        if(item.get("quantity") and item.get("cost")):
            amt = item.get("quantity") * item.get("cost")

        labourDoc.append("table_labour", {
            "type": item.get("type"),
            "item": item.get("item"),
            "quantity": item.get("quantity"),
            "cost": item.get("cost"),
            "amount":amt,
        })
        
    

    labourDoc.insert()
    frappe.db.commit()
    
    return frappe.parse_json(labourDoc)



#just for testing purpose
def generate_username():
    # Generate a UUID
    unique_id = uuid.uuid4()

    # Format the UUID as a username (e.g., remove dashes and truncate)
    username = str(unique_id).replace('-', '')[:10]  # Adjust length as needed

    return username





@frappe.whitelist()
def update_child_table_row(doc):
    data = frappe.parse_json(doc)

    # Load the parent document
    estimation = frappe.get_doc('Estimation', data.get('estimation_id'))
    
    # Find and update the specific row in the child table
    for row in estimation.table_hpqs:
        if row.idx == data.get('row_idx'):
            row.labour_and_materials = data.get('labour_and_materials_id')
            break
    
    # Save the parent document
    estimation.save()
    frappe.db.commit()



@frappe.whitelist()
def update_labour_and_material(doc):
    data = frappe.parse_json(doc)


    labourDoc = frappe.get_doc("Labour And Material",data.get("id"))
    labourDoc.table_labour = []


    labourDoc.idx= data.get("idx")
    labourDoc.category= data.get("category")                  
    labourDoc.type= data.get("type")
    labourDoc.item= data.get("item")
    # labourDoc.item_code= generate_username()
    labourDoc.est =  data.get("estimation_id") 

    

    for item in data.get("items", []):
        amt = 0
        if(item.get("quantity") and item.get("cost")):
            amt = item.get("quantity") * item.get("cost")

        labourDoc.append("table_labour", {
            "type": item.get("type"),
            "item": item.get("item"),
            "quantity": item.get("quantity"),
            "cost": item.get("cost"),
            "amount": amt
        })
    labourDoc.save()
    frappe.db.commit()

    return "updated successfully"





@frappe.whitelist()
def update_below_table(doc,est_id):
    
    # Parse the JSON data to get Labour And Material IDs
    labour_and_material_ids = frappe.parse_json(doc)

    # Initialize a list to hold new child table entries for Estimation
    new_estimation_charges = []
    estimation_doc = frappe.get_doc("Estimation", est_id)
    estimation_doc.est_og_charges = []



    for i in range(0,len(labour_and_material_ids)):
        # Fetch Labour And Material document
        labour_and_material = frappe.get_doc("Labour And Material", labour_and_material_ids[i])

        all_types_of_amount = {}
        for hpq in labour_and_material.get("table_labour"):
            # Create a new dictionary for Estimation child table entry
            new_charge = {
                "type": hpq.type,
                "item": hpq.item,
                "quantity": hpq.quantity,
                "category": labour_and_material.category,
                "boq_item": labour_and_material.type,
                "amount": hpq.get("amount"),
                "linking_idx": labour_and_material.idx,
                "labour_and_materials": labour_and_material.name
            }

            new_estimation_charges.append(new_charge)


            item_type = hpq.get("type")
            type_amount = hpq.get("amount")

            if(item_type in all_types_of_amount):
                 all_types_of_amount[item_type] += type_amount
            else:
                 all_types_of_amount[item_type] = type_amount

        


        idx=0
        for row in estimation_doc.table_hpqs:
            if row.labour_and_materials == labour_and_material_ids[i]:
                break

            idx+=1

        if(idx >=0):
            for type in all_types_of_amount:
                if(type == "Raw Material"):
                        estimation_doc.table_hpqs[idx].raw_cost = all_types_of_amount[type]
                elif(type == "Labour"):
                        estimation_doc.table_hpqs[idx].labour_cost = all_types_of_amount[type]
                elif(type == "Finished Material"):
                        estimation_doc.table_hpqs[idx].finished_cost = all_types_of_amount[type]

       

    for item in new_estimation_charges:
            estimation_doc.append("est_og_charges", {
                "type": item.get("type"),
                "item": item.get("item"),
                "quantity": item.get("quantity"),
                "category": item.get("category"),
                "boq_item": item.get("boq_item"),
                "amount": item.get("amount"),
                "linking_idx":item.get("linking_idx"),
                "labour_and_materials": item.get("labour_and_materials")
            })

    
    estimation_doc.save()
    frappe.db.commit()
    update_total_labour_and_material_cost(est_id)
    calculate_cost_for_each_table_row(est_id)

    # Return success message or any data if needed
    return "Child table entries updated successfully"




@frappe.whitelist()
def append_to_below_table(labourDoc,est_id):
    
    # Parse the JSON data to get Labour And Material IDs
    labourDoc = frappe.parse_json(labourDoc)

    # Initialize a list to hold new child table entries for Estimation
    new_estimation_charges = []
    estimation_doc = frappe.get_doc("Estimation", est_id)

    all_types_of_amount = {}
    
    # Iterate over child table 'table_hpqs' in Labour And Material document
    for hpq in labourDoc.get("table_labour"):
            # Create a new dictionary for Estimation child table entry
            new_charge = {
                "type": hpq.get("type"),
                "item": hpq.get("item"),
                "quantity": hpq.get("quantity"),
                "amount": hpq.get("amount")
            }
            new_estimation_charges.append(new_charge)


            item_type = hpq.get("type")
            type_amount = hpq.get("amount")

            if(item_type in all_types_of_amount):
                 all_types_of_amount[item_type] += type_amount
            else:
                 all_types_of_amount[item_type] = type_amount

        

    for item in new_estimation_charges:
            estimation_doc.append("est_og_charges", {
                "type": item.get("type"),
                "item": item.get("item"),
                "quantity": item.get("quantity"),
                "category": labourDoc.category,
                "boq_item": labourDoc.type,
                "amount": item.get("amount"),
                "linking_idx": labourDoc.idx,
                "labour_and_materials": labourDoc.name
            })


    idx=0
    for row in estimation_doc.table_hpqs:
            if row.labour_and_materials == labourDoc.name:
                break

            idx+=1

    for type in all_types_of_amount:
            if(type == "Raw Material"):
                    estimation_doc.table_hpqs[idx].raw_cost = all_types_of_amount[type]
            elif(type == "Labour"):
                    estimation_doc.table_hpqs[idx].labour_cost = all_types_of_amount[type]
            elif(type == "Finished Material"):
                    estimation_doc.table_hpqs[idx].finished_cost = all_types_of_amount[type]


    estimation_doc.save()
    frappe.db.commit()
    update_total_labour_and_material_cost(est_id)
    calculate_cost_for_each_table_row(est_id)


    # Return success message or any data if needed
    return "Child table entries updated successfully"



@frappe.whitelist()
def delete_labour_and_material(labour_id,est_id):

    estimation_doc = frappe.get_doc("Estimation", est_id)

    
    labour_and_material_ids = []
    remove_this_row= []
   
    estimation_doc.table_hpqs = [row for row in estimation_doc.table_hpqs if row.labour_and_materials != labour_id]

    labourDoc = frappe.get_doc("Labour And Material", labour_id)
    print("updating below table")
    print(estimation_doc.table_hpqs)

 
    rows_to_remove = [row for row in estimation_doc.est_og_charges if row.labour_and_materials == labour_id]
    print("rows to remove",rows_to_remove)
    for row in rows_to_remove:
            estimation_doc.est_og_charges.remove(row)

    
    estimation_doc.save()
    frappe.delete_doc("Labour And Material",labour_id)                   

    return "Deleted Successfully"
    

    

@frappe.whitelist()
def update_total_labour_and_material_cost(est_id):
    estimation_doc = frappe.get_doc("Estimation",est_id)

    total_labour_cost = 0
    total_row_cost = 0
    for row in estimation_doc.table_hpqs:
        total_row_cost += row.raw_cost
        total_labour_cost += row.labour_cost

    estimation_doc.total_material_cost = total_row_cost
    estimation_doc.total_labour_cost = total_labour_cost

    estimation_doc.save()
    frappe.db.commit()


@frappe.whitelist()
def calculate_cost_for_each_table_row(est_id):
    estimation_doc = frappe.get_doc("Estimation",est_id)
    

    i=0
    for row in estimation_doc.table_hpqs:
        estimation_doc.table_hpqs[i].fixed_amount = row.raw_cost + row.labour_cost
        estimation_doc.table_hpqs[i].overhead_amount = (estimation_doc.table_hpqs[i].fixed_amount * estimation_doc.overhead_percentage) / 100
        estimation_doc.table_hpqs[i].profit_amount = ((estimation_doc.table_hpqs[i].fixed_amount + estimation_doc.table_hpqs[i].overhead_amount) * estimation_doc.profit_and_margin) / 100
        estimation_doc.table_hpqs[i].selling_sum = estimation_doc.table_hpqs[i].fixed_amount + estimation_doc.table_hpqs[i].overhead_amount + estimation_doc.table_hpqs[i].profit_amount
        estimation_doc.table_hpqs[i].rateno = estimation_doc.table_hpqs[i].fixed_amount + estimation_doc.table_hpqs[i].overhead_amount + estimation_doc.table_hpqs[i].profit_amount

        if estimation_doc.table_hpqs[i].area > 0:
            estimation_doc.table_hpqs[i].ratem2 = (estimation_doc.table_hpqs[i].fixed_amount + estimation_doc.table_hpqs[i].overhead_amount + estimation_doc.table_hpqs[i].profit_amount) / estimation_doc.table_hpqs[i].area
        else:
            estimation_doc.table_hpqs[i].ratem2 = 0            

        i+=1

    estimation_doc.save()
    frappe.db.commit()

    return "calculation done"

