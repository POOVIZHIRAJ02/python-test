from flask import Flask, jsonify
from flask_cors import CORS
import os
import psycopg2
import logging

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to establish a connection to the PostgreSQL database
def get_db_connection():
    try:
        # Attempt to connect using environment variables
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'default_db'),
            user=os.getenv('DB_USER', 'default_user'),
            password=os.getenv('DB_PASSWORD', 'default_password')
        )
        logger.info("Database connection established successfully.")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

# Route to check if the database connection is working
@app.route('/db-test', methods=['GET'])
def db_test():
    conn = None
    try:
        # Get the database connection
        conn = get_db_connection()
        if not conn:
            logger.error("Failed to establish database connection.")
            return jsonify({"error": "Failed to connect to the database"}), 500
        
        # Create a cursor and execute a simple query to check the connection
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1;')  # Test query to check connection
            result = cursor.fetchone()
            if result and result[0] == 1:
                logger.info("Database connection test passed.")
                return jsonify({"message": "Database is connected successfully."}), 200
            else:
                logger.error("Unexpected result from the database test query.")
                return jsonify({"error": "Database connection test failed."}), 500
    except Exception as e:
        logger.error(f"Exception during database connection test: {e}")
        return jsonify({"error": "An error occurred while testing the database connection."}), 500
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()
            logger.info("Database connection closed.")

# Sample API route for testing the server
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from the backend!"}
    return jsonify(data)

# Main entry point
if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)
