import frappe
from frappe import _
import csv

@frappe.whitelist()
def imported_data():
	finallist = []
	z = []
	with open('/home/siddhi/Desktop/kmdatadump.csv') as kmdata:
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