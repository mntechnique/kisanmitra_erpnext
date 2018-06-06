import frappe
#patch to update caller name field
def execute():
	frappe.reload_doc("support","doctype","issue")
	name = None
	caller_name = None

	issues = frappe.get_all("Issue",filters={"km_caller_name":""},fields=["*"])
	try:
		for issue in issues:
			if issue.get("contact"):
				name = frappe.db.get_value("Contact",issue.get("contact"),["first_name","last_name"])
				if name:
					caller_name = " ".join([name[0] or "",name[1] or ""]).strip()
					frappe.db.sql("""update `tabIssue` 
						set km_caller_name=%s where name=%s""",(caller_name,issue.get("name")))
			
			elif issue.get("raised_by_phone"):
				name = frappe.db.get_value("Contact",{"mobile_no":issue.get("raised_by_phone")},["first_name","last_name"])
				if name:
					caller_name =" ".join([name[0] or "",name[1] or ""]).strip()
					frappe.db.sql("""update `tabIssue` 
						set km_caller_name=%s where name=%s""",(caller_name,issue.get("name")))
			
			elif issue.get("lead"):
				name = frappe.db.get_value("Lead",issue.get("lead"),["first_name","last_name"])
				if name:
					caller_name =" ".join([name[0] or "",name[1] or ""]).strip()
					frappe.db.sql("""update `tabIssue`
						set km_caller_name=%s where name=%s""",(caller_name,issue.get("name")))

	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=frappe.get_traceback(), title="error in update caller name")			