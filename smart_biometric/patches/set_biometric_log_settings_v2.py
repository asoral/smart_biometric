import frappe

def execute():
	# Force run by renaming patch or checking again
	log_settings = frappe.get_doc("Log Settings")
	
	# Check if Biometric Error Log is already in logs_to_clear
	existing_doctypes = [log.ref_doctype for log in log_settings.logs_to_clear]
	
	if "Biometric Error Log" not in existing_doctypes:
		log_settings.append("logs_to_clear", {
			"ref_doctype": "Biometric Error Log",
			"days": 7
		})
		log_settings.save(ignore_permissions=True)
		# Force database sync for Single DocType
		frappe.db.commit()
	else:
		# Update days if already exists
		for log in log_settings.logs_to_clear:
			if log.ref_doctype == "Biometric Error Log":
				log.days = 7
		log_settings.save(ignore_permissions=True)
		frappe.db.commit()
