// // Copyright (c) 2024,   and contributors
// // For license information, please see license.txt

// // frappe.ui.form.on("Labour And Material", {  
// //         refresh: function(frm) {
// //                 frm.fields_dict['table_labour'].grid.get_field('item').get_query = function(doc, cdt, cdn) {
// //                     let row = locals[cdt][cdn];
// //                     return {
// //                         filters: {
// //                             'item_type': row.type
// //                         }
// //                     };
// //                 };
// //             },
// //             table_labour: function(frm, cdt, cdn) {
// //                 var grid_row = frm.open_grid_row();
// //                 grid_row.on('field_change', function(fieldname, value) {
// //                     if(fieldname == 'item_type') {
// //                         grid_row.fields_dict['item'].get_query = function() {
// //                             return {
// //                                 filters: {
// //                                     'item_type': value
// //                                 }
// //                             };
// //                         };
// //                         grid_row.refresh_field('item');
// //                     }
// //                 });
// //         },        
// // 	// after_save(frm) {
//         // console.log("sdjkfsa fjsjkdfalkj sfdlkfjaskl")
//         // console.log(frm.doc.estimation_id)
//         // console.log(frm.doc.estimation_id)
//         // console.log(frm.doc.estimation_id)
//         // console.log(frm.doc.estimation_id)
//         // console.log(frm.doc.estimation_id)
//         // console.log(frm.doc.estimation_id)

//         // window.location.href = `/app/estimation/${frm.doc.estimation_id}`
// 	// },
//     // after_save: function(frm) {
//     //     // Redirect back to the original Estimation document
//     //     // frappe.set_route('Form', 'Estimation', frm.doc.estimate).then(function() {
//     //     //     // Update the child table with the newly created Labour And Material document
//     //     //     var row = frm.add_child('table_hpqs');
//     //     //     row.labour_and_materials = frm.doc.name;
//     //     //     frm.refresh_field('table_hpqs');
//     //     // });
//     // },
//     onload: function(frm) {
//         // var urlParams = new URLSearchParams(window.location.search);
//         // var row_data = urlParams.get('row_data');
//         // console.log(window.location.search)
//         // var estimation_id = urlParams.get('estimation_id');
//         // var row_idx = urlParams.get('idx');

//         // console.log(urlParams, row_data, estimation_id, row_idx)

//         // if (estimation_id && row_data) {
//             // frm.set_value('estimation_id', estimation_id);
//             // frm.set_value('idx', row_idx);

//             // Parse row_data and populate the fields
//             // var row = JSON.parse(decodeURIComponent(row_data));
//             // console.log("row",row)
//             // frm.set_value('some_field', row.some_field);
//             // frm.set_value('another_field', row.another_field);
//             // Populate other necessary fields
//         // }
//     },

//     after_save: function(frm) {
//         // Redirect back to Estimation doctype with Labour and Material ID
//         var labour_and_material_id = frm.doc.name;
//         var estimation_id = frm.doc.estimation_id;
//         var row_idx = frm.doc.idx;

//         let data = {
//             'estimation_id': estimation_id,
//             'row_idx': row_idx,
//             'labour_and_materials_id':labour_and_material_id,
//               // Replace with the actual value you want to pass
//             // Add other fields as needed
//         };
//         frappe.call({
//             method: 'crm.crm.whitelist_methods.estimation_and_labour.update_child_table_row',
//             args: {
//                 'doc': JSON.stringify(data)
//             },
//             callback: function(response) {
//                 if (!response.exc) {
//                     console.log(response)
//                     // frappe.msgprint('Labour And Material created successfully!');
//                     window.location.href = `/app/estimation/${estimation_id}?labour_and_material_id=${labour_and_material_id}&row_idx=${row_idx}`;
//                     // Optionally, you can handle further actions after creation
//                 } else {
//                     frappe.msgprint('Failed to done process: ' + response.exc);
//                 }
//             }
//         });


       
//     }
// });


// frappe.ui.form.on("Labour And M Table",{
//         refresh: function(frm) {
//                 frm.set_query('item', function() {
//                     return {
//                         filters: {
//                             'type': frm.doc.type
//                         }
//                     };
//                 });
//         }
// });



// // frappe.ui.form.on('Labour And Material', {
    
// // });
