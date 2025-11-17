import gradio as gr
from agent import my_agent

def chat_with_agent(message, history):
    """
    Your agent logic goes here.
    
    Args:
        message: The current user message (string)
        history: List of [user_msg, assistant_msg] pairs
    
    Returns:
        The agent's response (string)
    """
    # Example response - replace with your agent's actual response
    response, history = my_agent(message, history)
    return response, history

# Color options for bot messages
COLOR_OPTIONS = {
    "Purple": "#8b5cf6",
    "Blue": "#3b82f6",
    "Emerald": "#10b981",
    "Orange": "#f97316",
    "Pink": "#ec4899",
    "Cyan": "#06b6d4"
}

custom_css = """
.container {
    max-width: 900px !important;
    margin: auto !important;
}

.gradio-container {
    background: #000000 !important;
}

#chatbot {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

#chatbot .message-wrap {
    padding: 20px 0 !important;
}

#chatbot .message.user {
    background: #2a2a2a !important;
    border-radius: 18px !important;
    padding: 12px 16px !important;
    max-width: 80% !important;
    color: #ffffff !important;
}

#chatbot .message.bot {
    border-radius: 18px !important;
    padding: 12px 16px !important;
    color: #ffffff !important;
    max-width: 80% !important;
}

.input-box {
    border-radius: 24px !important;
    border: 1px solid #3a3a3a !important;
    padding: 12px 20px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    background: #1a1a1a !important;
    color: #ffffff !important;
}

.input-box:focus {
    border-color: #4a4a4a !important;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
}

button.primary {
    background: #ffffff !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-weight: 500 !important;
    border: none !important;
    color: #000000 !important;
}

button.primary:hover {
    background: #e5e5e5 !important;
}

button.secondary {
    background: #2a2a2a !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-weight: 500 !important;
    border: 1px solid #3a3a3a !important;
    color: #ffffff !important;
}

button.secondary:hover {
    background: #3a3a3a !important;
}

.header {
    text-align: center;
    padding: 40px 20px 20px 20px;
}

.header h1 {
    font-size: 32px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 8px;
}

.header p {
    color: #9ca3af;
    font-size: 16px;
}

.settings-page {
    padding: 40px 20px;
    max-width: 600px;
    margin: auto;
}

.settings-section {
    background: #1a1a1a;
    border-radius: 12px;
    padding: 24px;
    margin: 20px 0;
}

.settings-title {
    color: #ffffff;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 16px;
}

.color-option {
    display: inline-block;
    width: 60px;
    height: 60px;
    border-radius: 12px;
    margin: 8px;
    cursor: pointer;
    border: 3px solid transparent;
    transition: all 0.2s;
}

.color-option:hover {
    transform: scale(1.1);
    border-color: #ffffff;
}

.color-option.selected {
    border-color: #ffffff;
    box-shadow: 0 0 0 2px #000, 0 0 0 5px #ffffff;
}
"""

# Create the Gradio interface
with gr.Blocks(css=custom_css) as demo:
    current_color = gr.State("#8b5cf6")
    show_settings = gr.State(False)
    
    # Chat page
    with gr.Column(visible=True) as chat_page:
        gr.HTML("""
            <div class="header">
                <h1>Agentic File Explorer</h1>
                <p>File explorer that uses Agentic Frameworks to perform tasks such as file reading, writing, and summarization.</p>
            </div>
        """)
        
        settings_btn = gr.Button("⚙️ Bubble Settings", elem_classes=["secondary"], size="sm")
        
        chatbot = gr.Chatbot(
            elem_id="chatbot",
            height=500,
            show_label=False,
            type="messages",
            avatar_images=(None, None),
            # bubble_full_width=False,
        )
        
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Message AI Agent...",
                show_label=False,
                container=False,
                elem_classes=["input-box"],
                lines=1,
                max_lines=30
            )
            submit = gr.Button("Send", elem_classes=["primary"], scale=0, min_width=80)
        
        gr.HTML("""
            <div style="text-align: center; padding: 20px; color: #9ca3af; font-size: 14px;">
                <p>This AI assistant can make mistakes. Consider checking important information.</p>
            </div>
        """)
    
    # Settings page
    with gr.Column(visible=False) as settings_page:
        gr.HTML("""
            <div class="header">
                <h1>⚙️ Bubble Settings</h1>
                <p>Customize your AI Agent experience</p>
            </div>
        """)
        
        with gr.Column(elem_classes=["settings-page"]):
            with gr.Group(elem_classes=["settings-section"]):
                gr.HTML('<div class="settings-title">Appearance</div>')
                
                color_radio = gr.Radio(
                    choices=list(COLOR_OPTIONS.keys()),
                    value="Purple",
                    label="Bot Message Color",
                    interactive=True
                )
                
                color_preview = gr.HTML("""
                    <div style="margin-top: 20px;">
                        <p style="color: #9ca3af; margin-bottom: 10px;">Preview:</p>
                        <div style="background: #8b5cf6; color: white; padding: 12px 16px; border-radius: 18px; max-width: 80%; display: inline-block;">
                            This is how bot messages will appear
                        </div>
                    </div>
                """)
            
            back_btn = gr.Button("← Back to Chat", elem_classes=["primary"])
    
    # Dynamic style injection
    style_html = gr.HTML(f"""
        <style id="dynamic-bot-color">
            #chatbot .message.bot {{
                background: #8b5cf6 !important;
            }}
        </style>
    """)

    def respond(message, chat_history):
        if not message.strip():
            yield "", chat_history
            return

        # Immediately show user message
        chat_history.append({"role": "user", "content": message})
        yield "", chat_history

        # Then bot responds
        bot_message, chat_history = chat_with_agent(message, chat_history)
        yield "", chat_history["messages"]
    
    # Toggle between pages
    def show_settings_page():
        return gr.update(visible=False), gr.update(visible=True)
    
    def show_chat_page():
        return gr.update(visible=True), gr.update(visible=False)
    
    # Update color
    def update_color(color_name):
        color_hex = COLOR_OPTIONS[color_name]
        preview_html = f"""
            <div style="margin-top: 20px;">
                <p style="color: #9ca3af; margin-bottom: 10px;">Preview:</p>
                <div style="background: {color_hex}; color: white; padding: 12px 16px; border-radius: 18px; max-width: 80%; display: inline-block;">
                    This is how bot messages will appear
                </div>
            </div>
        """
        style_update = f"""
            <style id="dynamic-bot-color">
                #chatbot .message.bot {{
                    background: {color_hex} !important;
                }}
            </style>
        """
        return preview_html, style_update, color_hex
    
    settings_btn.click(show_settings_page, outputs=[chat_page, settings_page])
    back_btn.click(show_chat_page, outputs=[chat_page, settings_page])
    
    color_radio.change(
        update_color,
        inputs=[color_radio],
        outputs=[color_preview, style_html, current_color]
    )
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()
