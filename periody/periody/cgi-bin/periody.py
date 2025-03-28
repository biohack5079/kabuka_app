#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import cgi  # Import the cgi module
import cgitb  # Import the cgitb module for debugging
import os  # Import the os module for file operations
import time  # Import the time module

cgitb.enable()  # Enable CGI traceback for debugging

form = cgi.FieldStorage()  # Get form data
personal_name = form.getvalue('personal_name')  # Get the value of 'personal_name'
email = form.getvalue('email')  # Get the value of 'email'
contents = form.getvalue('contents')  # Get the value of 'contents'
action = form.getvalue('action')  # Get the value of 'action'
post_id = form.getvalue('post_id')  # Get the value of 'post_id'

bbs_file = '../bbs.txt'  # Define the file path for the bulletin board

# Get the IP address of the user
ip_address = os.environ.get('REMOTE_ADDR', '0.0.0.0')  # Get the IP address of the user

def read_data():
    if not os.path.exists(bbs_file):  # Check if the file exists
        return []  # Return an empty list if the file does not exist
    with open(bbs_file, 'r', encoding='utf-8') as f:  # Open the file in read mode
        return f.readlines()  # Return the lines of the file

def write_data(data):
    with open(bbs_file, 'a', encoding='utf-8') as f:  # Open the file in append mode
        f.write(data)  # Write data to the file

def delete_post(post_id, ip_address=None):
    lines = read_data()  # Read the data from the file
    with open(bbs_file, 'w', encoding='utf-8') as f:  # Open the file in write mode
        inside_post = False  # Initialize a flag to track if inside a post
        for line in lines:  # Iterate through each line
            if f'id="{post_id}"' in line and (ip_address is None or f'ip="{ip_address}"' in line):  # Check if the line contains the post ID and optionally IP address
                inside_post = True  # Set the flag to True
            elif inside_post and line.strip() == "</div>":  # Check if the end of the post is reached
                inside_post = False  # Set the flag to False
            elif not inside_post:  # If not inside the post
                f.write(line)  # Write the line to the file

def report_post(post_id):
    time.sleep(10)  # Wait for 10 seconds
    delete_post(post_id)  # Delete the post

print("Content-Type: text/html\n")  # Print the content type header
print("""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>Investment Bulletin Board "PERIODY"</title>
<meta charset="utf-8">
<meta name="description" content="">
<meta name="author" content="">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="">
<style>
    input[type="text"], input[type="email"], textarea {
        width: 100%;  /* Set width to 100% */
        padding: 10px;  /* Set padding */
        margin-bottom: 10px;  /* Set bottom margin */
        border: 1px solid #ccc;  /* Set border */
        border-radius: 4px;  /* Set border radius */
        box-sizing: border-box;  /* Set box-sizing to border-box */
    }
    @media (max-width: 600px) {
        input[type="text"], input[type="email"], textarea {
            padding: 8px;  /* Set padding for small screens */
        }
    }
</style>
</head>
<body>
<p>Investment Bulletin Board "PERIODY"</p>
<form method="POST" action="periody.py">
    <input type="text" name="personal_name" placeholder="Name"><br><br>
    <input type="email" name="email" placeholder="Email (optional)"><br><br>
    <textarea name="contents" rows="8" cols="40" placeholder="Content"></textarea><br><br>
    <input type="submit" name="action" value="Post">
</form>
""")

if action == "Post" and personal_name and contents:
    post_id = str(int(time.time()))  # Generate a post ID based on the current time
    email_link = f'<a href="mailto:{email}">{email}</a>' if email else '(No email address)'  # Create an email link if email is provided
    contents = contents.replace("\n", "<br>")  # Replace newlines with <br> tags
    data = f'<div id="{post_id}" ip="{ip_address}"><hr>\n<p>Poster: {personal_name} {email_link}</p>\n<p>Content:</p>\n<p>{contents}</p>\n'  # Format the post data with IP address
    data += f'<form method="POST" action="periody.py"><input type="hidden" name="post_id" value="{post_id}">'  # Add hidden input for post ID
    data += f'<input type="submit" name="action" value="Delete"><input type="submit" name="action" value="Report"></form></div>\n'  # Add delete and report buttons
    write_data(data)  # Write the post data to the file

if action == "Delete" and post_id:
    delete_post(post_id, ip_address)  # Delete the post if action is "Delete" and IP address matches

if action == "Report" and post_id:
    print("<p>Reporting post...</p>")  # Inform the user that the post is being reported
    print("<script>setTimeout(function() { window.location.reload(); }, 10000);</script>")  # Reload the page after 10 seconds without responding during this period
    report_post(post_id)  # Report and delete the post after waiting for 10 seconds

for line in read_data():  # Read and print each line from the file
    print(line)

print("""
</body>
</html>
""")

