# Database Systems Project

## Info

## System Design

For simplicity of setup/build, we are using SQLite, since it works nicely ootb with no setup outside of Python script.

## Quick Start

This section explains how to operate the project. See [Setup](#Setup) and [Running the Project](#Running-the-Project) for how to build and run the application for the first time.

### The Home Page

The home page is where all of the action begins. From you you can navigate to any of the submenus and modals detailed below.

### Search Books

One of the key features of the application is to all librarians to find and locate books to be checked in/out and managed. 

Search provides a text input and a data table to list books based on your queries.

Through the Search Books page you can:
- search for any book by isbn, book title or author name,
- filter your searches to a subset of the above fields, or by selecting whether you would like to see all books, or just those that are either available or unavailable (checked out). This can be accessed by pressing the Filter button in the top right corner and making the appropriate selections.

After searching for a desired book, the table should populate with a list of suggested titles based on your query. From left to right it shows the books ISBN, title, a list of authors, and its current status (available or unavailable). If it is unavailable, it will also show the corresponding borrower's id next to the status.

When you find a book you are interested in, click on it and you will be greeted by the book detail modal. This view allows you to view some basic information about the text as well as perform some actions.

Try selecting one of the author tiles and you will see that it repopulates the search with a query for books matching this authors name. 

Navigating to the Manage tab of the Book Details modal you can see an option to checkin or checkout the selected book. This view is dynamic depending on the status of the selected book. After a successful check-out, you can now navigate back to the book detail page and see that this book is now associate with a borrower.

To see a full history of the books checkins and checkouts, navigate to the Checkout History tab and browse the table.

Press Close to return to the search view.

When you are done with the Search Books page, press the back button in the top right corner to navigate backwards to the home page.

### Search Borrowers

Seaching of borrowers is very similar to the Search Books page.

Upon searching for a book you will see the table populate with the Borrower's Card ID, their name, followed by a number of checkouts and any built up fines. Keep in mind that these fines include the total fines across both existing and estimated fines for books that are overdue but still not checked in.

Click on the a borrower to view their details in full.

The info card is fairly standard, but navigating to the Manage tab we can see some useful information. If the borrower has no books actively checked out and no pending fines, we see a simple text label with the appropriate description. Otherwise, if a borrower has books actively checked out we see a selection list with the ISBNs and titles of the books they have checked out. From here you can make a selection or more, press Check-in and the books will be returned to the library.

Below this Active Checkouts section we can see some information on the users fines. We see the amount incurred per book as well as a total below of what needs to be paid. When a borrower has returned all of their overdue books, and they make a payment, press the Pay button to resolve these fines.

For a detailed breakdown of the rules for books and fines, see the system design section of this readme.

Lastly, the Checkout History has the same layout of that in the Search Books detail modal, except it filters checkout history by borrower ID, not book.

Again, press Close and then Back to return to the home page.

### Create Borrowers

Create Borrower allows you to enter in a borrower's information and register them with the library. It's functionality is very straight-forward, so we won't dive any deeper.

See the system design section of this readme for a breakdown of the rules in creating a new borrower.

### Settings

Within this settings modal there are a few advanced options that administrators can take advantage of such as: 
- Change the active database by typing in a new filename in the prompt and pressing "change".
- Initialize an existing but un-initialized database. This is relevant mainly only after you have changed the database name from the option listed above.
- Re-Initialize the current database. This will delete any created data and start fresh (after re-loading the initial migration data first).
- Reset the time feature. This is important when testing data with the "time-travel" menu testing item. It allows you to undo the 'go forward in time and set the simulated date to today'.
- And lastly, "Load Extra Data" which is helpful for testing/learning purposes to load in a selection of random example loan data into the application.

### Time Travel

Time Travel is a neat little feature that is handy in testing and learning about this tool before working with real-world data. It allows you to have the functionality to create loans between borrowers and then simulate the passage of time so that you can see the result of fines (for example). Click on the button and navigate forward in time. Once you pick a date you like, select it by pressing Confirm or cancel with Cancel. 

Note: you cannot move backwards in time after you have set a new date for 'today', although you can navigate forwards and backwards when selecting in the menu so long as you do not try and move back before 'todays' date. This sounds like a complex operation, but after playing around with it for a moment it should make sense. 

To reset the date to the real date, see the setting modal. Keep in mind again, this tool is only for demo and testing/learning purposes and would be removed in a production-ready system.

### Quit

Quit, as you might expect, shows a pop-up modal to close the application and leave. After pressing this, all data is saved from your current session.

## Setup

### Python Version

Ensure you are using at minimum python version 3.12.

This is the most widely-adopted of the recent python version. It has some nice features that make writing this code much better.

``` bash
python3 --version
```

### Dependencies

It is recommended that you use a virtual environment before continuing. This project was built using `uv` as it handles most of the annoying project config, but any venv will work.

You can [install uv here](https://docs.astral.sh/uv/getting-started/installation/).

To setup a venv with `uv`:

``` bash
uv venv
```

Remember to activate the venv afterwards using the command it spits back at you. On Linux this is simply:

``` bash
source .venv/bin/active
```

Install the project requirements:

``` bash
uv pip install -r requirements.txt
```

And you are ready to go.

## Running the Project

### First Run

Upon the first run of the project, a database must be created and initialized. When you first launch you will see a dialog prompting you to create a new database or quit the app. Pressing initialize will initialize the database and insert the migrated data into the system automatically.

### Normal Operation

Start the app with:

``` bash
uv run textual run src/app.py
```

If the textual command isn't found, just run it as a normal python file (not recommended).

``` bash
python3 src/app.py
```

It should open up a GUI/TUI in your terminal. To run it in the brower:

``` bash
uv run textual serve src/app.py
```

and open the corresponding port in your browser.

### Resetting Progress

To start with a fresh database, run the app and find the settings menu.

From here you can re-init the database, or optionally pass a new filename and initialize it.

NOTE: initializing the database loads in all of the given test data that is extracted from the csv files in `/data`.

WARNING: re-init removes all progress from created borrowers, checkouts, fines, etc. and just starts fresh with the given data.
