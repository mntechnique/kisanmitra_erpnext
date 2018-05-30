import frappe,os
from datetime import datetime

def execute():
	## Communication
	# call receiver, exophone, phone_no
	try:
		communications = frappe.get_all("Communication", filters={"status":"Info"})

		for communication in communications:
			frappe.db.sql("""update `tabComunication`
				set call_receiver=%s,exophone=%s,phone_no=%s where name=%s""",\
				(communication.get("call_receiver")[1:11],communication.get("exophone")[1:11],communication.get("phone_no")[1:11], communication.get("name")))
			frappe.db.commit()
	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(), title="Error in communication patch")

	## Contact 
	# mobile_no
	try:
		contacts = frappe.get_all("Contact", filters={})

		for contact in contacts:
			frappe.db.sql("""update `tabContact`
				set mobile_no=%s where name=%s""",(contact.get("mobile_no")[1:11], contact.get("name")))
			frappe.db.commit()
	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(), title="Error in contact patch")

	## Issue
	# raised_by_phone
	try:
		issues = frappe.get_all("Issue", filters={})
		
		for issue in issues:
			if(issue.raised_by_phone):
				frappe.db.sql("""update `tabIssue`
					set raised_by_phone=%s where name=%s""",(issue.get("raised_by_phone")[1:11], issue.get("name")))
				frappe.db.commit()
	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(), title="Error in issue patch")