import os
import gradio as gr

if os.environ.get("REMOTE_MODE"):
    from remote_agent import agent_for_ui, reset_session_stm, inject_notice
else:
    from agent import agent_for_ui, reset_session_stm, inject_notice

from rollback import rollback_last_change, rollback_all_changes, get_commits, get_commit_stat, get_file_diff

def render_diff(diff_text: str) -> str:
    if not diff_text.strip():
        return "<p style='color:#9ca3af;padding:8px'>No diff available.</p>"
    lines = []
    for line in diff_text.split("\n"):
        if line.startswith("+") and not line.startswith("+++"):
            style = "background:#1a3a1a;color:#4ade80"
        elif line.startswith("-") and not line.startswith("---"):
            style = "background:#3a1a1a;color:#f87171"
        elif line.startswith("@@"):
            style = "background:#1a2a4a;color:#60a5fa"
        elif line.startswith(("diff ", "index ", "---", "+++")):
            style = "color:#6b7280"
        else:
            style = "color:#e5e7eb"
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        lines.append(
            f'<div style="{style};font-family:monospace;font-size:12px;'
            f'padding:1px 8px;white-space:pre">{escaped or "&nbsp;"}</div>'
        )
    return (
        '<div style="background:#0d0d0d;border-radius:8px;padding:8px;'
        f'overflow:auto;max-height:400px">{"".join(lines)}</div>'
    )


def chat_with_agent(message):
    for token in agent_for_ui(user_prompt=message):
        yield token

COLOR_OPTIONS = {
    "Gray": "#2a2a2a",
    "Purple": "#8b5cf6",
    "Blue": "#3b82f6",
    "Emerald": "#10b981",
    "Orange": "#f97316",
    "Pink": "#ec4899",
    "Cyan": "#06b6d4",
}

DEFAULT_COLOR = "#2a2a2a"

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

#chatbot .message-row.bubble.user-row {
    max-width: 80% !important;
}

#chatbot .message-row.bubble.bot-row {
    max-width: 100% !important;
    justify-content: flex-start !important;
}

#chatbot .message-row.bubble.bot-row .message-bubble-border {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
}

#chatbot .message.user {
    border-radius: 18px !important;
    padding: 12px 16px !important;
    color: #ffffff !important;
    width: fit-content !important;
    max-width: 100% !important;
}

#chatbot .message.bot {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 4px 0 !important;
    color: #e5e7eb !important;
    width: 100% !important;
    max-width: 100% !important;
    box-shadow: none !important;
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
"""

# Create the Gradio interface
with gr.Blocks(css=custom_css) as demo:
    # Chat page
    with gr.Column(visible=True) as chat_page:
        gr.HTML("""
            <div class="header">
                <h1>Agentic File Explorer</h1>
                <p>File explorer that uses Agentic Frameworks to perform tasks such as file reading, writing, and summarization.</p>
            </div>
        """)

        with gr.Row():
            settings_btn = gr.Button("⚙️ Bubble Settings", elem_classes=["secondary"], size="sm")
            clear_btn = gr.Button("New Chat", elem_classes=["secondary"], size="sm")

        chatbot = gr.Chatbot(
            elem_id="chatbot",
            height=500,
            show_label=False,
            type="messages",
            avatar_images=(None, None),
            render_markdown=True,
            bubble_full_width=True,
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

        with gr.Accordion("File Changes", open=False):
            commit_skip = gr.State(0)
            commit_list = gr.State([])

            with gr.Row():
                rollback_last_btn = gr.Button("↩ Rollback Last", elem_classes=["secondary"], size="sm")
                rollback_all_btn  = gr.Button("⏮ Rollback All",  elem_classes=["secondary"], size="sm")

            commit_dropdown = gr.Dropdown(choices=[], label="Commits", interactive=True, allow_custom_value=False)
            load_more_btn = gr.Button("Load More", elem_classes=["secondary"], size="sm")
            file_dropdown = gr.Dropdown(choices=[], label="Changed files", interactive=True, visible=False, allow_custom_value=False)
            diff_display = gr.HTML()

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
                <p>Customize your chat experience</p>
            </div>
        """)

        with gr.Column(elem_classes=["settings-page"]):
            with gr.Group(elem_classes=["settings-section"]):
                gr.HTML('<div class="settings-title">User Bubble Color</div>')

                color_radio = gr.Radio(
                    choices=list(COLOR_OPTIONS.keys()),
                    value="Gray",
                    label="User Message Color",
                    interactive=True
                )

                color_preview = gr.HTML(f"""
                    <div style="margin-top: 20px;">
                        <p style="color: #9ca3af; margin-bottom: 10px;">Preview:</p>
                        <div style="background: {DEFAULT_COLOR}; color: white; padding: 12px 16px; border-radius: 18px; max-width: 80%; display: inline-block;">
                            This is how your messages will appear
                        </div>
                    </div>
                """)

            back_btn = gr.Button("← Back to Chat", elem_classes=["primary"])

    # Dynamic style injection for user bubble color
    style_html = gr.HTML(f"""
        <style id="dynamic-user-color">
            #chatbot .message.user {{
                background: {DEFAULT_COLOR} !important;
            }}
        </style>
    """)

    def respond(message, chat_history):
        chat_history = chat_history + [{"role": "user", "content": message}]
        yield chat_history

        response = None
        for token in chat_with_agent(message):
            if not response:
                response = {"role": "assistant", "content": ""}
                chat_history.append(response)
            chat_history[-1]["content"] += token
            yield chat_history

    def show_settings_page():
        return gr.update(visible=False), gr.update(visible=True)

    def show_chat_page():
        return gr.update(visible=True), gr.update(visible=False)

    def update_color(color_name):
        color_hex = COLOR_OPTIONS[color_name]
        preview_html = f"""
            <div style="margin-top: 20px;">
                <p style="color: #9ca3af; margin-bottom: 10px;">Preview:</p>
                <div style="background: {color_hex}; color: white; padding: 12px 16px; border-radius: 18px; max-width: 80%; display: inline-block;">
                    This is how your messages will appear
                </div>
            </div>
        """
        style_update = f"""
            <style id="dynamic-user-color">
                #chatbot .message.user {{
                    background: {color_hex} !important;
                }}
            </style>
        """
        return preview_html, style_update

    def _commit_choices(commits):
        return [f"{c['hash']} — {c['message']}" for c in commits]

    def load_initial_commits():
        commits = get_commits(n=10, skip=0)
        return gr.update(choices=_commit_choices(commits), value=None), commits, 10

    def load_more_commits(current_list, skip):
        new_commits = get_commits(n=10, skip=skip)
        merged = current_list + new_commits
        return gr.update(choices=_commit_choices(merged), value=None), merged, skip + 10

    def on_commit_select(choice):
        if not choice:
            return gr.update(choices=[], visible=False), ""
        commit_hash = choice.split(" — ")[0]
        files = get_commit_stat(commit_hash)
        if not files:
            return gr.update(choices=[], visible=False), ""
        return gr.update(choices=files, value=None, visible=True), ""

    def on_file_select(file_choice, commit_choice):
        if not file_choice or not commit_choice:
            return ""
        commit_hash = commit_choice.split(" — ")[0]
        return render_diff(get_file_diff(commit_hash, file_choice))

    def new_chat():
        reset_session_stm()
        return []

    def do_rollback_last(chat_history):
        result = rollback_last_change()
        notice = f"[File system] {result}"
        inject_notice(notice)
        commits = get_commits(n=10, skip=0)
        return (
            chat_history + [{"role": "assistant", "content": notice}],
            gr.update(choices=_commit_choices(commits), value=None), commits, 10,
            gr.update(choices=[], visible=False), "",
        )

    def do_rollback_all(chat_history):
        result = rollback_all_changes()
        notice = f"[File system] {result}"
        inject_notice(notice)
        commits = get_commits(n=10, skip=0)
        return (
            chat_history + [{"role": "assistant", "content": notice}],
            gr.update(choices=_commit_choices(commits), value=None), commits, 10,
            gr.update(choices=[], visible=False), "",
        )

    settings_btn.click(show_settings_page, outputs=[chat_page, settings_page])
    back_btn.click(show_chat_page, outputs=[chat_page, settings_page])
    clear_btn.click(new_chat, outputs=[chatbot])

    color_radio.change(update_color, inputs=[color_radio], outputs=[color_preview, style_html])

    def clear_textbox():
        return ""

    msg.submit(clear_textbox, None, msg)
    msg.submit(respond, [msg, chatbot], [chatbot])
    submit.click(clear_textbox, None, msg)
    submit.click(respond, [msg, chatbot], [chatbot])

    commit_dropdown.change(on_commit_select, inputs=[commit_dropdown], outputs=[file_dropdown, diff_display])
    file_dropdown.change(on_file_select, inputs=[file_dropdown, commit_dropdown], outputs=[diff_display])
    load_more_btn.click(load_more_commits, inputs=[commit_list, commit_skip], outputs=[commit_dropdown, commit_list, commit_skip])
    rollback_last_btn.click(do_rollback_last, inputs=[chatbot], outputs=[chatbot, commit_dropdown, commit_list, commit_skip, file_dropdown, diff_display])
    rollback_all_btn.click(do_rollback_all,   inputs=[chatbot], outputs=[chatbot, commit_dropdown, commit_list, commit_skip, file_dropdown, diff_display])

    demo.load(load_initial_commits, outputs=[commit_dropdown, commit_list, commit_skip])

if __name__ == "__main__":
    demo.launch()
