// Copyright (c) 2024,   and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Estimation", {
// 	refresh(frm) {

// 	},
// });


// frappe.ui.form.on('Estimation', {
//     labour_and_material: function(frm){
//         console.log("sdkfj hsja fsdljfk lsdfjlksdjflksa ")
//     },
//     refresh: function(frm){
//         console.log(frm)
//         // console.log("sdjkfsa dlfkjsaf jkasfdh kajs")
//         // console.log(frm.grids[0].grid)
//     }
// });


// frappe.ui.form.on('Item Estimation Table', {
//     labour_and_materials:async function(frm,cdt, cdn){

//         await frm.save()
//         // await frappe.new_doc("Labour And Material",{
//         //     'estimation_id': frm.doc.name,
//         // })
//     }
// });


var gridBody=null;

// setTimeout(()=>{
//     let addBtn = document.querySelector(".grid-add-row");

//     addBtn.addEventListener("click",(e)=>{
//         gridBody = document.getElementsByClassName("data-row");

//         console.log(gridBody)
//         updateRowList();
//     })
    
// },100)


function updateRowList(){
    for(let i=0;i<gridBody.length;i++){
        console.log("sdjhfkjs hdflkjsas")
        gridBody[i].addEventListener("click",(e)=>{
            console.log(e.currentTarget)
            let el = e.currentTarget;
        })
    }
}

frappe.ui.form.on('Estimation', {
    refresh: function(frm) {
        // Ensure the custom script is added only once to avoid multiple event bindings
        if (!frm.custom_new_doc_listener_added) {
            frm.custom_new_doc_listener_added = true;

            // Override the default behavior for the link field's "Add New" option
            frm.fields_dict['labour_and_materials'].get_new_doc = function() {
                // Save the current Estimation document before creating a new linked document
                frm.save_or_update().then(function() {
                    // Get the name of the current Estimation document
                    let estimation_doc_name = frm.doc.name;

                    // Create a new Labour And Material document
                    frappe.model.with_doctype('Labour And Material', function() {
                        let labour_and_material = frappe.model.get_new_doc('Labour And Material');

                        // Redirect to the new Labour And Material document
                        frappe.set_route('Form', 'Labour And Material', labour_and_material.name).then(function() {
                            // Add a hook to handle the after-save event of Labour And Material
                            frappe.ui.form.on('Labour And Material', {
                                after_save: function(frm) {
                                    // Redirect back to the original Estimation document
                                    frappe.set_route('Form', 'Estimation', estimation_doc_name).then(function() {
                                        // Update the child table with the newly created Labour And Material document
                                        var row = frm.add_child('table_hpqs');
                                        row.labour_and_materials = frm.doc.name;
                                        frm.refresh_field('table_hpqs');
                                    });
                                }
                            });
                        });
                    });
                });
            };
        }
    }
});
