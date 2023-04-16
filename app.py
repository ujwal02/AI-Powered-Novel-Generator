from flask import Flask, request, jsonify, render_template, session
import openai

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
    prompt = (f"You are a {data['genre']} author. Your task is to write a {data['genre']} story in a vivid and intriguing language, incorporating setting details, "
              f"character descriptions, and background information. Develop the plot with engaging dialogue, maintain a consistent tone, and vary the pacing to build and release tension.\n\n"
              f"Title: {data['title']}\n"
              f"Genre: {data['genre']}\n"
              f"Characters: {data['characters']}\n"
              f"Plot: {data['plot']}\n\n"
              f"{data['prompt']}")
    print(f"Prompt: {prompt}")

    num_agents = 2
    refinement_iterations = 2
    refinement_agent_index = num_agents - 1

    openai.api_key = default_api_key

    # Generate initial text
    generated_texts = []
    for i in range(num_agents - 1):
        p = f"{prompt} [Part {i + 1}/{num_agents - 1}]"
        response = openai.Completion.create(engine="text-davinci-002", prompt=p, max_tokens=250, n=1, stop=None, temperature=0.7)
        generated_texts.append(response.choices[0].text.strip())

    # Iteratively refine the text
    for _ in range(refinement_iterations):
        for i in range(num_agents - 1):
            text_part_1 = generated_texts[i]
            text_part_2 = generated_texts[i + 1] if i + 1 < len(generated_texts) else ""
            gap_prompt = f"Continue the story smoothly between:\n\n{text_part_1}\n\nand\n\n{text_part_2}\n\nRefined transition:"
            response = openai.Completion.create(engine="text-davinci-002", prompt=gap_prompt, max_tokens=100, n=1, stop=None, temperature=0.7)
            refined_text = response.choices[0].text.strip()
            generated_texts[i] = text_part_1 + " " + refined_text + " " + text_part_2

    combined_text = ' '.join(generated_texts)

    # Add editing agent
    editing_prompt = f"Please edit the following text for grammar, punctuation, and overall readability:\n\n{combined_text}\n\nEdited Text:"
    editing_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=editing_prompt,
        max_tokens=len(combined_text) + 100,  # Allow some extra tokens for edits
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
