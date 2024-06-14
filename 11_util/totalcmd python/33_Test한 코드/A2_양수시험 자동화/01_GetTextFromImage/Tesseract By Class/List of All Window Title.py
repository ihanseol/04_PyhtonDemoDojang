# import psutil
#
# def get_window_titles():
#     window_titles = []
#     for proc in psutil.process_iter(['pid', 'name']):
#         try:
#             # Fetch process details
#             proc_info = proc.as_dict(attrs=['pid', 'name'])
#             pid = proc_info['pid']
#             name = proc_info['name']
#             # Get the process's window
#             try:
#                 # Get the process's window
#                 window = psutil.Process(pid).exe()
#                 # Get the title of the window
#                 title = psutil.Process(pid).name()
#                 window_titles.append(title)
#             except psutil.NoSuchProcess:
#                 continue
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return window_titles
#
# # Get the list of window titles
# titles = get_window_titles()
# print(titles)


import pygetwindow as gw

def get_window_titles():
    window_titles = []
    for window in gw.getAllTitles():
        window_titles.append(window)
    return window_titles

# Get the list of window titles
titles = get_window_titles()
print(titles)
