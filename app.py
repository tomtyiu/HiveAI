from flask import Flask, render_template, request  # Import Flask modules for web functionality
from ai_logic import queen_ai_task, parse_task_description, subordinate_ai_task, dynamic_worker_assignment  # Import AI delegation functions

# Initialize the Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route for the web application.

    Handles both GET requests (to load the page) and POST requests (when the user submits a task).
    Based on the user's input, it interacts with the AI logic functions to:
    1. Determine the complexity of the task (number of agents required).
    2. Assign tasks to single or multiple AI agents.
    3. Integrate and present results dynamically.

    Returns:
        str: Rendered HTML template (`index.html`) with populated user input and AI responses.
    """
    user_input = ""  # Variable to hold user query from the form
    ai_response = ""  # Variable to store the AI's response

    if request.method == "POST":  # Process form submission from the user
        # Get the user input from the submitted form
        user_input = request.form.get("user_query", "")  
        
        # Check if the user input is non-empty (strip removes leading/trailing whitespace)
        if user_input.strip():
            # Analyze the user input to decide how many AI workers are needed
            worker_count = parse_task_description(user_input)
            
            # Get instructions from the Queen AI based on the user input
            queen_response = queen_ai_task(user_input)

            if worker_count > 1:  # If the task requires multiple agents
                # Create a task context to describe the assignment
                context = f"Task: {user_input} as instructed by the Queen AI."
                
                # Dynamically assign tasks to the required number of AI agents
                worker_responses = dynamic_worker_assignment(worker_count, "Multi-Agent Task", context)
                
                # Combine all worker responses for integration
                combined_worker_output = "\n\n".join(worker_responses)
                
                # Ask Queen AI to process and summarize the combined output from workers
                final_queen_response = queen_ai_task(f"Integrate these responses: {combined_worker_output}")
                
                # Compile the AI response including individual and integrated results
                ai_response = f"Queen AI Instruction:\n{queen_response}\n\n" \
                              f"Workers ({worker_count}) responses:\n{combined_worker_output}\n\n" \
                              f"Final integrated response:\n{final_queen_response}"
            else:  # If only a single agent is required for the task
                # Assign task to a single subordinate AI and get the response
                subordinate_response = subordinate_ai_task("Single Task", queen_response)
                
                # Compile the response for the user
                ai_response = f"Queen AI Instruction:\n{queen_response}\n\n" \
                              f"Subordinate AI Response:\n{subordinate_response}"
        else:  # If the form is empty
            ai_response = "Please provide a task description."

    # Render the HTML template with the user input and AI response variables
    return render_template("index.html", user_input=user_input, ai_response=ai_response)

if __name__ == "__main__":
    """
    Run the Flask web application in debug mode.
    """
    app.run(debug=True)
