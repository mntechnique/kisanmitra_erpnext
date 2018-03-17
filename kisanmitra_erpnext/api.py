import frappe
from frappe import _
import csv
import re
from datetime import datetime
from frappe.model.naming import make_autoname

@frappe.whitelist()
def imported_data():
	finallist = []
	z = []
	with open('/home/deepak/Desktop/kisanmitra (copy).csv') as kmdata:
   		reader = csv.DictReader(kmdata)
   		for row in reader:
			z = import_leads(row)
  			finallist.append(z)
  	return finallist

def import_leads(eachrow):
	a = {
	"Mobile" : eachrow.get("Contacts Mobile Phone") ,
	"Lead Source" : eachrow.get("Contacts Contact Type"),
	"Territory" : eachrow.get("Contacts Mandal"),
	"modified _by" : eachrow.get("Contacts Last Modified By"),
	"creation" : eachrow.get("Contacts Created Time"),
	"modified" : eachrow.get("Contacts Modified Time"),
	"_assign" : eachrow.get("Contacts Assigned To"),
	"name" : eachrow.get("Cases Case Number")
	}
	return a


@frappe.whitelist()
def lead_source():
	unique_lead_source=[]
	with open('/home/deepak/Desktop/kisanmitra (copy).csv') as kmdata:
   		reader = csv.DictReader(kmdata)
   		for row in reader:
   			if(row.get("Contacts Contact Type")):
				unique_lead_source.append(row.get("Contacts Contact Type"))
  	return unique_lead_source	


@frappe.whitelist()
def lead():
	lead_list=[]
	contact_list=[]
	with open('/home/deepak/Desktop/kisanmitra (copy).csv') as kmdata:
   		reader = csv.DictReader(kmdata)
   		for row in reader:
			lead_list.append(row.get("Contacts First Name")+" "+row.get("Contacts Last Name"))
			dict={"first_name":row.get("Contacts First Name"),
				  "last_name":row.get("Contacts Last Name"),
				  "mobile":row.get("Contacts Mobile Phone"),
				  "source":row.get("Contacts Contact Type"),
				  "creation":row.get("Contacts Created Time"),
				  "modified":row.get("Contacts Modified Time"),
				  "modified_by":row.get("Contacts Last Modified By")}
			contact_list.append(dict)

	unique_lead = list(set(lead_list))
	count = 1
	for i in unique_lead:
		
		contact_details = [j for j in contact_list if i == (j.get("first_name")+" "+j.get("last_name"))][0]
		modified_by_name = contact_details.get("modified_by")
		name = str(make_autoname('LEAD-','#####'))
		source = contact_details.get("source")
		creation = frappe.utils.get_datetime_str(datetime.strptime(contact_details.get("creation"), "%d-%m-%Y %I:%M %p"))
		modified = frappe.utils.get_datetime_str(datetime.strptime(contact_details.get("modified"), "%d-%m-%Y %I:%M %p"))
		if modified_by_name == "Visheshwar Rao":
			modified_by_name = "Vishesh rao Urvetha"
		modified_by = (frappe.get_all("User" , filters = {"full_name":modified_by_name})[0]).get("name")
		
		frappe.db.sql("""insert into `tabLead`
		(organization_lead,lead_name,company_name, name, source, creation, modified, owner,
		modified_by) values
		(1,%s,%s,%s,%s,%s,%s,%s,%s)""",(i,i,name,source,creation,modified,modified_by, modified_by))

		new_contact = frappe.new_doc("Contact")
		new_contact.first_name = contact_details.get("first_name")
		new_contact.last_name = contact_details.get("last_name")
		new_contact.mobile_no = contact_details.get("mobile")
		new_contact.append("links",{
			"link_doctype":"Lead",
			"link_name":name
			})
		new_contact.save()

		print ("Lead {0}".format(count))
		count += 1
	frappe.db.commit()
	return True 

@frappe.whitelist()
def issue():
	issue_list=[]
	with open('/home/deepak/Desktop/KMissue.csv') as kmdata:
   		reader = csv.DictReader(kmdata)
   		for row in reader:
			dict={"subject":row.get("Case Title"),
				  "description":row.get("Summary"),
				  "creation":row.get("Created Date"),
				  "name":row.get("Case Number"),
				  "modified":row.get("Modified Time"),
				  "owner":row.get("Created By"),
				  "resolution_details":row.get("Resolution"),
				  "modified_by":row.get("Last Modified By"),
				  "km_resolution_type":row.get("Resolution Type"),
				  "km_caller_name":row.get("Caller Name"),
				  "km_are_you_calling_for_yourself":row.get("Are you calling for yourself"),
				  "km_caller_relationship_with_farmer":row.get("Caller relationship with Farmer"),
				  "km_mandal_case":row.get("Mandal case"),
				  "km_village_case":row.get("Village Case"),
				  "km_caste_category":row.get("Caste Category"),
				  "km_caste":row.get("Caste"),
				  "contact":row.get("Alternate Contact Number"),
				  "km_other_caste":row.get("Other Caste"),
				  "km_case_category":row.get("Case Category"),
				  "farmer_name":row.get("Farmer Name"),
				  "km_district_case":row.get("District case"),
				  "km_relation":row.get("Relation"),
				  "km_relation_name":row.get("Relation Name") }
			issue_list.append(dict)	
	count = 1
	for i in issue_list:
		
		name_prifix = 'VKB-' if str(i.get("name"))[0]=='V' or str(i.get("name"))[0]=='v' else 'KM-'
		name_suffix = str(map(int,re.findall('\d+', str(i.get("name"))))[0])
		while len(name_suffix) < 5:
			name_suffix = '0' + name_suffix
		name =str(str(name_prifix) + name_suffix)
		creation = frappe.utils.get_datetime_str(datetime.strptime(i.get("creation"), "%d-%m-%Y %I:%M %p"))
		modified = frappe.utils.get_datetime_str(datetime.strptime(i.get("modified"), "%d-%m-%Y %I:%M %p"))
		modified_by_name = i.get("modified_by")
		if modified_by_name == "Visheshwar Rao":
			modified_by_name = "Vishesh rao Urvetha"
		modified_by = (frappe.get_all("User" , filters = {"full_name":modified_by_name})[0]).get("name")
		km_are_you_calling_for_yourself = 1 if str(i.get("km_are_you_calling_for_yourself")) == 'yes' else 0
		lead = ''
		if len((frappe.get_all("Lead", filters={"company_name":i.get("km_caller_name")}))):
			lead = (frappe.get_all("Lead", filters={"company_name":i.get("km_caller_name")}))[0].get("name")
		elif len((frappe.get_all("Lead", filters={"company_name":i.get("farmer_name")}))):
			lead = (frappe.get_all("Lead", filters={"company_name":i.get("farmer_name")}))[0].get("name")	
		
		frappe.db.sql("""insert into `tabIssue`
		(subject, description, creation, name, modified, owner, resolution_details, modified_by,
		km_resolution_type, km_caller_name, km_are_you_calling_for_yourself, km_caller_relationship_with_farmer,
		km_mandal_case, km_village_case, km_caste_category, km_caste, contact, km_other_caste, km_case_category,
		km_district_case, km_relation, km_relation_name, raised_by, lead) values
		(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
		(i.get("subject"), i.get("description"), creation, name, modified,
		modified_by, i.get("resolution_details"), modified_by, i.get("km_resolution_type"),
		i.get("km_caller_name"), str(km_are_you_calling_for_yourself), i.get("km_caller_relationship_with_farmer"),
		i.get("km_mandal_case"), i.get("km_village_case"), i.get("km_caste_category"), i.get("km_caste"),
		i.get("contact"), i.get("km_other_caste"), i.get("km_case_category"),
		i.get("km_district_case"), i.get("km_relation"), i.get("km_relation_name"), modified_by, lead))

		print("Issue {0}".format(count))
		count += 1
	frappe.db.commit()		
  	return True



@frappe.whitelist()
def demo_issue():
	demo_list=[]
	# count = 1
	with open('/home/deepak/Desktop/KMissue.csv') as kmdata:
   		reader = csv.DictReader(kmdata)
   		for row in reader:
   			# if row.get("Resolution Type") == '':
   			# 	print(count)
			demo_list.append(row.get("Status"))
			# count += 1
	return demo_list


@frappe.whitelist()
def demo_lead():
	demo_list=[]
	# count = 1
	with open('/home/deepak/Desktop/kisanmitra (copy).csv') as kmdata:
   		reader = csv.DictReader(kmdata)
   		for row in reader:
   			if row.get("Contacts Last Name") == '0':	
				demo_list.append(row.get("Contacts First Name"))
			# count += 1
	return demo_list			

					
