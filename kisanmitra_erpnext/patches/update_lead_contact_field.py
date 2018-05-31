import frappe
import os
import csv
import re

def execute():
	issues = []
	file_path = os.path.join(frappe.get_site_path(), "public","files", "issue_contact.csv")
	with open(file_path) as kmdata:
		reader = csv.DictReader(kmdata)
		for row in reader:
			dict = {"lead":row.get("Contacts First Name"),
					"name":row.get("Cases Case Number")}
			issues.append(dict)

	for issue in issues:
		name_prifix = 'VKB-' if str(issue.get("name"))[0]=='V' or str(issue.get("name"))[0]=='v' else 'KM-'
		name_suffix = str(map(int,re.findall('\d+', str(issue.get("name"))))[0])
		while len(name_suffix) < 5:
			name_suffix = '0' + name_suffix
		name =str(str(name_prifix) + name_suffix)
		lead = ''
		lead_name = str(issue.get("lead"))+" 0"
		contact = ''
		raised_by_phone = ''
		lead = (frappe.get_all("Lead", filters={"company_name":lead_name}))[0].get("name") if (frappe.get_all("Lead", filters={"company_name":lead_name})) else ""
		if lead_name and lead:
			contact = frappe.db.get_value("Dynamic Link",{"link_name":lead},"parent")
			raised_by_phone = frappe.db.get_value("Contact",contact,"mobile_no")
			if lead and contact and raised_by_phone:
				frappe.db.sql("""update `tabIssue`
						set lead=%s, contact=%s,
						raised_by_phone=%s where name=%s""",(lead,contact,raised_by_phone,name))
	