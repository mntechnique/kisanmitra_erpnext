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
		_("Case No") + ":Link/Issue:80",
		_("Department") + ":HTML:80",
		_("Mandal") + "::80",
		_("Village") + "::80",
		_("Caller Name") + "::80",
		_("Mobile No.") + "::80",
		_("Caste") + ":Data:80",
		_("Created Date") + "::80",
		_("Issue in Brief") + "::80",
		_("Cases Summary") + "::80",
		_("Updates") + ":HTML:80",
		_("Notes") + "::80",
	]	
	return columns

def get_data(filters):
	conditions = get_conditions(filters)
	issues = frappe.db.sql("""
		select name, km_department, km_mandal_case, 
		km_village_case, km_caller_name, 
		raised_by_phone, km_caste, 
		date(creation) as creation_date, km_case_category, 
		description from `tabIssue` where docstatus = 0 %s """% conditions, as_dict=1)
	data = [] 
	for issue in issues:
		update = ""
		department = ""
		case_category = ""
		comments = frappe.db.sql("""
			select content from `tabCommunication` 
			where comment_type='Comment' and reference_name=%s order by creation """,
			issue.get("name"), as_dict=1)
		if comments:
			for comment in comments:
				update += comment.get("content")+"<br>"	
		
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
		row = [
			issue.name, department,
			issue.km_mandal_case, issue.km_village_case,
			issue.km_caller_name, issue.raised_by_phone,
			issue.km_caste, issue.creation_date,
			case_category, issue.description,
			update
		]
		data.append(row)
	return data

def get_conditions(filters):
	conditions = ""
	
	if filters.get("from_date"): 
		conditions += "and creation >=" + "'" + filters.get("from_date") + "'"
	if filters.get("to_date"): 
		conditions += "and creation <= " + "'" + filters.get("to_date") + "'"
	if filters.get("status"): 
		conditions += "and status = " + "'" + filters.get("status") + "'"		
	return conditions
