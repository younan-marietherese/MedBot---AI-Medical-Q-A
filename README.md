# MedBot

MedBot is an AI-powered medical question-answering assistant built using **Flask** for the interface and a **fine-tuned TinyLLaMA** model for inference.

It allows you to:
- Ask medical-related questions through a clean, web-based interface.
- Receive AI-generated answers in real-time.
- Run completely locally via Docker; no external API calls required.

**Disclaimer**: This app is for educational and research purposes only. It is not intended for professional medical diagnosis or treatment.

---

## 1. Setup Instructions (Run Locally via Docker)

**Prerequisite:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

**Steps:**
1. Build the Docker image.
2. Run the container.
3. Access the app in your browser at **http://localhost:8080**.

---

## 2. How to Use the Interface

1. Open the web app in your browser.
2. Type your question in the input box.
3. Click **Submit**.
4. Wait for the model to process your question.
5. The AI-generated response will appear below the input field.

---

## 3. Known Issues or Limitations

- Startup Delay: First load may take time while the model downloads and initializes.
- Performance: On low-spec hardware, generation speed may be slow.
- Accuracy: TinyLlama is lightweight and may not always provide clinically accurate answers.
- No History: Current version doesn't store previous questions or answers.
- Medical Disclaimer: Not for real-world medical use.

---

## 4. Deploy to Hugging Face Spaces (Docker)

What you’ll need: 

- A Hugging Face account (free)

- Your project files:
app.py, inference.py, requirements.txt, Dockerfile, templates/, medbot_model/ 

Do not upload a huge base_model/ folder. The base model (e.g., TinyLlama/TinyLlama-1.1B) will be downloaded automatically by the container.

A. Create the Space:

- Go to Spaces -> Create new Space.

- Name: medbot (or any name).

- SDK: Docker.

- Visibility: Public (or Private).

- Click Create Space.

B. Upload your project:
Upload your files into the Space (drag & drop or “Add file -> Upload”)

C. Pick a GPU (Optional but useful for faster responses):

- Open the Settings -> Hardware tab in the Space.

- Choose a GPU (e.g., Nvidia 1×L4) when you want faster responses.

- You can Pause Space when you’re done to stop billing; click Restart later to bring it back.

D. Build & logs:

- Spaces will build the Docker image automatically after each commit.

- Click Logs to watch the build and startup.

- When you see something like: 
Starting gunicorn...
Listening at: http://0.0.0.0:8080
The app is live.

E. Your public URL: 

- The app will be available at:
https://huggingface.co/spaces/<your-username>/<space-name>
- In my case: https://huggingface.co/spaces/MTY2025/medbot

F. Common issues (quick fixes): 

- Tokenizer “fast” JSON error: we already force use_fast=False in inference.py.

- Protobuf missing: added to requirements.txt.

- Cache permission denied: Dockerfile sets HF_HOME=/data/hf and creates the folder.

- Slow first request: first run downloads the base model; later runs are faster.

- High cost risk: remember to Pause Space when not using GPU.

---

## 5. Preview
![MedBot in Action](assets/preview.png)


