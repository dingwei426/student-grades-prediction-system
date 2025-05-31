from app import create_app  # Import the create_app function from the app package
import logging

# Create the app instance
app = create_app()
app.logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app.run(debug=True)
