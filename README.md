# Country Comparison Tool

A retro-style web application that allows users to compare countries based on population and area, using a classic Apple System OS interface. The tool finds the top 3 countries closest to user-defined population and area values.


## Features

- **Retro Interface**: Styled using [System.css](https://github.com/sakofchit/system.css) to mimic the classic Apple System OS look.
- **Population and Area Comparison**: Input target population and area to find the top 3 countries closest to those values.
- **Responsive Design**: Adjusts to various screen sizes for usability on different devices.
- **Cached Data**: Utilizes a local CSV file to cache country data and reduce API calls.
- **User-Friendly Input**: Dropdown menus for unit selection to simplify user input.

## Demo

![2024-10-29 13 57 07](https://github.com/user-attachments/assets/2fd8385c-3597-44ac-bdc7-bc666a006e8f)

## Prerequisites

- Python 3.6 or higher
- `pip` package manager

## Installation

1. **Clone the Repository**

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   *If `requirements.txt` is not present, install the packages manually:*

   ```bash
   pip install flask requests
   ```

5. **Ensure the Project Structure**

   ```
   country-comparison-tool/
   ├── app.py
   ├── countries_data.csv      # Will be created after running the app
   ├── requirements.txt
   └── templates/
       ├── static/
       │   └── styles.css
       ├── index.html
       ├── results.html
       ├── documentation.html
       └── about.html
   ```

## Project Structure

- **app.py**: Main Flask application file containing routes and logic.
- **countries_data.csv**: Local cache of country data fetched from the Rest Countries API.
- **static/**: Directory containing static files like `styles.css`.
- **templates/**: Directory containing HTML templates.
  - **index.html**: Home page with input form.
  - **results.html**: Page displaying comparison results.
  - **documentation.html**: Application documentation page.
  - **about.html**: Information about the application and developer.

## Usage

1. **Run the Application**

   ```bash
   python app.py
   ```

2. **Access the Application**

   Open your best **online web browser tool** and navigate to `http://127.0.0.1:5000/`.

3. **Use the Tool**

   - **Home Page**: Enter the target population and/or area.
     - Input the numerical value.
     - Select the unit from the dropdown (Units, Thousands, Millions, Billions).
   - **Results Page**: View the top 3 countries closest to your inputs.
   - **Navigation**: Use the menu bar to access Documentation and About pages.

## Deployment

To implement this application on your own website, follow these steps:

### Option 1: Deploying on a Server (Self-Hosted)

1. **Prepare the Server**

   - Ensure Python 3.6 or higher is installed.
   - Install a web server (e.g., Nginx, Apache).

2. **Install a WSGI Server**

   - Install Gunicorn or uWSGI to serve the Flask application.

     ```bash
     pip install gunicorn
     ```

3. **Configure the Web Server**

   - Set up Nginx or Apache to proxy requests to the WSGI server.

   - **Example Nginx Configuration:**

     ```nginx
     server {
         listen 80;
         server_name yourdomain.com;

         location / {
             proxy_pass http://127.0.0.1:8000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
         }
     }
     ```

4. **Run the Application with Gunicorn**

   ```bash
   gunicorn --bind 127.0.0.1:8000 wsgi:app
   ```

   *Create a `wsgi.py` file if needed:*

   ```python
   from app import app

   if __name__ == "__main__":
       app.run()
   ```

5. **Set Up as a Service**

   - Use systemd or another init system to run Gunicorn as a service.

6. **Ensure Security**

   - Use HTTPS by obtaining an SSL certificate (e.g., via Let's Encrypt).

### Option 2: Deploying on a Cloud Platform

1. **Heroku**

   - **Create a `Procfile`:**

     ```
     web: gunicorn app:app
     ```

   - **Create a `requirements.txt`:**

     ```txt
     flask
     requests
     gunicorn
     ```

   - **Push to Heroku:**

     ```bash
     heroku create
     git push heroku main
     ```

2. **AWS Elastic Beanstalk**

   - Package your application and deploy using the AWS Elastic Beanstalk console.

3. **Google App Engine**

   - **Create an `app.yaml`:**

     ```yaml
     runtime: python
     entrypoint: gunicorn -b :$PORT app:app
     ```

   - Deploy using the `gcloud` command-line tool.

## Customization

- **Styling**

  - Modify `styles.css` to customize the appearance.
  - Update HTML templates in the `templates/` directory.

- **Content**

  - Edit `documentation.html` and `about.html` to include relevant information.
  - Update navigation links and menu items as needed.

- **Functionality**

  - Add new features by modifying `app.py` and corresponding templates.
  - Ensure that any additional dependencies are added to `requirements.txt`.

## Technologies Used

- **Python 3**: Core programming language.
- **Flask**: Web framework for handling routes and server logic.
- **Requests**: Library to handle HTTP requests to the Rest Countries API.
- **System.css**: CSS framework for retro Apple System OS styling.
- **HTML/CSS**: Front-end structure and styling.
- **CSV**: Data caching for country information.

## Acknowledgments

- **[System.css](https://github.com/sakofchit/system.css)**: For providing the retro CSS framework.
- **[Rest Countries API](https://restcountries.com/)**: For country data used in the application.
- **[Flask](https://flask.palletsprojects.com/)**: For the web framework.

## License

This project is licensed under no license, do what you want for the love of god, I'm not going to tell you what you have to do and what you don't have to do à la fin.
