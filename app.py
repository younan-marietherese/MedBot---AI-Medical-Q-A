from flask import Flask, request, render_template
from inference import get_answer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        question = request.form.get("question")
        answer = get_answer(question)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    # disable reloader (heavy models + Windows reloader can kill the process)
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
