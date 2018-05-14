// Copyright (c) 2018, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('KissanMitra ERPNext Settings', {
	refresh: function(frm) {
		import_lead(frm);
		import_issue(frm);
		import_comments(frm);
		import_phone_call(frm);
		import_vikarabad(frm);
		import_adilabad(frm);
		delete_data(frm);

	},

	delete_data_for: function(frm) {
		frm.save();
	}
});

function import_lead(frm) {
	var wrapper = $(frm.fields_dict["import"].wrapper);
	wrapper.find(".btn-import-lead").on("click", function() {
		frappe.call({
			method: "kisanmitra_erpnext.api.lead_outer",
		}).done((r) => {
		}).fail((r)=>{
			console.log(r);
		});
	})
}

function import_issue(frm) {
	var wrapper = $(frm.fields_dict["import_issue_button"].wrapper);
	wrapper.find(".btn-import-issue").on("click", function() {
		frappe.call({
			method: "kisanmitra_erpnext.api.issue_outer",
		}).done((r) => {
		}).fail((r)=>{
			console.log(r);
		});
	})
}

function import_comments(frm) {
	var wrapper = $(frm.fields_dict["import_comments_button"].wrapper);
	wrapper.find(".btn-import-comments").on("click", function() {
		frappe.call({
			method: "kisanmitra_erpnext.api.comment_outer",
		}).done((r) => {
		}).fail((r)=>{
			console.log(r);
		});
	})
}

function import_phone_call(frm) {
	var wrapper = $(frm.fields_dict["import_phone_call_button"].wrapper);
	wrapper.find(".btn-import-phone-call").on("click", function() {
		frappe.call({
			method: "kisanmitra_erpnext.api.phone_call_outer",
		}).done((r) => {
		}).fail((r)=>{
			console.log(r);
		});
	})
}

function import_vikarabad(frm) {
	var wrapper = $(frm.fields_dict["import_vikarabad_button"].wrapper);
	wrapper.find(".btn-import-vikarabad").on("click", function() {
		frappe.call({
			method: "kisanmitra_erpnext.api.vikarabad_outer",
		}).done((r) => {
		}).fail((r)=>{
			console.log(r);
		});
	})
}

function import_adilabad(frm) {
	var wrapper = $(frm.fields_dict["import_adilabad_button"].wrapper);
	wrapper.find(".btn-import-adilabad").on("click", function() {
		frappe.call({
			method: "kisanmitra_erpnext.api.adilabad_outer",
		}).done((r) => {
		}).fail((r)=>{
			console.log(r);
		});
	})
}

function delete_data(frm) {
	var wrapper = $(frm.fields_dict["delete"].wrapper);
	wrapper.find(".btn-delete").on("click", function() {
		frappe.call({
			method: "kisanmitra_erpnext.api.delete_data",
		}).done((r) => {
		}).fail((r)=>{
			console.log(r);
		});
	})
}