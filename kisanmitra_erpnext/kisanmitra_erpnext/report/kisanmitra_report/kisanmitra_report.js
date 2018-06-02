// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Kisanmitra Report"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options":"\nOpen\nReplied\nHold\nClosed\nNew\nWait for caller/farmer\nMandal Committee\nKisan Mitra\nDistrict Committee\nCollector Review\nWait for 3rd party\nAssigned\nResolved\nDeferred\nCollector Action Awaited\nPending to be Resolved\nKisanMitra Field Coordinator\nRDO\nField Visit Done\nInsurance Company\nPlanned\nPending after LRU",
			"default": "Open"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"state",
			"label": __("State"),
			"fieldtype": "Link",
			"options":"Territory",
			"get_query": function() {
				return {
					"filters": {
						"parent_territory": "India"	
					}
				}
			}
		},
		{
			"fieldname":"district",
			"label": __("District"),
			"fieldtype": "Link",
			"options":"Territory",
			"get_query": function() {
				var state = frappe.query_report_filters_by_name.state.get_value();
				return {
					"filters": {
						"parent_territory": state
					}
				}
			}
		},
		{
			"fieldname":"mandal",
			"label": __("Mandal"),
			"fieldtype": "Link",
			"options":"Territory",
			"get_query": function() {
				var district = frappe.query_report_filters_by_name.district.get_value();
				return {
					"filters": {
						"parent_territory": district	
					}
				}
			}
		},
		{
			"fieldname":"village",
			"label": __("Village"),
			"fieldtype": "Link",
			"options":"Territory",
			"get_query": function() {
				var mandal = frappe.query_report_filters_by_name.mandal.get_value();
				return {
					"filters": {
						"parent_territory": mandal	
					}
				}
			}
		}

	]
}
