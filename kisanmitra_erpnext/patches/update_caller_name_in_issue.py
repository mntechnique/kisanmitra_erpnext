import frappe

def execute():
	frappe.reload_doc("support","doctype","issue")

	issues = frappe.get_all("Issue",filters={"km_caller_name":""},fields=["*"])
	print "in update caller name patch"
	count = 1
	try:
		for issue in issues:
			if issue.get("contact"):
				frappe.db.sql("""update `tabIssue` 
					set km_caller_name=(select trim(concat(first_name," ",last_name))
					from `tabContact` where name=%s) where name=%s""",(issue.get("contact"),issue.get("name")))
				print "updated by contact field ",count
				count += 1
			
			elif issue.get("raised_by_phone"):
				frappe.db.sql("""update `tabIssue` 
					set km_caller_name=(select trim(concat(first_name," ",last_name))
					from `tabContact` where mobile_no=%s) where name=%s""",(issue.get("raised_by_phone"),issue.get("name")))
				print "updated by raised_by_phone field ",count
				count += 1
			
			elif issue.get("lead"):
				frappe.db.sql("""update `tabIssue` 
					set km_caller_name=(select trim(lead_name)
					from `tabLead` where name=%s) where name=%s""",(issue.get("lead"),issue.get("name")))
				print "updated by lead field ",count
				count += 1
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=frappe.get_traceback(), title="error in update caller name")			