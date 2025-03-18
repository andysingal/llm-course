```py
import anthropic
import os
import sys
from termcolor import colored
from dotenv import load_dotenv


class ClaudeAgent:
    def __init__(self, api_key=None, model="claude-3-7-sonnet-20250219", max_tokens=4000):
        """Initialize the Claude agent with API key and model."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set ANTHROPIC_API_KEY environment variable or pass api_key.")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.max_tokens = max_tokens  # Maximum tokens for Claude's responses
        self.conversation_history = []
        self.file_backups = {}  # For undo functionality

        # System prompt with instructions for using the text editor tool
        self.system_prompt = """You are a helpful coding assistant with access to a text editor tool.
You can view and modify files using the following commands:
1. view - Use this to examine the contents of a file before making any changes
Parameters: path (required), view_range (optional)

Example usage: View a file to understand its structure before editing
2. str_replace - Use this to modify file contents by replacing text
Parameters: path (required), old_str (required), new_str (required)

Important: The old_str must match EXACTLY with the content to replace
Best practice: First use view to see the file, then use str_replace
3. create - Use this to create a new file with content
Parameters: path (required), file_text (required)

Example usage: Create new test files, documentation, etc.
4. insert - Use this to add text at a specific location in a file
Parameters: path (required), insert_line (required), new_str (required)

Best practice: Use view first to identify the correct line number
5. undo_edit - Use this to revert the last edit made to a file
Parameters: path (required)

Example usage: When you need to undo a mistaken edit
IMPORTANT WORKFLOW:
1. When asked to modify a file, ALWAYS use view first to see the contents

2. For each modification task, use the appropriate command
3. When using str_replace, ensure the old_str matches exactly with whitespace and indentation
4. After making changes, summarize what you modified
For sequential operations, make sure to complete one tool operation fully before starting another.
        """.strip()

    def chat(self):
        """Start an interactive chat session with Claude."""
        print(colored("\n🤖 Claude Agent with Text Editor Tool", "cyan"))
        print(colored("Type 'exit' to quit, 'history' to see conversation history\n", "cyan"))

        while True:
            user_input = input(colored("You: ", "green"))
            if user_input.lower() == 'exit':
                print(colored("\nGoodbye! 👋", "cyan"))
                break
            if user_input.lower() == 'history':
                self._print_history()
                continue

            # Process the user message and handle any tool use
            final_response = self._process_message(user_input)
            # Print the final response
            if final_response:
                self._print_assistant_response(final_response)

    def _process_message(self, user_message):
        """Process a user message, handling any tool use with a simple loop."""
        # Add the user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": [{"type": "text", "text": user_message}]
        })
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                tools=[{"type": "text_editor_20250124",
                        "name": "str_replace_editor"}],
                messages=self.conversation_history
            )
            # Add Claude's response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            # Main loop for handling tools - continue as long as Claude wants to use more tools
            while response.stop_reason == "tool_use":
                # Process all tool_use requests in the current response
                for content_item in response.content:
                    if content_item.type == "tool_use":
                        # Execute the tool
                        tool_result = self._handle_tool_use(content_item)
                        # Add the result to conversation history
                        self.conversation_history.append({
                            "role": "user",
                            "content": [{
                                "type": "tool_result",
                                "tool_use_id": content_item.id,
                                "content": tool_result
                            }]
                        })

                # Get the next response from Claude with the tool results
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=self.system_prompt,
                    tools=[{"type": "text_editor_20250124",
                            "name": "str_replace_editor"}],
                    messages=self.conversation_history
                )
                # Add Claude's response to the history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
            # The loop will continue if response.stop_reason is still "tool_use"
            # Otherwise, it will exit and return the final response
            return response
        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))
            return None

    def _handle_tool_use(self, tool_use):
        """Handle tool use requests from Claude."""
        print(colored(f"\n🛠️ Using tool: {tool_use.name}", "yellow"))
        try:
            input_params = tool_use.input
            command = input_params.get('command', '')
            file_path = input_params.get('path', '')
            print(colored(f"Command: {command} on {file_path}", "yellow"))
            if command == 'view':
                view_range = input_params.get('view_range', None)
                return self._view_file(file_path, view_range)
            elif command == 'str_replace':
                old_str = input_params.get('old_str', '')
                new_str = input_params.get('new_str', '')
                return self._replace_in_file(file_path, old_str, new_str)
            elif command == 'create':
                file_text = input_params.get('file_text', '')
                return self._create_file(file_path, file_text)
            elif command == 'insert':
                insert_line = input_params.get('insert_line', 0)
                new_str = input_params.get('new_str', '')
                return self._insert_in_file(file_path, insert_line, new_str)
            elif command == 'undo_edit':
                return self._undo_edit(file_path)
            else:
                return f"Error: Unknown command '{command}'"
        except Exception as e:
            return f"Error executing {tool_use.name}: {str(e)}"

    def _view_file(self, file_path, view_range=None):
        """View file contents."""
        try:
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if view_range:
                start = max(0, view_range[0] - 1)  # Convert to 0-indexed
                end = view_range[1] if view_range[1] != -1 else len(lines)
                lines = lines[start:end]
            # Add line numbers
            result = ""
            for i, line in enumerate(lines):
                line_num = i + 1 if not view_range else view_range[0] + i
                result += f"{line_num}: {line}"
            return result
        except Exception as e:
            return f"Error viewing file: {str(e)}"

    def _create_file(self, file_path, file_text):
        """Create a new file."""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            if os.path.exists(file_path):
                return f"Error: File already exists: {file_path}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_text)
            return f"Successfully created file: {file_path}"
        except Exception as e:
            return f"Error creating file: {str(e)}"

    def _replace_in_file(self, file_path, old_str, new_str):
        """Replace text in a file."""
        try:
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
            # Create backup
            self._backup_file(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Count occurrences
            count = content.count(old_str)
            if count == 0:
                return f"Error: Text not found in {file_path}"
            if count > 1:
                return f"Error: Multiple matches ({count}) found in {file_path}"
            # Replace the text
            new_content = content.replace(old_str, new_str, 1)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return "Successfully replaced text at exactly one location."
        except Exception as e:
            return f"Error replacing text: {str(e)}"

    def _insert_in_file(self, file_path, insert_line, new_str):
        """Insert text at a specific line in a file."""
        try:
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
            # Create backup
            self._backup_file(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if insert_line > len(lines):
                return f"Error: Line number {insert_line} exceeds file length ({len(lines)})"
            # Insert the new text
            lines.insert(insert_line, new_str if new_str.endswith(
                '\n') else new_str + '\n')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return f"Successfully inserted text at line {insert_line}."
        except Exception as e:
            return f"Error inserting text: {str(e)}"

    def _undo_edit(self, file_path):
        """Undo the last edit to a file."""
        try:
            if file_path not in self.file_backups:
                return f"Error: No backup found for {file_path}"
            backup_content = self.file_backups[file_path]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            # Remove the backup
            del self.file_backups[file_path]
            return f"Successfully restored {file_path} to previous state."
        except Exception as e:
            return f"Error undoing edit: {str(e)}"

    def _backup_file(self, file_path):
        """Create a backup of a file before editing."""
        if file_path not in self.file_backups:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.file_backups[file_path] = f.read()
            except Exception:
                pass

    def _print_assistant_response(self, response):
        """Print the assistant's response."""
        if not response:
            return
        print(colored("\nClaude: ", "blue"), end="")
        for content in response.content:
            if content.type == "text":
                print(colored(content.text, "blue"))

    def _print_history(self):
        """Print the conversation history."""
        print(colored("\n===== Conversation History =====", "cyan"))
        for message in self.conversation_history:
            role = message["role"]
            if role == "user":
                content = message["content"][0]
                if content["type"] == "text":
                    print(colored(f"\nYou: {content['text']}", "green"))
                elif content["type"] == "tool_result":
                    print(colored(f"\nTool Result: [ID: {content['tool_use_id']}]", "yellow"))
            elif role == "assistant":
                print(colored("\nClaude: ", "blue"), end="")
                for content in message["content"]:
                    if content.type == "text":
                        print(colored(content.text, "blue"))
                    elif content.type == "tool_use":
                        print(colored(f"[Used tool: {content.name}]", "yellow"))
        print(colored("\n===============================", "cyan"))

def main():
    """Main function to run the Claude agent."""
    try:
        # Load environment variables from .env file
        load_dotenv()
        agent = ClaudeAgent()
        agent.chat()
    except KeyboardInterrupt:
        print(colored("\nGoodbye! 👋", "cyan"))
    except Exception as e:
        print(colored(f"\nError: {str(e)}", "red"))

if __name__ == "__main__":
    main()
```
