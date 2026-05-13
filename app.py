import gradio as gr
import anthropic

client = anthropic.Anthropic()

def generate_dockerfile(description, base_os, app_type):
    prompt = f"""You are a DevOps expert. Generate a production-ready Dockerfile for:
Description: {description}
Base OS: {base_os}
App Type: {app_type}

Include:
- Multi-stage build if applicable
- Non-root user for security
- Health check
- Clear comments
Only return the Dockerfile content, nothing else."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

demo = gr.Interface(
    fn=generate_dockerfile,
    inputs=[
        gr.Textbox(label="App Description", placeholder="e.g. A FastAPI app with PostgreSQL"),
        gr.Dropdown(["ubuntu:22.04", "debian:slim", "alpine:3.18", "python:3.11-slim"], label="Base OS"),
        gr.Dropdown(["Python/FastAPI", "Node.js", "Java/Spring", "Go", "React"], label="App Type")
    ],
    outputs=gr.Code(language="dockerfile", label="Generated Dockerfile"),
    title="🐳 DevOps Dockerfile Generator",
    description="Generate production-ready Dockerfiles instantly!"
)

demo.launch()
