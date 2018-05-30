frappe.listview_settings['Issue'] = {
	onload: function(listview) {
		var method = "kisanmitra_erpnext.dochooks.export_collector_report"
		listview.page.add_menu_item(__("Export Collector Report"), function() {
			console.log("in issue list method");
			frappe.call({
				method:"kisanmitra_erpnext.api.get_km_data"
			}).done((r)=>{
				console.log("in done ");
			}).fail((r)=>{
				console.log(r);
			});
			// listview.call_for_selected_items(method, {});
			// var w = window.open("kisanmitra_erpnext/report/collector_review_report/get_data");
			// if(!w) {
			// 	frappe.msgprint(__("Please enable pop-ups")); return;
			// }
		});
	}
}
