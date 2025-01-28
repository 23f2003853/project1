from flask import Flask, request, jsonify
import os
import traceback

app = Flask(__name__)

# Dummy function to simulate task execution, replace with actual task logic
def execute_task(task_description):
    try:
        # Simulate execution logic (e.g., interacting with an LLM or internal services)
        if "error" in task_description.lower():
            raise ValueError("Simulated error during task execution")
        
        # Simulate success
        return f"Task '{task_description}' executed successfully."

    except Exception as e:
        # Log the exception (here, we just print it; in real apps, log to a file or monitoring system)
        print(f"Error occurred: {str(e)}")
        raise

@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')
    
    if not task_description:
        # Missing task description in query string
        return jsonify({"error": "Missing task description"}), 400

    try:
        # Attempt to execute the task
        result = execute_task(task_description)
        
        # Return successful response with task output
        return jsonify({"message": result}), 200

    except ValueError as ve:
        # If task execution fails due to a specific error
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Internal server error for unhandled exceptions
        error_details = traceback.format_exc()  # Get stack trace for debugging purposes
        return jsonify({"error": "Internal server error", "details": error_details}), 500

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path')
    
    if not file_path:
        return jsonify({"error": "Missing file path"}), 400
    
    # Ensure file path is not outside the allowed directory (security measure)
    if not os.path.isabs(file_path):
        return jsonify({"error": "Invalid file path"}), 400

    try:
        # Check if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
            return content, 200  # Return file content with 200 OK status
        else:
            return jsonify({"error": "File not found"}), 404  # File does not exist
    except Exception as e:
        # Catch other exceptions (e.g., permission errors) and return internal server error
        error_details = traceback.format_exc()
        return jsonify({"error": "Internal server error", "details": error_details}), 500


if __name__ == '__main__':
    app.run(debug=True)
