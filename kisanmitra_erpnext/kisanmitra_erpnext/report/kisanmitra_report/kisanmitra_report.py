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
		# _("Case Catogery") + ":HTML:100",
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
		select name, status, km_mandal_case, 
		km_village_case, km_caller_name, 
		raised_by_phone, km_caste, 
		creation as creation_date, km_case_category, 
		description from `tabIssue` where docstatus = 0 %s """% conditions, as_dict=1)
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
		creation = (issue.creation_date).strftime("%d-%m-%Y %I:%M %p")
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
	
	if filters.get("from_date"): 
		conditions += "and creation >=" + "'" + filters.get("from_date") + "'"
	if filters.get("to_date"): 
		conditions += "and creation <= " + "'" + filters.get("to_date") + "'"
	if filters.get("status"): 
		conditions += "and status = " + "'" + filters.get("status") + "'"	
	if filters.get("district"):
		conditions += "and km_district_case =" + "'" + filters.get("district") + "'"
	return conditions