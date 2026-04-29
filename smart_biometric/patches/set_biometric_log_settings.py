import frappe

def execute():
	log_settings = frappe.get_doc("Log Settings")
	
	# Check if Biometric Error Log is already in logs_to_clear
	found = False
	for log in log_settings.logs_to_clear:
		if log.ref_doctype == "Biometric Error Log":
			log.days = 7
			found = True
			break
	
	if not found:
		log_settings.append("logs_to_clear", {
			"ref_doctype": "Biometric Error Log",
			"days": 7
		})
	
	log_settings.save(ignore_permissions=True)
