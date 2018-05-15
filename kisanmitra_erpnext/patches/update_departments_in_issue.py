import frappe

def execute():
	frappe.reload_doc("support", "doctype", "issue")

	issues = frappe.get_all("Issue", fields=["name", "creation", "owner", "modified_by", "modified", "km_department"])

	sql = """
		INSERT INTO `tabKM Issue Department` (name, creation, owner, modified, modified_by, parent, parentfield, parenttype, department_name) 
		VALUES {0}
	"""

	for issue in issues:
		if issue.km_department:
			departments = (issue.km_department).split(",")
			departments = [department.strip() for department in departments]

			values = []
			for department in departments:
				values.append(
					"('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')"
					.format(frappe.generate_hash(length=10), issue.creation, issue.owner, issue.modified, issue.modified_by, issue.name, "km_issue_department", "Issue", department)
				)

			query = sql.format(", ".join(values) + ";")

			frappe.db.sql(query)
