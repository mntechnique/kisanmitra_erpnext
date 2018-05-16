import frappe

def execute():
	frappe.reload_doc("support", "doctype", "issue")

	issues = frappe.get_all("Issue", fields=["name", "km_caller_name"], filters = {"contact":"","lead":""})

	for issue in issues:
		lead = ''
		contact = ''
		raised_by_phone = ''
		caller_name = issue.km_caller_name
		if caller_name:
			caller_name = (caller_name.split("."))[0].strip()+" 0"
			lead = (frappe.get_all("Lead", filters={"company_name":caller_name}))[0].get("name")
			contact = frappe.db.get_value("Dynamic Link",{"link_name":lead},"parent")
			raised_by_phone = frappe.db.get_value("Contact",contact,"mobile_no")
			if lead and contact and raised_by_phone:
				frappe.db.sql("""update `tabIssue`
						set lead=%s, contact=%s,
						raised_by_phone=%s where name=%s""",(lead,contact,raised_by_phone,issue.get("name")))

	frappe.db.sql("""update `tabIssue`
					set raised_by_phone='' where contact=''""")