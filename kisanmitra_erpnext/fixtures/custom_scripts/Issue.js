frappe.ui.form.on("Issue", {
	refresh: function(frm) {
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
	}
});