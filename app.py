"""
app.py
Gradio UI entry‑point for the WellBe+ Assistant.

This file focuses *exclusively* on building and launching the UI. Business
logic remains in ``wellbe_agent.py`` so that the web interface stays lean and
maintainable.
"""

from __future__ import annotations
import gradio as gr

from wellbe_agent import answer_sync


DESCRIPTION_MD = (
    "# **WellBe+ Assistant**\n\n"
    "WellBe+ AI Agent is a multi‑context assistant built with the Agents SDK framework "
    "from OpenAI. It orchestrates **three secure MCP servers**: a public drug‑knowledge FDA "
    "service, a WHOOP biometric feed, and a MySQL clinical data store.\n\n"
    "Ask how medications, habits or workouts influence your sleep and recovery – the agent "
    "combines **medical knowledge** with your **personal Whoop data** to craft evidence‑backed "
    "answers.\n\n"
    "## Example questions\n"
    "- *What are the adverse effects of Prozac?*\n"
    "- *I started to take Prozac 3 months ago; do you see any trends in my sleep quality and what are its most frequent side‑effects?*\n\n"
    "## MCP Servers in use\n"
    "- [Whoop](https://smithery.ai/server/@ctvidic/whoop-mcp-server)\n"
    "- [Healthcare MCP with PubMed, FDA and other APIs](https://smithery.ai/server/@Cicatriiz/healthcare-mcp-public)\n"
)


def build_interface() -> gr.Blocks:
    """Construct and return the Gradio interface for the WellBe+ Assistant."""
    with gr.Blocks(title="WellBe+ Assistant") as app:
        gr.HTML("<p><img src='file=docs/images/logo.png' style='height:80px'></p>")
        gr.Markdown(DESCRIPTION_MD)

        with gr.Row():
            # -----------------------------------------------------------------
            # Left column – credential inputs
            # -----------------------------------------------------------------
            with gr.Column(scale=1):
                gr.Markdown("### Credentials")
                openai_key_box = gr.Textbox(
                    label="OpenAI API Key",
                    type="password",
                    placeholder="sk‑…",
                )
                whoop_email_box = gr.Textbox(label="Whoop e‑mail")
                whoop_pass_box = gr.Textbox(label="Whoop password", type="password")

            # -----------------------------------------------------------------
            # Right column – chat interface
            # -----------------------------------------------------------------
            with gr.Column(scale=2):
                gr.Markdown("### Chat")
                question_box = gr.Textbox(
                    label="Question",
                    lines=3,
                    placeholder="e.g. How has my sleep changed since starting Prozac?",
                )
                answer_box = gr.Textbox(label="Assistant", lines=8, interactive=False)
                ask_btn = gr.Button("Ask Assistant ▶️", variant="primary")
                ask_btn.click(
                    fn=answer_sync,
                    inputs=[
                        question_box,
                        openai_key_box,
                        whoop_email_box,
                        whoop_pass_box,
                    ],
                    outputs=answer_box,
                )

        gr.Markdown(
            "---\nDevelopers: [Natalia B.](https://www.linkedin.com/in/natalia-bobkova/), [Victoria L.](https://www.linkedin.com/in/victoria-latynina/)"
        )

    return app


if __name__ == "__main__":
    build_interface().launch()
