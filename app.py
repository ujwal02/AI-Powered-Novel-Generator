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
    prompt = f"Title: {data['title']}\nGenre: {data['genre']}\nCharacters: {data['characters']}\nPlot: {data['plot']}\n\n{data['prompt']}"
    print(f"Prompt: {prompt}")

    num_agents = 2
    prompts = [f"{prompt} [Part {i+1}/{num_agents}]" for i in range(num_agents)]

    openai.api_key = default_api_key

    generated_texts = []

    for p in prompts:
        response = openai.Completion.create(engine="text-davinci-002", prompt=p, max_tokens=150, n=1, stop=None, temperature=0.7)
        print(f"API Response for {p}: {response}")
        generated_text = response.choices[0].text.strip()
        generated_texts.append(generated_text)

    combined_text = ""
    for i, text in enumerate(generated_texts):
        if i > 0:
            text_part_1 = generated_texts[i - 1]
            text_part_2 = text
            gap_prompt = f"Continue the story smoothly between:\n\n{text_part_1}\n\nand\n\n{text_part_2}\n\nRefined transition:"

            gap_response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=gap_prompt,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.5
            )

            refined_transition = gap_response.choices[0].text.strip()
            combined_text += " " + refined_transition

        combined_text += " " + text

    formatted_text = formatText(combined_text)
    return jsonify(formatted_text)

        # Add refinement process
    refinement_prompt = f"Refine the following text for better consistency, coherence, and add gaps between different parts of the story:\n\n{combined_text}\n\nRefined Text:"
    refined_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=refinement_prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5
    )
    refined_text = refined_response.choices[0].text.strip()

    formatted_text = formatText(refined_text)
    return jsonify(formatted_text)

def formatText(text):
    return text.replace('\n', ' ')

if __name__ == "__main__":
    app.run(debug=True)
