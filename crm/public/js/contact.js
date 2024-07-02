frappe.ui.form.on('Contact', {
    refresh: function(frm) {
        // Add custom button
        frm.add_custom_button(__('Create Enquiry'), function() {
            // // Redirect to Enquiry form
            // frappe.route_options = {
            //     'contact_id': frm.doc.name  // Pass the project name to the Enquiry form
            // };
            frappe.new_doc('Enquiry Form',{
                'contact_id': frm.doc.name  
            });  // Replace 'Enquiry' with your DocType name
        });
    }
});