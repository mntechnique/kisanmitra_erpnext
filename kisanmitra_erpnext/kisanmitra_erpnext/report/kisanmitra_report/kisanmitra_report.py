# Copyright (c) 2013, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe 
from frappe import _
from datetime import datetime,date

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		_("Case No") + ":Link/Issue:100",
		_("Status") + ":Data:100",
		_("Department") + ":HTML:100",
		_("Mandal/Village") + ":HTML:100",
		_("Caller Name/Mobile No.") + ":HTML:100",
		_("Caste Catogery") + ":Data:100",
		_("Created Date") + "::100",
		_("Issue in Brief") + "::200",
		_("Cases Summary") + ":HTML:400",
		_("Updates") + ":HTML:400",
		_("Notes") + "::100",
	]	
	return columns

def get_data(filters):
	conditions = get_conditions(filters)
	issues = frappe.db.sql("""
		select iss.name, iss.status, iss.km_mandal_case, 
		iss.km_village_case, iss.km_caller_name, 
		iss.raised_by_phone, iss.km_caste, 
		iss.creation as creation_date, iss.km_case_category, 
		iss.description from `tabIssue` iss %s where iss.docstatus = 0 %s """% (conditions[0], conditions[1]), as_dict=1)
	data = [] 
	for issue in issues:
		update = ""
		department = ""
		case_category = ""
		mandal = ''
		village = ''
		mandal_village = ""
		note = ""
		comments = frappe.db.sql("""
			select content, date(creation) as creation_date from `tabCommunication` 
			where comment_type='Comment' and reference_name=%s order by creation desc""",
			issue.get("name"), as_dict=1)
		if comments:
			for comment in comments:
				update += "<p>"+str((comment.get("creation_date")).strftime("%d-%b,%y"))+":-"+comment.get("content")+"</p>"	
		department_list = frappe.db.sql("""
			select department_name from `tabKM Issue Department` 
			where parent=%s""",
			issue.get("name"), as_dict=1)
		if department_list:
			for dept in department_list:
				department += dept.get("department_name")+"<br>"

		category_list = frappe.db.sql("""
			select category from `tabKM Issue Category Item` 
			where parent=%s""",
			issue.get("name"), as_dict=1)
		if category_list:
			for category in category_list:
				case_category += category.get("category")+"<br>"
		mandal = issue.get("km_mandal_case") if issue.get("km_mandal_case") else "-"
		village = issue.get("km_village_case") if issue.get("km_village_case") else "-"
		mandal_village = str(mandal)+"<br>"+str(village)
		caller_name_mobile_no = str(issue.km_caller_name)+"<br>"+str(issue.raised_by_phone)
		creation = (issue.creation_date).strftime("%d-%b,%y %I:%M %p")
		row = [
			issue.name, issue.status, department,
			mandal_village,
			caller_name_mobile_no,
			issue.km_caste, creation,
			case_category, issue.description,
			update,note
		]
		data.append(row)
	return data

def get_conditions(filters):
	conditions = ""
	department_and_case_category = ""
	
	if filters.get("from_date"): 
		conditions += "and iss.creation >=" + "'" + filters.get("from_date") + "'"
	if filters.get("to_date"): 
		conditions += "and iss.creation <= " + "'" + filters.get("to_date") + "'"
	if filters.get("status"): 
		conditions += "and iss.status = " + "'" + filters.get("status") + "'"
	if filters.get("state"): 
		conditions += "and iss.km_state_case = " + "'" + filters.get("state") + "'"		
	if filters.get("district"):
		conditions += "and iss.km_district_case =" + "'" + filters.get("district") + "'"
	if filters.get("mandal"):
		conditions += "and iss.km_mandal_case =" + "'" + filters.get("mandal") + "'"
	if filters.get("village"):
		conditions += "and iss.km_village_case =" + "'" + filters.get("village") + "'"		
	if filters.get("department"):
		department_and_case_category += ",`tabKM Issue Department` d"
		conditions += "and iss.name=d.parent and d.department_name = " + "'" + filters.get("department") + "' "
	if filters.get("case_category"):
		department_and_case_category += ",`tabKM Issue Category Item` c"
		conditions += "and iss.name=c.parent and c.category = " + "'" + filters.get("case_category") + "' "

	return department_and_case_category, conditions