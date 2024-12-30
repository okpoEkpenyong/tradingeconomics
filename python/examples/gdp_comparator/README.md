# **Economic Indicators Comparison API**

This Flask-based web application allows users to compare economic indicators (e.g., GDP and inflation rates) between two countries. The app uses RESTful APIs to fetch data and provides interactive charts for visualization.

---

## **Features**
- Compare GDP and Inflation Rate (MoM) for supported countries.
- Fetches real-time data using external APIs.
- Interactive user interface for data comparison and visualization.
- Implements Content Security Policy (CSP) for enhanced security.
- Extensible modular structure with Flask Blueprints.

---

## **Installation**

### **Prerequisites**
- Python 3.12+
- Node.js (if modifying frontend assets like `script.js`)
- A valid API key for the external data source (Trading Economics API or similar).

### **Steps**
1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Set Up a Virtual Environment**
   It's recommended to use a virtual environment to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   The application relies on environment variables for its configuration. Below is the complete list of required variables and their purposes:
   
   1. Create a `.env` file in the root of the project directory.
   2. Copy the content below into the `.env` file.
   3. Replace placeholder values (e.g., `your_api_key_here`, `my-secret-key`) with actual values.

   ```env
   FLASK_APP=main.py
   FLASK_ENV=development  # Options: development, production
   DEBUG=True
   SECRET_KEY=my-secret-key

   # Redis Configuration
   REDIS_URL=redis://localhost:6379/0
   CACHE_TYPE=RedisCache

   # Trading Economics API
   TRADING_ECONOMICS_API_KEY=your-api-key-here
   API_BASE_URL=https://api.tradingeconomics.com

   # Allowed Countries (comma-separated list)
   ALLOWED_COUNTRIES=Sweden,Mexico,New Zealand,Thailand

   # Logging Configuration
   LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

   # Additional Settings
   CACHE_TIMEOUT=300  # Cache timeout in seconds
   REQUEST_TIMEOUT=30  # HTTP request timeout in seconds
   ```

5. **Run the Application**

   You can run the application using one of the following methods:

   - **Flask Development Server**:
     ```bash
     python main.py
     ```

   - **Gunicorn for Production**:
     ```bash
     gunicorn main:app -c gunicorn_config.py
     ```

   The app will be accessible at [http://127.0.0.1:5000/api](http://127.0.0.1:5000/api).

---

## **Docker Setup**

To run the application using Docker, follow these steps to build and run the container:

### **Steps to Run with Docker**
1. **Build the Docker Image**
   In the root of the project directory, run the following command:
   ```bash
   docker build -t economic-indicators-api .
   ```

2. **Run the Application Using Docker Compose**
   Use Docker Compose to manage both the app and Redis container:
   ```bash
   docker-compose up
   ```

   The app will be accessible at [http://localhost:5000/api](http://localhost:5000/api).

### **Docker Compose Details**
This project includes a `docker-compose.yml` file that sets up the following services:
- **App**: The Flask application running in a container.
- **Redis**: A Redis container for caching purposes.

---

## **Usage**

### **Endpoints**
- `/api/` - Compares economic indicators between two countries (index page).
  - **Query Parameters**:
    - `country1` - First country (e.g., `Sweden`).
    - `country2` - Second country (e.g., `Mexico`).
    - `indicator` - Indicator type (`GDP` or `Inflation Rate MoM`).

### **How to Use**
1. Navigate to the app's index page.
2. Select two countries and an economic indicator.
3. View a table of the comparison data.
4. Plot the data using the interactive chart feature.

---

## **Development Notes**
- **CSP Middleware**: The app uses Flask-Talisman for enforcing a strong Content Security Policy.
  - Current CSP settings allow scripts from `self` and `https://cdn.jsdelivr.net`.
- **Debug Mode**: The app runs in development mode. To enable production:
  1. Set `FLASK_ENV=production` in `.env`.
  2. Update `DEBUG = False` in `Config`.

---

## **Future Enhancements**
- Add support for more economic indicators.
- Enhance charting features (e.g., multiple chart types).
- Improve error handling for API failures.

---

## **Contributing**
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Submit a pull request for review.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Acknowledgments**
- Flask framework
- Chart.js for visualization
- External API for economic data

