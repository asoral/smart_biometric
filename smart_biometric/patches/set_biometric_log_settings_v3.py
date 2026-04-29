import frappe

def execute():
	frappe.clear_cache(doctype="Log Settings")
	
	log_settings = frappe.get_doc("Log Settings")
	
	# Check if it already exists
	exists = False
	for log in log_settings.get("logs_to_clear"):
		if log.ref_doctype == "Biometric Error Log":
			log.days = 7
			exists = True
			break
	
	if not exists:
		log_settings.append("logs_to_clear", {
			"ref_doctype": "Biometric Error Log",
			"days": 7
		})
	
	log_settings.save(ignore_permissions=True)
	frappe.db.commit()
	
	# Verify
	frappe.clear_cache(doctype="Log Settings")
	updated = frappe.get_doc("Log Settings")
	found = any(l.ref_doctype == "Biometric Error Log" for l in updated.logs_to_clear)
	
	if not found:
		# Fallback: Direct SQL insertion
		name = frappe.generate_hash(length=10)
		frappe.db.sql("""
			INSERT INTO `tabLogs To Clear` 
			(name, owner, creation, modified, modified_by, parent, parentfield, parenttype, ref_doctype, days, idx)
			VALUES (%s, 'Administrator', NOW(), NOW(), 'Administrator', 'Log Settings', 'logs_to_clear', 'Log Settings', 'Biometric Error Log', 7, 
			(SELECT IFNULL(MAX(idx), 0) + 1 FROM `tabLogs To Clear` AS t WHERE parent='Log Settings'))
		""", (name,))
		frappe.db.commit()
		frappe.clear_cache(doctype="Log Settings")
