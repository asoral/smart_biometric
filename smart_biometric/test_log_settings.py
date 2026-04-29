import frappe

def run():
	frappe.connect()
	site = "newtek.dexciss.tech"
	frappe.init(site=site)
	frappe.connect()
	
	print(f"Checking Log Settings for site {site}")
	log_settings = frappe.get_doc("Log Settings")
	
	found = False
	for log in log_settings.logs_to_clear:
		print(f"Found: {log.ref_doctype}")
		if log.ref_doctype == "Biometric Error Log":
			found = True
	
	if not found:
		print("Biometric Error Log NOT found. Adding...")
		log_settings.append("logs_to_clear", {
			"ref_doctype": "Biometric Error Log",
			"days": 7
		})
		log_settings.save(ignore_permissions=True)
		frappe.db.commit()
		print("Added and committed.")
	else:
		print("Biometric Error Log already exists.")

if __name__ == "__main__":
	run()
