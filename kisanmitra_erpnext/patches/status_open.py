import frappe
import os
import csv
import re
from datetime import datetime

def execute():
	frappe.reload_doc("support", "doctype", "issue")

	issues = frappe.get_all("Issue", filters={"status":"Open"})


	file_path = os.path.join(frappe.get_site_path(), "public","files", "status_open.csv")

	issues = []
	with open(file_path) as kmdata:
		reader = csv.DictReader(kmdata)
		for row in reader:
			dict = {"km_name":row.get("Case Number"),
					"km_modified":row.get("Modified Time"),
					"km_modified_by":row.get("Last Modified By"),
					"km_status":row.get("Status")}
			issues.append(dict)

	for issue in issues:
		name_prifix = 'VKB-' if str(issue.get("km_name"))[0]=='V' or str(issue.get("km_name"))[0]=='v' else 'KM-'
		name_suffix = str(map(int,re.findall('\d+', str(issue.get("km_name"))))[0])
		while len(name_suffix) < 5:
			name_suffix = '0' + name_suffix
		name =str(str(name_prifix) + name_suffix)
		modified = frappe.utils.get_datetime_str(datetime.strptime(issue.get("km_modified"), "%d-%m-%Y %I:%M %p"))
		modified_by_name = issue.get("km_modified_by")
		if modified_by_name == "Visheshwar Rao":
			modified_by_name = "Vishesh rao Urvetha"
		modified_by = (frappe.get_all("User" , filters = {"full_name":modified_by_name})[0]).get("name")

		if frappe.get_all("Issue",filters={"name":name,"status":"Open"}):
			if frappe.get_doc("Issue",name).modified_by == "Administrator":
				frappe.db.sql("""update `tabIssue`
					set status=%s, modified_by=%s,
					modified=%s where name=%s""",( issue.get("km_status"), modified_by,
						modified, name))

			else :
				frappe.db.sql("""update `tabIssue`
					set status=%s where name=%s""",(issue.get("km_status"), name))