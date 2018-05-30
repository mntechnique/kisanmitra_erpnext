import frappe

@frappe.whitelist()
def export_collector_report(args):
	print(args)