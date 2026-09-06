import gradio as gr
from src.query import process_user_query

def answer_question(user_input: str):
    """Send the user's question to the warehouse query engine."""
    if not user_input or not user_input.strip():
        return "", "", ""

    try:
        generated_sql, query_result, final_answer = process_user_query(
            user_input.strip()
        )
        return final_answer, generated_sql, query_result

    except Exception as e:
        return f"❌ Error: {e}", "", ""

# Injecting your custom color palette seamlessly into Gradio's CSS
custom_theme = gr.themes.Soft(
    primary_hue=gr.themes.colors.blue,      # Fallback defaults
    neutral_hue=gr.themes.colors.slate,
).set(
    button_primary_background_fill="#118AB2",      # Deep Sky Blue
    button_primary_background_fill_hover="#06D6A0",# Emerald Accent
    button_primary_text_color="#FFFFFF",
    button_secondary_background_fill="#FF7F50",    # Coral Accent
    button_secondary_text_color="#FFFFFF",
    background_fill_primary="#FFFFFF",
    block_background_fill="#FFD166" + "1A",        # 10% Transparent Yellow tint for block depth
    block_border_color="#118AB2",
)

with gr.Blocks(
    title="LLM Warehouse Assistant",
    theme=custom_theme,
) as demo:

    gr.Markdown(
        """
        # 🧠 LLM Warehouse Assistant
        Ask questions about your document warehouse using natural language.
        """
    )

    # Dynamic layout structure: splits left/right on desktops, stacks vertically on mobile
    with gr.Row(equal_height=False):
        
        # Left Panel: User Input and Controls
        with gr.Column(scale=1, min_width=320):
            gr.Markdown("### 📝 Ask Your Query")
            question = gr.Textbox(
                label="Natural Language Input",
                placeholder="Example: How many documents are there?",
                lines=4,
            )
            
            with gr.Row():
                submit = gr.Button("Ask Engine", variant="primary")
                clear = gr.Button("Clear All", variant="secondary")
                
            gr.Markdown(
                """
                **Engine Workflow:**
                1. Parse natural text query
                2. Autogenerate optimal SQL
                3. Run extraction against DuckDB
                4. Explanatory interpretation
                """
            )

        # Right Panel: Output and Technical Inspections
        with gr.Column(scale=1, min_width=320):
            gr.Markdown("### ✨ Answer Interpretations")
            answer = gr.Markdown("*The engine breakdown will appear here...*")

            with gr.Accordion("🛠️ Technical Details & Schema Logs", open=False):
                generated_sql = gr.Code(
                    label="Generated SQL Blueprint",
                    language="sql",
                    lines=5,
                )

                query_result = gr.Textbox(
                    label="Raw Database Output Matrix",
                    lines=8,
                )

    # Event handlers for submission
    submit.click(
        fn=answer_question,
        inputs=question,
        outputs=[answer, generated_sql, query_result],
    )

    question.submit(
        fn=answer_question,
        inputs=question,
        outputs=[answer, generated_sql, query_result],
    )

    # Reset trigger to sweep layout clean
    clear.click(
        fn=lambda: ("", "*The engine breakdown will appear here...*", "", ""),
        inputs=[],
        outputs=[question, answer, generated_sql, query_result],
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
    )
