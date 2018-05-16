import frappe

def execute():
	frappe.reload_doc("support", "doctype", "issue")

	issues = frappe.get_all("Issue", fields=["name", "creation", "owner", "modified_by", "modified", "km_case_category"])

	sql = """
		INSERT INTO `tabKM Issue Category Item` (name, creation, owner, modified, modified_by, parent, parentfield, parenttype, category) 
		VALUES {0}
	"""

	for issue in issues:
		if issue.km_case_category:
			case_categories = (issue.km_case_category).split(",")
			case_categories = [department.strip() for department in departments]

			values = []
			for case_category in case_categories:
				values.append(
					"('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')"
					.format(frappe.generate_hash(length=10), issue.creation, issue.owner, issue.modified, issue.modified_by, issue.name, "km_issue_category", "Issue", case_category)
				)

			query = sql.format(", ".join(values) + ";")

			frappe.db.sql(query)