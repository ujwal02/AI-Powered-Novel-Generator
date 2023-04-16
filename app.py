from flask import Flask, request, jsonify, render_template, session
import openai, time

app = Flask(__name__)

default_api_key = "Your API Key"

@app.route("/", methods=["GET"])
def index():
    saved_api_key = request.args.get("api-key", default_api_key)
    return render_template("index.html", saved_api_key=saved_api_key)

@app.route("/save-api-key", methods=["POST"])
def save_api_key():
    global default_api_key
    default_api_key = request.form["api-key"]
    print(f"New API Key: {default_api_key}")  # Add this line for debugging
    return "", 204

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = (f"You are a {data['genre']} author. Your task is to write a {data['genre']} story that is vivid, intriguing, and engaging. Pay close attention to the following aspects:\n\n"
              f"1. Setting: Include time period, location, and relevant background information.\n"
              f"2. Characters: Describe the protagonist, antagonist, and other key characters in terms of their appearance, motivations, and roles in the story.\n"
              f"3. Conflict: Clearly outline the main conflict and the stakes involved.\n"
              f"4. Dialogue: Use dialogue to advance the plot, reveal character, and provide information to the reader.\n"
              f"5. Theme: Develop the central theme throughout the plot, characters, and setting.\n"
              f"6. Tone: Maintain a consistent tone that is appropriate to the genre, setting, and characters.\n"
              f"7. Pacing: Vary the pace to build and release tension, advance the plot, and create a dramatic effect.\n\n"
              f"Title: {data['title']}\n"
              f"Genre: {data['genre']}\n"
              f"Characters: {data['characters']}\n"
              f"Plot: {data['plot']}\n\n"
              f"{data['prompt']}")
    print(f"Prompt: {prompt}")

    num_agents = 2
    refinement_iterations = 1
    refinement_agent_index = num_agents - 1

    openai.api_key = default_api_key

    num_agents = 2  # Change this value to increase or decrease the number of agents
    generated_text = ""
    for i in range(num_agents):
        if i == 0:
            prompt_to_use = f"{prompt} [Part {i + 1}/{num_agents}]"
        else:
            prompt_to_use = generated_text[-1] + " [Part {i + 1}/{num_agents}]"

        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt_to_use, max_tokens=380, n=1, stop=None, temperature=0.7)
        new_text = response.choices[0].text.strip()
        generated_text += " " + new_text

        time.sleep(0)  # Wait for 1 minute before the next agent starts to generate text to reset the token usage

    combined_text = generated_text

    # Add editing agent
    editing_prompt = f"Please edit the following text for grammar, punctuation, and overall readability:\n\n{combined_text}\n\nEdited Text:"
    editing_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=editing_prompt,
        max_tokens=len(combined_text) + 300,  # Allow some extra tokens for edits
        n=1,
        stop=None,
        temperature=0.5
    )
    edited_text = editing_response.choices[0].text.strip()

    # Format edited text
    formatted_text = formatText(edited_text)
    return jsonify(formatted_text)

def formatText(text):
    return text.replace('\n', ' ')

if __name__ == "__main__":
    app.run(debug=True)
