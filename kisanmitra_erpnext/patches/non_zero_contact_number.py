import frappe,os
from datetime import datetime

def execute():
	## Communication
	# call receiver, exophone, phone_no
	try:
		communications = frappe.get_all("Communication", fields=["*"], filters={"comment_type":"Info"})

		for communication in communications:
			if(communication.get("call_receiver") and len(communication.get("call_receiver"))==11):
				frappe.db.sql("""update `tabCommunication`
				set call_receiver=%s where name=%s""",\
				(communication.get("call_receiver")[1:11], communication.get("name")))
				frappe.db.commit()

			if(communication.get("exophone") and len(communication.get("exophone"))==11):
				frappe.db.sql("""update `tabCommunication`
					set exophone=%s where name=%s""",\
					(communication.get("exophone")[1:11], communication.get("name")))
				frappe.db.commit()

			if(communication.get("phone_no") and len(communication.get("phone_no"))==11):
				frappe.db.sql("""update `tabCommunication`
				set phone_no=%s where name=%s""",\
				(communication.get("phone_no")[1:11], communication.get("name")))
				frappe.db.commit()
	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(), title="Error in communication patch")

	## Contact 
	# mobile_no
	try:
		contacts = frappe.get_all("Contact", fields=["*"], filters=[], order_by="creation desc")

		for contact in contacts:
			if(len(contact.get("mobile_no"))==11):
				frappe.db.sql("""update `tabContact`
				set mobile_no=%s where name=%s""",(contact.get("mobile_no")[1:11], contact.get("name")))
				frappe.db.commit()
	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(), title="Error in contact patch")

	## Issue
	# raised_by_phone
	try:
		issues = frappe.get_all("Issue", fields=["*"], filters=[])
		
		for issue in issues:
			if(issue.get("raised_by_phone")!=""):
				if(len(issue.get("raised_by_phone"))==11):
					frappe.db.sql("""update `tabIssue`
						set raised_by_phone=%s where name=%s""",(issue.get("raised_by_phone")[1:11], issue.get("name")))
					frappe.db.commit()
	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(), title="Error in issue patch")

	## User
	# user's mobile_no
	try:
		users = frappe.get_all("User", fields=["*"], filters=[])
		
		for user in users:
			if(user.get("mobile_no")!=""):
				if(len(user.get("mobile_no"))==11):
					frappe.db.sql("""update `tabUser`
						set mobile_no=%s where name=%s""",(user.get("mobile_no")[1:11], user.get("name")))
					frappe.db.commit()
	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(), title="Error in User patch")