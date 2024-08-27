# Ticket-Sales-and-Seating-Arrangement-System

This Python program is a console-based ticket sales and seating arrangement system. It allows users to manage ticket sales for an event, with a focus on seating arrangement. The program ensures that disabled clients are given preferential seating and arranges clients based on their height for optimal seating.

# Features
Date Management: Input and validation of start and end dates for ticket sales.
Seating Configuration: Allows the user to specify the number of rows and seats per row.
Client Information Input: Collects client details, including name, height, and whether they are disabled.
Ticket Number Generation: Generates unique ticket numbers for each client.
Seating Arrangement: Arranges clients with a focus on accessibility for disabled clients and optimal height arrangement.
Ticket Cancellation: Allows cancellation of tickets by client name.
Display Options: Visualize seating arrangements, including the current state of seat occupancy and ticket numbers.
Sales Reporting: Generates a report on all sales, including details of each client and their seat assignment.

# Requirements
Python 3.x
No external libraries are required.

# Usage
1.Run the program:

ticket_sales.py

2.Follow the prompts:

Enter the start and end dates for ticket sales.
Input the number of rows and seats per row.
Use the menu options to sell tickets, cancel tickets, view seating charts, or generate sales reports.

3.Menu Options:

1: Sell a ticket.
2: Cancel a ticket.
3: View the seating chart.
4: View seating chart with ticket numbers.
5: Generate a sales report.
6: Exit the program.

# Example Output
Seating Chart: Displays the seating arrangement with client initials, height, and sale number.
Sales Report: Lists all sales, including client name, ticket number, height, row, and seat number.

# Notes
The program handles date and input validation to ensure correctness.
Disabled clients are given seats near the aisles.
Clients are sorted by height for optimal visibility.
