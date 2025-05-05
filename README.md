
# Donate Tech - Web Application

**Developer**: ricardo-str

## Requirements

- Python 3.x must be installed on your system.

## Installation

1. Download this project to your local device.
2. Install the dependencies from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```


**Note**: Sometimes, the required dependencies in `requirements.txt` may not install correctly, so you may need to install them manually.

## Running the Application

To run the application, execute the following command:

```bash
python app.py
```

## Project Structure

```
database/
│         
├── db.py
├── region-comuna.sql
├── sentencias.sql
├── tarea2.sql          
static/
├── css/
├── js/
├── media/ 
├── uploads/            
templates/
├── agregar-donacion.html
├── index.html 
├── informacion-dispositivo.html 
├── ver-dispositivos.html
├── menu.html
├── stats.html
├── stats2.html 
utils/            
├── validations.py  
app.py
README.md   
requirements.txt  
```

## Database Setup

This project includes three SQL files. To store the data using MySQL, follow these steps:

1. Run the `tarea2.sql` script to create the necessary database schema and tables for storing information.
2. Next, run the `region-comuna.sql` script to insert the regions and their respective communes into the corresponding table.
3. Finally, execute the `sentencias.sql` script to create a user and grant the required privileges/permissions for the application to function correctly.

Additionally, the project uses a `sentencias.json` file, which contains the queries for inserting and retrieving the required data.

Lastly, `db.py` is included to handle the database connection and execute queries defined in `sentencias.json`.

## Validation

The project performs **frontend validations** using JavaScript, as in Task 1. Additionally, a new file `validations.py` has been created to perform **backend validations** for each input, including sanitizing text inputs to prevent XSS attacks.

Both frontend (JavaScript) and backend validations are applied to the comments section for devices.

## Fixes

This version includes fixes for issues that were present in the previous submission:

- **Multiple Device Insertions**: Previously, when trying to add two or more devices in the donation form, only the first one would be inserted. Now, multiple devices can be added simultaneously without issues.

- **File Size Limitation**: In the previous version, there was no mechanism to limit the maximum file size, which could be risky. This has been addressed using the `MAX_CONTENT_LENGTH` setting in `app.py`.

- **PDF File Restrictions**: PDF files were being accepted when they shouldn't have been. Now, when attempting to select a `.pdf` file, the donation form submission is blocked.

## Task 3 Features

- **Comments**: A new form has been added to the 'informacion-dispositivo' URL, allowing users to submit comments (name and text). If validation fails, the user is informed, and the form remains visible for corrections.

   Comments for each device can also be viewed on the same page, showing the commenter's name, text, and submission date.

- **Charts**: A new option has been added to the main menu, where users can access a page containing two different charts: *Device Types* and *Contacts by Commune*. These charts were implemented using AJAX and Highcharts.
