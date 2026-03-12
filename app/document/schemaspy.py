import streamlit as st
st.subheader("Generate with SchemaSpy")
# import time
# import schedule
# pip install schedule
# Then, schedule your download task:

#     # Function to download files


# def scheduled_download():
#     url = "https://example.com/file.pdf"
#     save_path = "file.pdf"
#     download_file(url, save_path)


# # Schedule the task to run every day at 2:00 AM
# schedule.every().day.at("02:00").do(scheduled_download)
# # Keep the script running to check for pending tasks
# while True:
#     schedule.run_pending()
#     time.sleep(60)  # Check every 60 seconds

# opção 2 

#from apscheduler.schedulers.background import BackgroundScheduler

#def my_task():
#    print("Task executed!")

#scheduler = BackgroundScheduler()
# Schedule task with a cron-style expression (e.g., every weekday at 1:31 AM)
#scheduler.add_job(my_task, 'cron', day_of_week='mon-fri', hour='1', minute='31')
#scheduler.start()

