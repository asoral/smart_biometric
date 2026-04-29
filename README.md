# Smart Biometric

A Frappe application designed for seamless biometric device integration and attendance synchronization.

## Purpose

The **Smart Biometric** app automates the process of fetching attendance data from biometric devices and syncing it with the Employee Checkin system in Frappe/ERPNext. It provides robust error handling and automated maintenance to ensure reliable attendance tracking.

## Key Features

- **Biometric Device Integration**: Connect and synchronize data from various biometric attendance systems.
- **Biometric Error Log**: Detailed logging of synchronization attempts, errors, and tracebacks for easy troubleshooting.
- **Automated Log Maintenance**: Built-in integration with Frappe's **Log Settings** to automatically clear biometric error logs after 7 days, preventing database bloat.
- **Employee Checkin Mapping**: Seamlessly maps biometric records to Frappe Employee Checkin records.

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/Satish/smart_biometric --branch version-16
bench install-app smart_biometric
```

## Maintenance & Logs

This app automatically adds a rule to **Log Settings** upon installation/migration to clear the `Biometric Error Log` every **7 days**. You can adjust this duration in the **Log Settings** desk page.

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/smart_biometric
pre-commit install
```

## License

MIT
