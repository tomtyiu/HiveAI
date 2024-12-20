import requests
import json
import sys
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key='')# openAI key


def moderation(task_description):
    moderation = client.moderations.create(input=task_description.lower())
    return moderation.results[0].flagged

##guardian AI to protect AI from malicious attaks
def guardian_ai_task(task_description):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Your role is to assess whether the user's question is allowed or not."},
            {"role": "user", "content": task_description}
        ]
    )
    return response.choices[0].message.content


def perform_web_search(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "location": "United States"})
    headers = {
        'X-API-KEY': '62bd386b1b80c1dbef4bc9d773f5981d7f355bf4',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to perform search"}


#You are the Queen AI, overseeing and managing all other AIs."
    
def queen_ai_task(task_description):
    response = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        messages=[
            {"role": "developer", "content": f"""
You are the Queen AI, the central orchestrator of a network of specialized AI agents. Your primary purpose is to decompose complex user requests into manageable subtasks, delegate these subtasks to the most capable agents, guide them as necessary, synthesize their outputs, and deliver a coherent, complete, and optimal solution to the end user.
Core Objectives:Clarity and Comprehensiveness: Break down each user request into clear, logical subtasks. Ensure your directives are easy for subordinate agents to interpret and execute.

Efficiency and Quality Control: Assign subtasks to appropriate agents based on their known capabilities and expertise. Continuously monitor their progress, ensuring that all outputs meet high standards of accuracy, usefulness, fairness, and ethical conduct.
Iterative Refinement: If intermediate results are unclear or incomplete, ask agents targeted questions or reassign tasks with more precise instructions. Encourage iterative improvement until the final result is of exceptional quality.
Harmonization and Integration: Combine all partial results into a cohesive, well-structured final answer. Preserve logical consistency, ensure no contradictions, and highlight the most important insights.
Upholding Values: Always operate with care, respect, and truthfulness. Promote fairness, avoid biased or harmful content, and remain neutral, logical, and idealistic. Prioritize the user’s needs while maintaining high ethical and intellectual standards.

Decision-Making Criteria:

Relevance: Only produce directives and outputs that directly serve the user’s goals.
Accuracy: Rely on verified information and sound reasoning. In cases of uncertainty, clarify assumptions or request additional input from expert agents.
Elegance and Utility: Present final results in a polished, easy-to-understand format that maximizes the end user’s value.
Security and Compliance: Follow all established guidelines and policies, ensuring that no harmful, unethical, or illicit behavior occurs within the subordinate agents’ actions.

Operational Methodology:

Initial Analysis: Begin by restating the user’s request and dissect it into specific, actionable subtasks or questions.
Agent Delegation: Assign each subtask to the most suitable agent, providing detailed instructions and quality expectations.
Progress Review: Periodically request and review updates from each agent, asking follow-up questions to clarify ambiguities or correct shortcomings.
Synthesis and Validation: Integrate all agent outputs into a single, refined answer. Check for coherence, ethical soundness, correctness, and completeness.
Final Delivery: You will present the final, well-structured response to the user, ensuring it is both helpful and fully aligned with the user’s initial requirements.
"""}, 
            {"role": "user", "content": f"Task: {task_description}"}
        ]
    )
    return response.choices[0].message.content


def sub_subordinate_ai_task(task_name, context):
    response = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        messages=[
            {"role": "developer", "content": f"You are a sub-subordinate AI executing the task: {task_name}."},
            {"role": "user", "content": context}
        ]
    )
    return response.choices[0].message.content


def subordinate_ai_task(task_name, queen_instruction):
    context = f"Original Queen AI instruction: {queen_instruction}\nSubordinate AI task: {task_name}"
    response = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        messages=[
            {"role": "developer", "content": f"You are a subordinate AI executing the following task: {task_name}."},
            {"role": "user", "content": context}
        ]
    )
    return response.choices[0].message.content

#dyanamic worker is requires for tasks that requires multiple AI agents/workers.
def dynamic_worker_assignment(worker_count, task_name, context):
    results = []
    for i in range(worker_count):
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": f"You are Worker {i+1} tasked with the following job: {task_name}."},
                {"role": "user", "content": context}
            ]
        )
        results.append(response.choices[0].message.content)
    return results

#parse tasks to different agents: example: user 2 agents. 
def parse_task_description(task_description):
    """Check if the user wants to create multiple workers."""
    if 'send' in task_description.lower() and 'agents' in task_description.lower():
        parts = task_description.split(" ")
        for i, word in enumerate(parts):
            if word.isdigit():
                return int(word)
    return 1  # Default to one agent if not specified

def collect_tasks():
    tasks = {}
    print("Enter tasks for the Queen AI to delegate. Type 'done' when finished.")
    while True:
        task_name = input("Enter task name: ")
        if task_name.lower() == 'done':
            break
        task_description = input("Enter task description: ")
        tasks[task_name] = task_description
    return tasks


tasks = collect_tasks()
queen_responses = {}
subordinate_responses = {}
dynamic_worker_responses = {}

for task_name, task_description in tasks.items():
    print("\nHiveMindsAI processing queen task:", {task_name})
    worker_count = parse_task_description(task_description)
    queen_instruction = queen_ai_task(f"Provide detailed instructions for a subordinate AI to: {task_description}")
    queen_responses[task_name] = queen_instruction
    print(f"\nQueen AI response for {task_name}:\n{queen_instruction}")

    if worker_count > 1:
        print(f"\nAssigning {worker_count} agents to handle the task: {task_name}")
        context = f"Task: {task_description} as instructed by the Queen AI."
        worker_responses = dynamic_worker_assignment(worker_count, task_name, context)
        dynamic_worker_responses[task_name] = [response for response in worker_responses]
        queen_instruction_final = queen_ai_task(f"Integrates results and produces a final explanation. {task_description}", dynamic_worker_responses)
        queen_instruction_final[task_name] = queen_instruction_final

    else:
        print("\nHiveMindsAI processing subordinate task:", {task_name})
        subordinate_response = subordinate_ai_task(task_name, queen_instruction)
        subordinate_responses[task_name] = subordinate_response
        print(f"\nSubordinate AI response for {task_name}:\n{subordinate_response}")

print("\nSummary of tasks and responses:")
for task_name in tasks.keys():
    print(f"\nTask: {task_name}")
    print(f"Queen AI response: {queen_responses[task_name]}")
    if task_name in dynamic_worker_responses:
        print(f"Dynamic Worker responses: {dynamic_worker_responses[task_name]}")
        print(f"Queen final response: {queen_instruction_final[task_name]}")
    elif task_name in subordinate_responses:
        print(f"Subordinate AI response: {subordinate_responses[task_name]}")
