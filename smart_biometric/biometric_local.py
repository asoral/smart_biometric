
# import pyodbc
# import requests
# from datetime import datetime
# from apscheduler.schedulers.background import BackgroundScheduler
# import json
# def fetch_and_send_data():
#     print("Trigger -->")
#     DRIVER_NAME = 'SQL Server'
#     SERVER_NAME = 'SERVER-PC\\SQLEXPRESS'  # Double backslash for correct escaping
#     DATABASE_NAME = 'etimetracklite1'
#     UID = 'essl'
#     PWD = 'essl'
#     connection_string = f"""
#         DRIVER={{{DRIVER_NAME}}};
#         SERVER={SERVER_NAME};
#         DATABASE={DATABASE_NAME};
#         UID={UID};
#         PWD={PWD};
#         TRUSTED_CONNECTION=yes;
#     """
#     try:
#         conn = pyodbc.connect(connection_string, autocommit=True)  # Enable autocommit
#         print("Connected to database")
#         cursor = conn.cursor()
#         url = "https://amitalliance.dexciss.tech/api/method/amitalliance.biometric_api.employee_checkin"
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': 'token f806ed19bf7a474:d809d53307ae641'
#         }
#         query = "SELECT EMPCODE, LOGDATE, Deviceid FROM dbo.atten WHERE update_checking IS NULL"
#         print("Executing query:", query)
#         cursor.execute(query)
#         rows = cursor.fetchall()
#         for row in rows:
#             emp_id, punch_time, device_id = row
#             time_str = punch_time.strftime('%Y-%m-%d %H:%M:%S')
#             # **Step 1: First Update UpdateCheckin = 1**
#             update_checkin_query = """
#                 UPDATE dbo.atten 
#                 SET update_checking = 1 
#                 WHERE EMPCODE = ? AND LOGDATE = ?
#             """
#             cursor.execute(update_checkin_query, (emp_id, punch_time))
#             conn.commit()  # Commit after updating `UpdateCheckin`
#             # **Step 2: Send API request**
#             payload = {
#                 "emp_id": emp_id,
#                 "time": time_str,
#                 "device_id": device_id
#             }
#             print("payload-----",payload)
#             response = requests.post(url, headers=headers, json=payload)
#             if response.status_code == 200:
#                 response_data = response.json()
#                 print("Response:", response_data)
#                 # **Step 3: If API response is successful, update EmployeeRecord**
#                 if response_data.get("isSuccess") == 1:
#                     update_employee_record_query = """
#                         UPDATE dbo.atten 
#                         SET employee_checkin = ? 
#                         WHERE EMPCODE = ? AND LOGDATE = ?
#                     """
#                     cursor.execute(update_employee_record_query, (response_data.get('Employee Checkin', ''), emp_id, punch_time))
#                     conn.commit()  # Commit after updating `EmployeeRecord`
#     except pyodbc.Error as db_err:
#         print(f"Database Error: {db_err}")
#     except requests.RequestException as req_err:
#         print(f"API Request Error: {req_err}")
#     except Exception as e:
#         print(f"Unexpected Error: {e}")
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
# # Set up scheduler to run every 5 minutes
# scheduler = BackgroundScheduler()
# scheduler.add_job(fetch_and_send_data, 'interval', minutes=1)
# try:
#     scheduler.start()
#     while True:
#         pass
# except KeyboardInterrupt:
#     scheduler.shutdown()
