import gradio as gr
import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="Qwen/Qwen2.5-72B-Instruct",
    token=os.environ.get("HF_TOKEN")
)

def generate_dockerfile(description, base_os, app_type):
    response = client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a DevOps expert. Return ONLY Dockerfile content, no explanation, no markdown backticks."
            },
            {
                "role": "user",
                "content": f"""Generate a production-ready Dockerfile for:
Description: {description}
Base OS: {base_os}
App Type: {app_type}

Include:
- Multi-stage build if applicable
- Non-root user for security
- Health check
- Clear comments"""
            }
        ],
        max_tokens=800,
        temperature=0.3
    )
    return response.choices[0].message.content

demo = gr.Interface(
    fn=generate_dockerfile,
    inputs=[
        gr.Textbox(label="App Description", placeholder="e.g. A FastAPI app with PostgreSQL"),
        gr.Dropdown(["ubuntu:22.04", "debian:slim", "alpine:3.18", "python:3.11-slim"], label="Base OS"),
        gr.Dropdown(["Python/FastAPI", "Node.js", "Java/Spring", "Go", "React"], label="App Type")
    ],
    outputs=gr.Code(language="dockerfile", label="Generated Dockerfile"),
    title="🐳 DevOps Dockerfile Generator",
    description="Generate production-ready Dockerfiles using FREE AI!"
)

demo.launch()
