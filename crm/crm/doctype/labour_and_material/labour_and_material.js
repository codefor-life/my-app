// Copyright (c) 2024,   and contributors
// For license information, please see license.txt

frappe.ui.form.on("Labour And Material", {  
        refresh: function(frm) {
                frm.fields_dict['table_labour'].grid.get_field('item').get_query = function(doc, cdt, cdn) {
                    let row = locals[cdt][cdn];
                    return {
                        filters: {
                            'item_type': row.type
                        }
                    };
                };
            },
            table_labour: function(frm, cdt, cdn) {
                var grid_row = frm.open_grid_row();
                grid_row.on('field_change', function(fieldname, value) {
                    if(fieldname == 'item_type') {
                        grid_row.fields_dict['item'].get_query = function() {
                            return {
                                filters: {
                                    'item_type': value
                                }
                            };
                        };
                        grid_row.refresh_field('item');
                    }
                });
        },        
	after_save(frm) {
        // console.log("sdjkfsa fjsjkdfalkj sfdlkfjaskl")
        // console.log(frm.doc.estimation_id)
        // console.log(frm.doc.estimation_id)
        // console.log(frm.doc.estimation_id)
        // console.log(frm.doc.estimation_id)
        // console.log(frm.doc.estimation_id)
        // console.log(frm.doc.estimation_id)

        // window.location.href = `/app/estimation/${frm.doc.estimation_id}`
	},
});


frappe.ui.form.on("Labour And M Table",{
        refresh: function(frm) {
                frm.set_query('item', function() {
                    return {
                        filters: {
                            'type': frm.doc.type
                        }
                    };
                });
        }
});
