frappe.ui.form.on("Issue", {
	refresh: function(frm) {
		if (!frm.doc.km_state_case) {
			frm.set_value("km_state_case", "Telangana");
		}

		frm.set_query("km_state_case", function() {
			return {
				filters: {
					"parent_territory": "India"
				}
			}
		});
		frm.set_query("km_district_case", function() {
			return {
				filters: {
					"parent_territory": frm.doc.km_state_case
				}
			}
		});
		frm.set_query("km_mandal_case", function() {
			return {
				filters: {
					"parent_territory": frm.doc.km_district_case
				}
			}
		});
		frm.set_query("km_village_case", function() {
			return {
				filters: {
					"parent_territory": frm.doc.km_mandal_case
				}
			}
		});

		frm.add_custom_button(__("Send SMS"), function() {
			var dialog = new frappe.ui.Dialog({
				title: 'Send SMS',
				fields: [
					{'fieldname': "message_template", 'fieldtype': 'Link', 'options': "KM SMS Template", 'label':'Template'},
					{'fieldname': "message_text", 'fieldtype': 'Text', 'options': "", 'label':'Message'},
					{'fieldname': "recipients", 'fieldtype': 'Data', 'options': "", 'label':'Recipients'}
				],
			});
			dialog.set_value("recipients", cur_frm.doc.raised_by_phone);
			
			dialog.get_input("message_template").on("blur", function(e) {
				console.log("blur", );
				frappe.model.with_doc("KM SMS Template", dialog.get_value("message_template"), () => {

				});
			});
			
			dialog.set_primary_action(__("Send"), () => {
				var values = dialog.get_values();
				frm.call("frappe.core.doctype.sms_settings.sms_settings.send_sms", {
					receiver_list: values.get("recipients"),
					msg: values.get("message_text")
				}, () => {
					dialog.hide();
				});
			});
			dialog.show();
    	});
	}
});