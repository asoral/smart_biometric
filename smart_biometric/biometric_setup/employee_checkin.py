import frappe
from frappe.utils.data import get_datetime

@frappe.whitelist(allow_guest=True)
def employee_checkin(emp_id, time, device_id):
    try:
        if not emp_id or not time or not device_id:
            return {
                "isSuccess": 0,
                "message": "Missing required parameters: emp_id, time, and device_id"
            }

        time = get_datetime(time)

        # Find Employee by biometric ID
        employee = frappe.db.get_value("Employee", {"attendance_device_id": emp_id}, "name")

        if not employee:
            return log_biometric_error(emp_id, time, f"Employee Not Found ({emp_id})")

        emp_doc = frappe.get_doc("Employee", employee)

        if emp_doc.status != "Active":
            return log_biometric_error(emp_id, time, "Employee Is Inactive", employee)

        # Create Checkin
        checkin = frappe.new_doc("Employee Checkin")
        checkin.employee = employee
        checkin.time = time
        checkin.device_id = device_id
        checkin.log_type = "IN"
        checkin.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "isSuccess": 1,
            "message": f"Check-in created for: {employee}",
            "Employee Checkin": checkin.name,
            "Time": str(time)
        }

    except Exception as e:
        return log_biometric_error(emp_id, time, str(e))


def log_biometric_error(emp_id, time, message, employee=None):
    doc = frappe.new_doc("Biometric Error Log")
    doc.biometric_id = emp_id
    doc.time = time
    doc.traceback = message
    if employee:
        doc.employee = employee
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "isSuccess": 0,
        "message": message,
        "Time": str(time)
    }
