# availa-buddy

As a professional, and parent, I find that my time faces ever competing interests. To help with that I created a simple little python project to help keep track of the many calendars I use between by family, and work. It uses the 'icalBuddy' command line utility to fetch event or availability information from the user's calendars in the calendar app and outputs it in a neatly formatted list. Out can be either your upcoming events for x days, or weekday availability for x days. Output is grouped by day. Availa-buddy checks all local and account synced calendars set up on your mac.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

* Python 3.x
* Homebrew
* icalBuddy

### Installing

To install availa-buddy:

1. Clone the repo:
```bash
git clone https://github.com/usmc0341/avail-buddy.git
```

2. Install icalBuddy (if on a Mac):
```bash
brew install ical-buddy
```

## Running the Script

How to run the script:

```bash
python3 availa_buddy.py
```

## Usage Examples

After running the script, you will be prompted to choose a forecast window and an action. 

Example 1: 

```text
Check schedule for the next how many days? [1-90] 3
What would you like to see?
1. See availability for the next 7 days. 
2. See scheduled items for the next 7 days. 1
```

This example will show your availability for the next 3 days.
```markdown
Availability for 06/07/2023:
    Available: 08:00:00 - 11:45:00
    Available: 12:00:00 - 12:30:00
    Available: 13:30:00 - 15:30:00
    Available: 17:00:00 - 19:30:00
Availability for 06/08/2023:
    Available: 08:00:00 - 09:00:00
    Available: 10:00:00 - 11:00:00
    Available: 13:00:00 - 15:00:00
    Available: 15:30:00 - 16:00:00
    Available: 17:00:00 - 19:30:00
Availability for 06/09/2023:
    Available: 09:00:00 - 09:15:00
    Available: 09:30:00 - 11:30:00
    Available: 13:00:00 - 15:00:00
    Available: 15:50:00 - 16:00:00
    Available: 17:00:00 - 18:30:00
```

Example 2:

```text
Check schedule for the next how many days? [1-90] 3
What would you like to see?
1. See availability for the next 3 days. 
2. See scheduled items for the next 3 days. 2
```

This example will show your scheduled items for the next 3 days.

```markdown
 Jun 21, 2023:
 ------------------------
 • Event 1 >> 12:30 PM - 1:30 PM
 • Event 2 >> 2:00 PM - 2:30 PM
 • Event 3 >> 3:30 PM - 4:00 PM

 
 Jun 22, 2023:
 ------------------------
 • Event 1 >> 9:00 AM - 10:00 AM
 • Event 2 >> 9:00 AM - 10:30 AM
 • Event 3 >> 4:00 PM - 4:30 PM
 • Event 4 >> 4:30 PM - 5:00 PM
 • Event 5 >> 7:30 PM - 8:00 PM
 
 Jun 23, 2023:
 ------------------------
 • Event 1 >> 8:00 AM - 9:00 AM
 • Event 2 >> 9:15 AM - 9:30 AM
 • Event 3 >> 11:30 AM - 12:00 PM
 • Event 4 >> 6:30 PM - 7:30 PM
 • Event 5 >> 7:30 PM - 8:00 PM
```

## Author

* **Ryan McDonald** - [usmc0341](https://github.com/usmc0341)


# License

This project is licensed under the MIT License.

```markdown
MIT License

Copyright (c) 2023 Ryan McDonald

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

