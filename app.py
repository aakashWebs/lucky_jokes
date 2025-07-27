from flask import Flask, render_template, jsonify,request
import random
import requests
app = Flask(__name__)
def get_random_fun_content(joke_type='english'):
    """
    Returns a random English joke, Hindi joke (via dedicated API), or meme.
    """
    # content_types = ["joke_en", "joke_hi", "meme"]
    choice = joke_type #random.choice(content_types)
    try:
        if choice == "english":
            resp = requests.get("https://v2.jokeapi.dev/joke/Any?lang=en&type=single")
            if resp.ok:
                data = resp.json()
                joke = data.get("joke") or f"{data.get('setup')} {data.get('delivery')}"
                return f"{joke}"
            return "😕 Could not fetch English joke."

        elif choice == "hindi":
            resp = requests.get("https://hindi-jokes-api-rm0c.onrender.com/jokes")
            if resp.ok:
                data = resp.json()
                # If API returns array or single object
                joke_text = data.get("jokeContent") or (data[0].get("jokeContent") if isinstance(data, list) else None)
                if joke_text:
                    return f"{joke_text}"
                
            # fallback
            # return "😕 Could not fetch Hindi joke."
            jokes = [
                'पप्पू – डॉक्टर साहब मुझे भूलने की बीमारी हो गई है। डॉक्टर – कब से? पप्पू – कब से क्या? 🤣',
                'टीचर: होमवर्क क्यों नहीं किया? बच्चा: पापा ने कहा जो काम रोज करते हो उसमें दिल नहीं लगता, तो छोड़ दो। 😂'
            ]
            return f"{random.choice(jokes)}"
        
        elif choice == "meme":
            resp = requests.get("https://meme-api.com/gimme")
            if resp.ok:
                m = resp.json()
                return {
                    "title": m.get("title"),
                    "url": m.get("url"),
                }
            
            return {
                "title": "Yes. they were real.",
                "url": "https://i.redd.it/03sy3p10e8ff1.gif"
            }

    except Exception as e:
        return f"❌ Error occurred: {e}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_joke')
def random_joke():
    joke_type = request.args.get('type', 'english')
    joke = get_random_fun_content(joke_type) #get_random_joke()
    return jsonify({'joke': joke})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


