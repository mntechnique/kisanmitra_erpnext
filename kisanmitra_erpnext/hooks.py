# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "kisanmitra_erpnext"
app_title = "KisanMitra ERPNext"
app_publisher = "MN Technique"
app_description = "ERPNext customisations for KisanMitra ERPNext"
app_icon = "fa fa-handshake-o"
app_color = "green"
app_email = "support@mntechnique.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/kisanmitra_erpnext/css/kisanmitra_erpnext.css"
# app_include_js = "/assets/kisanmitra_erpnext/js/kisanmitra_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/kisanmitra_erpnext/css/kisanmitra_erpnext.css"
# web_include_js = "/assets/kisanmitra_erpnext/js/kisanmitra_erpnext.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "kisanmitra_erpnext.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "kisanmitra_erpnext.install.before_install"
# after_install = "kisanmitra_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "kisanmitra_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"kisanmitra_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"kisanmitra_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"kisanmitra_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"kisanmitra_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"kisanmitra_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "kisanmitra_erpnext.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "kisanmitra_erpnext.event.get_events"
# }

fixtures = [
	{
		"dt":"Custom Field", 
		"filters": [["name", "in", ["Issue-section_break_28",
									"Issue-km_resolution_type",
									"Issue-km_caller_name",
									"Issue-km_are_you_calling_for_yourself",
									"Issue-km_caller_relationship_with_farmer",
									"Issue-km_mandal_case",
									"Issue-km_village_case",
									"Issue-km_caste_category",
									"Issue-column_break_36",
									"Issue-km_caste",
									"Issue-km_other_caste",
									"Issue-km_case_category",
									"Issue-km_district_case",
									"Issue-km_relation",
									"Communication-section_break_48",
									"Communication-km_call_status",
									"Communication-km_call_customer",
									"Communication-column_break_52",
									"Communication-km_call_duration",
									"Communication-km_call_gateway",
									"Communication-km_calls_start_time",
									"Communication-km_calls_end_time"]]]
	}]