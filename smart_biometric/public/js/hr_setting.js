frappe.ui.form.on("HR Settings", {
    allow_geolocation_tracking: function (frm) {
        if (frm.doc.allow_geolocation_tracking) {
            if (frm.doc.custom_latitude <= 0 || frm.doc.custom_longitude <= 0) {
                frm.set_value("allow_geolocation_tracking", 0);
                frappe.throw(__("Please set Latitude and Longitude before enabling Geolocation Tracking."));
            }
        }
    }
});