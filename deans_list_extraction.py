"""
This script sends a request to the Saint Louis University Dean's List webpage
and parses the response to gather each student's name and major.
The data is then written into a CSV file with each row representing a student
and two columns for their name and major.

A total of 2,360 students are gathered from this method.
"""


import requests
from bs4 import BeautifulSoup

# URL for Dean's List Webpage
# Replace "***" with your university's url name
url = 'https://www.***.edu/services/emis/apps/deans_list/listing.php?term=202220'

# List of all schools to input into search bar of deans list
schools = ['BA','PL','AS','AH','PK','PH','PS','LP','NR']

# Create CSV file 
with open("deans_list_students.csv", "a") as csvFile:

	# Loop through each school
	for i in schools:
		# Parameters to submit with POST request
		PARAMS = {'college':i, 'submit':'Submit'} 
		response = requests.post(url, PARAMS)
		soup = BeautifulSoup(response.content, "html.parser")
		
		# Parse the "table" tag
		bodyCopy = soup.find("table")
		# Make each row of the table (each student) an element in a list
		students = bodyCopy.findAll("tr")
		# Remove the first element. These are headers for the table.
		students.pop(0)

		# Loop through each student in the school
		for student in students:
			# Create a list containing the student's name and major
			student_Name_and_Major = student.findAll('td')
			name = student_Name_and_Major[0].text
			major = student_Name_and_Major[1].text

			# Format Name: Given as "LastName, FirstName MiddleInitial". Want as "FirstName LastName"
			name = name.replace(",", "").split(" ")
			name = name[1] + " " + name[0]

			# Write data to CSV file
			# Each row is a student
			# Columns are "Name" and "Major"
			csvFile.write(name + "," + major + "\n")
