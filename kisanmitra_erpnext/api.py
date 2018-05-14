import frappe
from frappe import _, msgprint
import os
import csv
import re
from datetime import datetime
from frappe.model.naming import make_autoname
from frappe.core.page.background_jobs.background_jobs import get_info

@frappe.whitelist()
def lead_outer():
	if not is_queue_running('kisanmitra_erpnext.api.lead_inner'):
		result = frappe.enqueue('kisanmitra_erpnext.api.lead_inner',
			queue="long",timeout=3500
		)


@frappe.whitelist()
def issue_outer():
	if not is_queue_running('kisanmitra_erpnext.api.issue_inner'):
		result = frappe.enqueue('kisanmitra_erpnext.api.issue_inner',
			queue="long",timeout=3500
		)


@frappe.whitelist()
def comment_outer():
	if not is_queue_running('kisanmitra_erpnext.api.comment_inner'):
		result = frappe.enqueue('kisanmitra_erpnext.api.comment_inner',
			queue="long",timeout=3500
		)


@frappe.whitelist()
def phone_call_outer():
	if not is_queue_running('kisanmitra_erpnext.api.phone_call_inner'):
		result = frappe.enqueue('kisanmitra_erpnext.api.phone_call_inner',
			queue="long",timeout=3500
		)


@frappe.whitelist()
def vikarabad_outer():
	if not is_queue_running('kisanmitra_erpnext.api.vikarabad_inner'):
		result = frappe.enqueue('kisanmitra_erpnext.api.vikarabad_inner',
			queue="long",timeout=3500
		)



@frappe.whitelist()
def adilabad_outer():
	if not is_queue_running('kisanmitra_erpnext.api.adilabad_inner'):
		result = frappe.enqueue('kisanmitra_erpnext.api.adilabad_inner',
			queue="long",timeout=3500
		)										


def lead_inner():
	lead_list=[]
	contact_list=[]
	file_name = (frappe.get_doc("KissanMitra ERPNext Settings","KissanMitra ERPNext Settings").import_lead).strip("/files")
	lead_file_path = os.path.join(frappe.get_site_path(), "public","files", file_name)
	try:
		with open(lead_file_path) as kmdata:
	   		reader = csv.DictReader(kmdata)
	   		for row in reader:
				lead_list.append(row.get("Contacts First Name")+" "+row.get("Contacts Last Name"))
				dict={"first_name":row.get("Contacts First Name"),
					  "last_name":row.get("Contacts Last Name"),
					  "mobile":row.get("Contacts Mobile Phone"),
					  "creation":row.get("Contacts Created Time"),
					  "modified":row.get("Contacts Modified Time"),
					  "modified_by":row.get("Contacts Last Modified By")}
				contact_list.append(dict)

		unique_lead = list(set(lead_list))
		frappe.msgprint("importing lead started")

		for i in unique_lead:
			
			contact_details = [j for j in contact_list if i == (j.get("first_name")+" "+j.get("last_name"))][0]
			modified_by_name = contact_details.get("modified_by")
			name = str(make_autoname('LEAD-','#####'))
			creation = frappe.utils.get_datetime_str(datetime.strptime(contact_details.get("creation"), "%Y-%m-%d %I:%M %p"))
			modified = frappe.utils.get_datetime_str(datetime.strptime(contact_details.get("modified"), "%Y-%m-%d %I:%M %p"))
			if modified_by_name == "Visheshwar Rao":
				modified_by_name = "Vishesh rao Urvetha"
			modified_by = (frappe.get_all("User" , filters = {"full_name":modified_by_name})[0]).get("name")

			if contact_details.get("mobile") == "" or not frappe.get_all("Contact",filters = {"mobile_no":contact_details.get("mobile")}):
			
				frappe.db.sql("""insert into `tabLead`
				(organization_lead,lead_name,company_name, name, creation, modified, owner,
				modified_by) values
				(1,%s,%s,%s,%s,%s,%s,%s)""",(i,i,name,creation,modified,modified_by, modified_by))

				new_contact = frappe.new_doc("Contact")
				new_contact.first_name = contact_details.get("first_name")
				new_contact.last_name = contact_details.get("last_name")
				new_contact.mobile_no = contact_details.get("mobile")
				new_contact.append("links",{
					"link_doctype":"Lead",
					"link_name":name
					})
				new_contact.save()
		frappe.db.commit() 
		frappe.msgprint("importing lead completed")
	except Exception as e:
		frappe.db.rollback()
    	frappe.log_error(message=frappe.get_traceback(), title="Error in lead import")	


def issue_inner():
	issue_list=[]
	file_name = (frappe.get_doc("KissanMitra ERPNext Settings","KissanMitra ERPNext Settings").import_issue).strip("/files")
	issue_file_path = os.path.join(frappe.get_site_path(), "public","files", file_name)
	try:
		with open(issue_file_path) as kmdata:
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
					  "km_other_caste":row.get("Other Caste"),
					  "km_case_category":row.get("Case Category"),
					  "farmer_name":row.get("Farmer Name"),
					  "km_state_case":"Telangana",
					  "km_status":row.get("Status"),
					  # "km_state_case":row.get("State Case"),
					  "km_district_case":row.get("District case"),
					  "km_relation":row.get("Relation"),
					  "km_relation_name":row.get("Relation Name"),
					  "km_call_type":row.get("Call Type") ,
					  "km_priority":row.get("Priority"),
					  "km_department":row.get("Department")}
				issue_list.append(dict)	
		frappe.msgprint("importing issue started")		
		for i in issue_list:
			
			name_prifix = 'VKB-' if str(i.get("name"))[0]=='V' or str(i.get("name"))[0]=='v' else 'KM-'
			name_suffix = str(map(int,re.findall('\d+', str(i.get("name"))))[0])
			while len(name_suffix) < 5:
				name_suffix = '0' + name_suffix
			name =str(str(name_prifix) + name_suffix)
			creation = frappe.utils.get_datetime_str(datetime.strptime(i.get("creation"), "%Y-%m-%d %I:%M %p"))
			modified = frappe.utils.get_datetime_str(datetime.strptime(i.get("modified"), "%Y-%m-%d %I:%M %p"))
			owner_by_name = i.get("owner")
			if owner_by_name == "Visheshwar Rao":
				owner_by_name = "Vishesh rao Urvetha"
			owner = (frappe.get_all("User" , filters = {"full_name":owner_by_name})[0]).get("name")	
			modified_by_name = i.get("modified_by")
			if modified_by_name == "Visheshwar Rao":
				modified_by_name = "Vishesh rao Urvetha"
			modified_by = (frappe.get_all("User" , filters = {"full_name":modified_by_name})[0]).get("name")
			km_are_you_calling_for_yourself = 1 if str(i.get("km_are_you_calling_for_yourself")) == 'yes' else 0
			lead = ''
			contact = ''
			if len((frappe.get_all("Lead", filters={"company_name":i.get("km_caller_name")}))):
				lead = (frappe.get_all("Lead", filters={"company_name":i.get("km_caller_name")}))[0].get("name")
			elif len((frappe.get_all("Lead", filters={"company_name":i.get("farmer_name")}))):
				lead = (frappe.get_all("Lead", filters={"company_name":i.get("farmer_name")}))[0].get("name")
			if lead:
				contact = frappe.db.get_value("Dynamic Link",{"link_name":lead},"parent")
			state = str(i.get("km_state_case"))
			district = str(i.get("km_district_case"))
	 		mandal = str(i.get("km_mandal_case"))
	 		village = str(i.get("km_village_case"))
	 		if mandal == "Vikarabad":
				mandal = "Vikarabad(M)"
			if village == "Vikarabad":
				village = "Vikarabad(V)"
						
			
			if not frappe.get_all("Territory",filters = {"is_group":1 ,"parent_territory":"India" ,"territory_name":state}) and \
			state:
				new_state_territory = frappe.new_doc("Territory")
				new_state_territory.is_group = 1
				new_state_territory.parent_territory = "All Territories"
				new_state_territory.territory_name = state
				new_state_territory.save()

			if state:	
				if not frappe.get_all("Territory",filters = {"is_group":1 ,"parent_territory":state ,"territory_name":district}) and  \
				district:
					new_district_territory = frappe.new_doc("Territory")
					new_district_territory.is_group = 1
					new_district_territory.parent_territory = state
					new_district_territory.territory_name = district
					new_district_territory.save()

			if district:	
				if frappe.get_all("Territory",filters = {"is_group":1 ,"parent_territory":district ,"territory_name":mandal}):
					mandal = mandal
				elif frappe.get_all("Territory",filters = {"is_group":1 ,"parent_territory":district ,"territory_name":mandal + " (" + district + ")"}):
					mandal = mandal + " (" + district + ")"
				elif frappe.get_all("Territory",filters = {"territory_name":mandal}):
					mandal = mandal + " (" + district + ")"
				if not frappe.get_all("Territory",filters = {"is_group":1 ,"parent_territory":district ,"territory_name":mandal}) and \
				mandal:
					new_mandal_territory = frappe.new_doc("Territory")
					new_mandal_territory.is_group = 1
					new_mandal_territory.parent_territory = district
					new_mandal_territory.territory_name = mandal
					new_mandal_territory.save()
	 		
			if mandal:
				if frappe.get_all("Territory",filters = {"parent_territory":mandal ,"territory_name":village}):
					village = village
				elif frappe.get_all("Territory",filters = {"parent_territory":mandal ,"territory_name":village + " (" + mandal + ")"}):
					village = village + " (" + mandal + ")"
				elif frappe.get_all("Territory",filters = {"territory_name":village}):
					village = village + " (" + mandal + ")"
				if not frappe.get_all("Territory",filters = {"parent_territory":mandal ,"territory_name":village}) and \
				village:
					new_village_territory = frappe.new_doc("Territory")
					new_village_territory.parent_territory = mandal
					new_village_territory.territory_name = village
					new_village_territory.save()			

			frappe.db.sql("""insert into `tabIssue`
			(subject, description, creation, name, modified, owner, resolution_details, modified_by,
			km_resolution_type, km_caller_name, km_are_you_calling_for_yourself, km_caller_relationship_with_farmer,
			km_mandal_case, km_village_case, km_caste_category, km_caste, contact, km_other_caste, km_case_category,
			km_district_case, km_relation, km_relation_name, raised_by, lead, 
			km_state_case, km_call_type, km_priority, km_department, status, company, communication_medium) values
			(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
			(i.get("subject"), i.get("description"), creation, name, modified,
			owner, i.get("resolution_details"), modified_by, i.get("km_resolution_type"),
			i.get("km_caller_name"), str(km_are_you_calling_for_yourself), i.get("km_caller_relationship_with_farmer"),
			mandal, village, i.get("km_caste_category"), i.get("km_caste"),
			contact, i.get("km_other_caste"), i.get("km_case_category"),district, i.get("km_relation"), 
			i.get("km_relation_name"), modified_by, lead, 
			state, i.get("km_call_type"), i.get("km_priority"), i.get("km_department"), i.get("km_status"), "KisanMitra",
			"Phone"))
		frappe.db.commit()
		frappe.msgprint("importing issue completed")		
	except Exception as e:
		frappe.db.rollback()
    	frappe.log_error(message=frappe.get_traceback(), title="Error in issue import")


def comment_inner():
	comment_list=[]
	file_name = (frappe.get_doc("KissanMitra ERPNext Settings","KissanMitra ERPNext Settings").import_comments).strip("/files")
	comment_file_path = os.path.join(frappe.get_site_path(), "public","files", file_name)
	try:
		with open(comment_file_path) as kmdata:
	   		reader = csv.DictReader(kmdata)
	   		for row in reader:
	   			dict={"case_number":row.get("Cases Case Number") ,
	   				  "content":row.get("Comments Comment"),
	   				  "reference_owner":row.get("Comments Creator"),
	   				  "subject":row.get("Comments Related To"),
	   				  "creation":row.get("Comments Created Time"),
	   				  "modified":row.get("Comments Modified Time")}
				comment_list.append(dict)

		frappe.msgprint("importing comments started")
		for i in comment_list:
			reference_name=''
			reference_doctype = ''
			status = 'Open'
			if i.get("case_number"):
				name_prifix = 'VKB-' if str(i.get("case_number"))[0]=='V' or str(i.get("case_number"))[0]=='v' else 'KM-'
				name_suffix = str(map(int,re.findall('\d+', str(i.get("case_number"))))[0])
				while len(name_suffix) < 5:
					name_suffix = '0' + name_suffix
				reference_name =str(str(name_prifix) + name_suffix)
				reference_doctype = "Issue"
				status = "Linked"
			name = frappe.generate_hash(length=10)
			creation = frappe.utils.get_datetime_str(datetime.strptime(i.get("creation"), "%Y-%m-%d %I:%M %p"))
			modified = frappe.utils.get_datetime_str(datetime.strptime(i.get("modified"), "%Y-%m-%d %I:%M %p"))
			modified_by_name = i.get("reference_owner")
			if modified_by_name == "Visheshwar Rao":
				modified_by_name = "Vishesh rao Urvetha"
			modified_by = (frappe.get_all("User" , filters = {"full_name":modified_by_name})[0]).get("name")
			sender_full_name = modified_by_name

			frappe.db.sql("""insert into `tabCommunication`
			(comment_type, communication_type, content, reference_owner, subject, 
			reference_doctype, reference_name, communication_date, user, 
			creation, modified, modified_by, name , status, 
			sender_full_name ,sent_or_received) values
			('Comment','Comment',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
			(i.get("content"),modified_by, i.get("subject"), reference_doctype, reference_name, creation,
			modified_by, creation, modified, modified_by, name ,status, sender_full_name, 'Sent'))
		frappe.db.commit()	
		frappe.msgprint("importing comments completed")	
	except Exception as e:
		frappe.db.rollback()
    	frappe.log_error(message=frappe.get_traceback(), title="Error in comments import")	




def phone_call_inner():
	phone_call_list=[]
	file_name = (frappe.get_doc("KissanMitra ERPNext Settings","KissanMitra ERPNext Settings").import_phone_call).strip("/files")
	phone_call_file_path = os.path.join(frappe.get_site_path(), "public","files", file_name)
	try:
		with open(phone_call_file_path) as kmdata:
	   		reader = csv.DictReader(kmdata)
	   		for row in reader:
	   			dict={"case_number":row.get("Cases Case Number") ,
	   				  "reference_owner":row.get("Phone Calls Created By"),
	   				  "subject":row.get("Phone Calls Cases"),
	   				  "creation":row.get("Phone Calls Created Time"),
	   				  "modified":row.get("Phone Calls Modified Time"),
	   				  "modified_by":row.get("Phone Calls Last Modified By"),
	   				  "sent_or_received":row.get("Phone Calls Direction"),
	   				  "km_call_status":row.get("Phone Calls Call Status"),
	   				  "km_call_customer":row.get("Phone Calls Customer"),
	   				  "phone_no":row.get("Phone Calls Customer Number"),
	   				  "km_calls_start_time":row.get("Phone Calls Start Time"),
	   				  "km_calls_end_time":row.get("Phone Calls End Time"),
	   				  "recording_url":row.get("Phone Calls Recording"),
					  "sid":row.get("Phone Calls Source UUID"),
	   				  "km_call_duration":row.get("Phone Calls Duration (sec)"),
	   				  "km_call_gateway":row.get("Phone Calls Gateway")}
				phone_call_list.append(dict)

		frappe.msgprint("importing phone_call started")		
		for i in phone_call_list:
			if i.get("modified_by") and i.get("km_calls_start_time"):
				reference_name=''
				reference_doctype = ''
				km_calls_start_time = ''
				km_calls_end_time = ''
				status = 'Open'
				mgs = ''
				if i.get("case_number"):
					name_prifix = 'VKB-' if str(i.get("case_number"))[0]=='V' or str(i.get("case_number"))[0]=='v' else 'KM-'
					name_suffix = str(map(int,re.findall('\d+', str(i.get("case_number"))))[0])
					while len(name_suffix) < 5:
						name_suffix = '0' + name_suffix
					reference_name =str(str(name_prifix) + name_suffix)
					reference_doctype = "Issue"
					status = "Linked"
				name = frappe.generate_hash(length=10)
				creation = frappe.utils.get_datetime_str(datetime.strptime(i.get("creation"), "%Y-%m-%d %I:%M %p"))
				modified = frappe.utils.get_datetime_str(datetime.strptime(i.get("modified"), "%Y-%m-%d %I:%M %p"))
				km_calls_start_time = frappe.utils.get_datetime_str(datetime.strptime(i.get("km_calls_start_time"), "%Y-%m-%d %I:%M %p"))
				if i.get("km_calls_end_time"):
					km_calls_end_time = frappe.utils.get_datetime_str(datetime.strptime(i.get("km_calls_end_time"), "%Y-%m-%d %I:%M %p"))
				elif (i.get("km_calls_end_time") =='' and i.get("km_call_duration") == 0):
					km_calls_end_time = frappe.utils.get_datetime_str(datetime.strptime(i.get("km_calls_start_time"), "%Y-%m-%d %I:%M %p"))
				modified_by_name = i.get("reference_owner")
				if modified_by_name == "Visheshwar Rao":
					modified_by_name = "Vishesh rao Urvetha"
				modified_by = (frappe.get_all("User" , filters = {"full_name":modified_by_name})[0]).get("name")
				sender_full_name = modified_by_name
				if i.get("sent_or_received") == "inbound":
					sent_or_received = "Received"
					if i.get("km_call_customer"):
						mgs = "I received a call from "+i.get("phone_no")+"("+i.get("km_call_customer")+") and spoke for "+i.get("km_call_duration")+" sec"
					else :
						mgs = "I received a call from "+i.get("phone_no")+" and spoke for "+i.get("km_call_duration")+" sec"
				else :
					sent_or_received = "Sent"	
					if i.get("km_call_customer"):
						mgs = "I call to "+i.get("phone_no")+"("+i.get("km_call_customer")+") and spoke for "+i.get("km_call_duration")+" sec"
					else :
						mgs = "I call to "+i.get("phone_no")+" and spoke for "+i.get("km_call_duration")+" sec"	

				frappe.db.sql("""insert into `tabCommunication`
				(comment_type, communication_type, reference_owner, subject, reference_doctype, reference_name, 
				communication_date, user, creation, modified, modified_by, name , status, sender_full_name , sent_or_received , 
				km_call_status , km_call_customer , phone_no , km_calls_start_time , km_calls_end_time , km_call_duration , 
				km_call_gateway , owner, sid, recording_url, communication_medium, content) values 
				('Info', 'Communication', %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
				(modified_by ,i.get("subject") ,reference_doctype ,reference_name ,creation ,modified_by, creation, modified, 
				modified_by, name ,status ,sender_full_name ,sent_or_received ,i.get("km_call_status") ,i.get("km_call_customer") ,
				i.get("phone_no") ,km_calls_start_time ,km_calls_end_time ,i.get("km_call_duration") ,
				'Exotel' ,modified_by ,i.get("sid"), i.get("recording_url"), 'Phone', mgs))

				if row.get("Phone Calls Customer Number"):
					if not len((frappe.get_all("Contact", filters={"mobile_no":row.get("Phone Calls Customer Number")}))):
						if m.km_caller_name == i.get("km_call_customer"):
							first_name = i.get("km_call_customer")
						elif i.get("km_call_customer"):
							first_name = i.get("km_call_customer")
						elif m.km_caller_name:
							first_name = m.km_caller_name
						if first_name:
							new_contact = frappe.new_doc("Contact")
							new_contact.first_name = first_name
							new_contact.last_name = row.get("Phone Calls Customer Number")
							new_contact.mobile_no = row.get("Phone Calls Customer Number")
							new_contact.save()
							m = frappe.get_doc("Issue",reference_name)
							if m.contact == '':
								m.contact = new_contact.name
								m.save()
		frappe.db.commit()
		frappe.msgprint("importing phone_call completed")	
	except Exception as e:
		frappe.db.rollback()
    	frappe.log_error(message=frappe.get_traceback(), title="Error in phone_call import")		



def vikarabad_inner():
	vikarabad_list=[]
	vikarabad_village_list=[]
	duplicate_village_list = []
	file_name = (frappe.get_doc("KissanMitra ERPNext Settings","KissanMitra ERPNext Settings").import_vikarabad).strip("/files")
	vikarabad_file_path = os.path.join(frappe.get_site_path(), "public","files", file_name)
	try:
		with open(vikarabad_file_path) as kmdata:
	   		reader = csv.DictReader(kmdata)
	   		for row in reader:
	   			dict = {"mandal":row.get("mandal"),"Village":row.get("Village")}
	   			vikarabad_village_list.append(row.get("Village"))
	   			vikarabad_list.append(dict)	
	   		unique_village_list = list(set(vikarabad_village_list))
	   		for i in unique_village_list:
	   			m = [ j for j in vikarabad_village_list if j == i]
	   			if len(m) > 1:
	   				duplicate_village_list.append(m[0])		
		frappe.msgprint("importing started")
		for vkb in vikarabad_list:	
			mandal = str(vkb.get("mandal"))
			village = str(vkb.get("Village"))

			if [ k for k in duplicate_village_list if k == vkb.get("Village")]:
				village = village + " (" + mandal + ")"

			if mandal == "Vikarabad":
				mandal = "Vikarabad(M)"
			if village == "Vikarabad":
				village = "Vikarabad(V)"
			if frappe.get_all("Territory",filters = {"is_group":1 ,"parent_territory":"Vikarabad" ,"territory_name":village}):
				village = village + " (" + mandal + ")"	

			if not frappe.get_all("Territory",filters = {"is_group":1 ,"parent_territory":"Vikarabad" ,"territory_name":mandal}) and mandal:
				new_mandal_territory = frappe.new_doc("Territory")
				new_mandal_territory.is_group = 1
				new_mandal_territory.parent_territory = "Vikarabad"
				new_mandal_territory.territory_name = mandal
				new_mandal_territory.save()

			if not frappe.get_all("Territory",filters = {"parent_territory":mandal ,"territory_name":village}) and \
			not frappe.get_all("Territory",filters = {"parent_territory":mandal ,"territory_name":village + " (" + mandal + ")"}) and mandal and village:
				new_village_territory = frappe.new_doc("Territory")
				new_village_territory.parent_territory = mandal
				new_village_territory.territory_name = village
				new_village_territory.save()
		frappe.db.commit()
		frappe.msgprint("importing completed")
	except Exception as e:
		frappe.db.rollback()
    	frappe.log_error(message=frappe.get_traceback(), title="Error in vikarabad import")	

def adilabad_inner():
	adilabad_list=[]
	adilabad_village_list=[]
	duplicate_village_list = []

	file_name = (frappe.get_doc("KissanMitra ERPNext Settings","KissanMitra ERPNext Settings").import_adilabad).strip("/files")
	adilabad_file_path = os.path.join(frappe.get_site_path(), "public","files", file_name)
	try:
		with open(adilabad_file_path) as kmdata:
	   		reader = csv.DictReader(kmdata)
	   		for row in reader:
	   			dict = {"Mandal":row.get("Mandal"),"Village":row.get("Village")}
	   			adilabad_village_list.append(row.get("Village"))	
	   			adilabad_list.append(dict)
	   		unique_village_list = list(set(adilabad_village_list))
	   		for i in unique_village_list:
	   			m = [ j for j in adilabad_village_list if j == i]
	   			if len(m) > 1:
	   				duplicate_village_list.append(m[0])
		frappe.msgprint("importing started")
		for albd in adilabad_list:	
			mandal = str(albd.get("Mandal"))
			village = str(albd.get("Village"))
			if [ k for k in duplicate_village_list if k == albd.get("Village")]:
				village = village + " (" + mandal + ")"
			if frappe.get_all("Territory",filters = {"is_group":1 ,"parent_territory":"Adilabad" ,"territory_name":village}):
				village = village + " (" + mandal + ")"		

			if not frappe.get_all("Territory",filters = {"is_group":1 ,"parent_territory":"Adilabad" ,"territory_name":mandal}) and mandal:
				new_mandal_territory = frappe.new_doc("Territory")
				new_mandal_territory.is_group = 1
				new_mandal_territory.parent_territory = "Adilabad"
				new_mandal_territory.territory_name = mandal
				new_mandal_territory.save()

			if not frappe.get_all("Territory",filters = {"parent_territory":mandal ,"territory_name":village}) and \
			not frappe.get_all("Territory",filters = {"parent_territory":mandal ,"territory_name":village + " (" + mandal + ")"}) and mandal and village:
				new_village_territory = frappe.new_doc("Territory")
				new_village_territory.parent_territory = mandal
				new_village_territory.territory_name = village
				new_village_territory.save()	
		frappe.db.commit()
		frappe.msgprint("importing completed")
	except Exception as e:
		frappe.db.rollback()
    	frappe.log_error(message=frappe.get_traceback(), title="Error in adilabad import")	

@frappe.whitelist()
def delete_data():
	delete_all_data =(frappe.get_doc("KissanMitra ERPNext Settings","KissanMitra ERPNext Settings").delete_data_for).split(",")
	for delete in delete_data:
		if delete == "Contact":
			data = frappe.get_all("Contact")
			frappe.msgprint("Contacts Deletion started")
			for i in data:
				frappe.delete_doc("Contact",i.name)
			frappe.db.sql("""delete from `tabCommunication` where reference_doctype='Contact'""")	
			frappe.db.commit()
			frappe.msgprint("All Contacts Deleted")
		elif delete == "Lead":
			data = frappe.get_all("Lead")
			frappe.msgprint("Leads Deletion started")
			for i in data:
				frappe.delete_doc("Lead",i.name)
			frappe.db.sql("""delete from `tabCommunication` where reference_doctype='Lead'""")	
			frappe.db.commit()
			frappe.msgprint("All Leads Deleted")
		elif delete == "Issue":
			data = frappe.get_all("Issue")
			frappe.msgprint("Issues Deletion started")
			for i in data:
				frappe.delete_doc("Issue",i.name)
			frappe.db.sql("""delete from `tabCommunication` where reference_doctype='Issue'""")
			frappe.db.commit()
			frappe.msgprint("All Issues Deleted")
		elif delete == "Comments":
			frappe.msgprint("Comments Deletion started")
			frappe.db.sql("""delete from `tabCommunication` where reference_doctype='Issue' and comment_type='Comment'""")
			frappe.db.commit()
			frappe.msgprint("All Comments Deleted")
		elif delete == "Phone-call":
			frappe.msgprint("Phone Calls Deletion started")
			frappe.db.sql("""delete from `tabCommunication` where reference_doctype='Issue' and communication_medium='Phone'""")
			frappe.db.commit()
			frappe.msgprint("All Phone Calls Deleted")


def get_job_queue(job_name):
	queue_info = get_info()
	queue_by_job_name = [queue for queue in queue_info if queue.get("job_name")==job_name]
	return queue_by_job_name

def is_queue_running(job_name):
	queue = get_job_queue(job_name)
	return queue and len(queue) > 0 and queue[0].get("status") in ["started", "queued"]