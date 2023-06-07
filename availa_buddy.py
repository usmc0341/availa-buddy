#!/usr/bin/env 
"""
Service: availa_buddy
Version: 1.0.0
Author: Ryan McDonald
Date: June 7, 2023
Python version: 3.11.3
icalBuddy version: 1.10.1
Description: This script checks user's availability and scheduled events for 
            the current day and a user defined number of days after
            It uses the MacOs 'icalBuddy' command line utility to fetch this 
            information from the user's apple calendar.app.
"""

from subprocess import check_output as icalBuddy
from subprocess import CalledProcessError
import re
from datetime import datetime, timedelta, date
import logging

logging.basicConfig(level=logging.INFO)
DEBUG = False

def preflight():
    """
    Checks brew for the ical-buddy(icalBuddy) command line utility.
    
    Returns:
        If ical-buddy is not installed, it instructs user to install it.
    """
    buddy_check = icalBuddy("brew list | grep ical-buddy", shell=True, text=True)
    if buddy_check == "ical-buddy\n":
        return
    else:
        # You gotta have your buddy!
        print("Your buddy is missing! You can install ical-buddy by running: ")
        print("brew install ical-buddy")
        exit()


def user_choice(forecast):
    """
    Prompts the user to enter a choice and validates the input.
    
    The user must enter either 1 or 2. If the input is invalid (not a number or
    a number other than 1 or 2), the function will continue to prompt the user
    until a valid input is received.
    
    Returns:
        int: The user's choice (either 1 or 2).
    """
    while True:  # Continue prompting until a valid input is received
        try:
            # Prompt the user for their choice
            print("What would you like to see?")
            choice = int(input(f"1. See availability for the next {forecast} days. \n2. See scheduled items for the next {forecast} days.  "))
            # If the input is not 1 or 2, display an error message
            if choice not in [1, 2]:
                print("Invalid input. Please enter 1 or 2.")
                continue  # Skip the rest of the loop and start the next iteration
        except ValueError:  # Raised if the input cannot be converted to an integer
            print("Invalid input. Please enter a number.")
            continue  # Skip the rest of the loop and start the next iteration
        break  # If we've gotten this far, the input is valid, so we can break the loop
    return choice


def forecast_window():
    """
    Prompts the user to enter a choice and validates the input.
    
    The user must enter either 1 or 2. If the input is invalid (not a number or
    a number other than 1 or 2), the function will continue to prompt the user
    until a valid input is received.
    
    Returns:
        int: Number of days to forecast (between 1 and 90).
    """
    days = int(input("Check schedule for the next how many days? [1-90] "))
    while True:  # Continue prompting until a valid input is received
        try:
            if days not in range(1, 91):
                # Prompt the user for their range
                print("Invalid input. Please enter a number between 1 or 90.")
                continue  # Skip the rest of the loop and start the next iteration
        except ValueError:  # Raised if the input cannot be converted to an integer
            print("Invalid input, must be integer. Please enter a number between 1 or 90")
            continue  # Skip the rest of the loop and start the next iteration
        break
    return days


def convert_to_date(event_date):
    """
    Convert a date string into a date object.

    Args:
        event_date (str): String representing a date.

    Returns:
        date: Date object corresponding to the input string.
    """
    if event_date == "today":
        return date.today()
    elif event_date == "tomorrow":
        return date.today() + timedelta(days=1)
    elif event_date == "day after tomorrow":
        return date.today() + timedelta(days=2)
    else:
        return datetime.strptime(event_date, "%b %d, %Y").date()


def process_availability(input_lines):
    """
    Process the availability from the icalBuddy output lines.

    Args:
        input_lines (list): Lines of output from icalBuddy command.
    """
    event_pattern = r'\s+(.+?) at (\d{1,2}:\d{2} [AP]M) - (\d{1,2}:\d{2} [AP]M)'
    # title_pattern = r'.\s(.+)'
    busy_slots = []
    current_day = ""

    
    if DEBUG:
        for event_title in input_lines[::2]:
            title = event_title
            logging.debug(title)

    for event_line in input_lines[1::2]:
        match = re.match(event_pattern, event_line)
        if DEBUG:
            logging.debug(f"line1: {event_line}")
            logging.debug(f"match1: {match.group(1)}")

        if match:
            event_date = convert_to_date(match.group(1).strip())
            event_start_time = datetime.strptime(match.group(2), "%I:%M %p").time()
            event_end_time = datetime.strptime(match.group(3), "%I:%M %p").time()

            if DEBUG:
                logging.debug(f"Matched line: {event_line.strip()}")
                logging.debug(f"Extracted details: {event_title}, {event_date}, {event_start_time}, {event_end_time}")

            if event_date != current_day:
                if current_day and busy_slots:
                    print_availability(current_day, busy_slots)

                current_day = event_date
                busy_slots = []

            if event_date.weekday() < 5:
                busy_slots.append((event_start_time, event_end_time))

    if current_day and busy_slots:
        print_availability(current_day, busy_slots)


def print_availability(day, busy_slots, start_of_day="8:00 AM", end_of_day="5:00 PM"):
    """
    Prints the availability for a specific day.

    Args:
    day (str): Day for which to print availability.
    busy_slots (list): List of tuples representing busy timeslots.
    start_of_day (str): String representing the start of the day.
    end_of_day (str): String representing the end of the day.
    """
    print(f"Availability for {day.strftime('%m/%d/%Y')}:")
    available_start_time = datetime.strptime(start_of_day, "%I:%M %p").time()
    end_of_day = datetime.strptime(end_of_day, "%I:%M %p").time()
    
    for busy_slot in sorted(busy_slots):
        if available_start_time < busy_slot[0]:
            print(f"    Available: {available_start_time} - {busy_slot[0]}")

        available_start_time = max(available_start_time, busy_slot[1])

    if available_start_time < end_of_day:
        print(f"    Available: {available_start_time} - {end_of_day}")

def availability(forecast):
    """
    Fetches and returns the user's availability for the forecasted number of days.
    
    Args:
        forecast_window (int): Number of days to fetch the availability for.

    Returns:
        str: Output of the icalBuddy command containing the user's availability.
    """
    try:
        command = f"icalBuddy -npn -nc -iep 'title,datetime' eventsToday+{forecast}"
        output = icalBuddy(command, shell=True, text=True)
        logging.debug(output)
        return output
    except CalledProcessError as e:
        logging.error(f'Error executing command {command}. Details: {str(e)}')
        return

def obligations(forecast):
    """
    Fetches and prints the user's scheduled events for the forecasted number of days.
    
    Args:
        forecast_window (int): Number of days to fetch the events for.
    """
    try:
        command = f"icalBuddy -npn -nc -f -sd -ps '/ >> /' -iep 'title,datetime' eventsToday+{forecast}"
        output = icalBuddy(command, shell=True, text=True)
        logging.info(output)
        return
    except CalledProcessError as e:
        logging.error(f'Error executing command {command}. Details: {str(e)}')
        return


def main():
    # run preflight checks
    preflight()
    # usage
    forecast = forecast_window()
    choice = user_choice(forecast)
    
    if choice == 1:
        input_lines = availability(forecast).splitlines()
        process_availability(input_lines)
        pass
    elif choice == 2:
        obligations(forecast)
        pass

if __name__ == "__main__":
    main()
