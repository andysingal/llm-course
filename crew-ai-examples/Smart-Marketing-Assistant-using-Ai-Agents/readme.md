# Smart Marketing Assistant using AI Agents

## Overview
The Smart Marketing Assistant is an innovative project that leverages AI agents to automate tasks within an Instagram marketing workflow. This project aims to streamline and optimize various marketing activities, providing users with a powerful tool to enhance their social media strategies.

## Workflow
![](https://github.com/praj2408/Smart-Marketing-Assistant-using-Ai-Agents/blob/main/docs/crew2-instagram.jpg)
## Features
- **Automated Content Creation**: Generate engaging posts and stories using AI-powered content creation tools.
- **Hashtag Optimization**: Analyze and suggest the most effective hashtags to reach a wider audience.
- **Post Scheduling**: Automatically schedule posts at optimal times for maximum engagement.
- **Performance Analytics**: Track and analyze the performance of posts and campaigns.
- **Audience Interaction**: Automate responses to comments and messages to maintain active engagement with followers.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Smart-Marketing-Assistant-using-Ai-Agents.git
   cd Smart-Marketing-Assistant-using-Ai-Agents
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```
     LANGCHAIN_TRACING_V2=true
     LANGCHAIN_API_KEY=your langchain api key
     OPENAI_API_KEY=your openai api key
     OPENAI_MODEL_NAME=gpt-3.5-turbo-0125
     ```

## Usage

1. **Run the Assistant**:
   ```bash
   python main.py
   ```

2. **Access the Dashboard**:
   Open your web browser and navigate to `http://localhost:5000` to access the Smart Marketing Assistant dashboard.

## Configuration

- **Customization**:
  You can customize the assistant's behavior and settings by modifying the `config.py` file.

- **AI Models**:
  The project uses pre-trained AI models. You can replace these models with your own by changing llm = your_model in the main.py file.

## Project Structure
- `requirements.txt:` Lists required Python dependencies.
- `main.py:` Main script to run the AI agents.
- `agents:` (Optional) Folder containing code for individual AI agents (market research, content strategy, etc.)
- `config.py:` (Optional) Configuration file for Crew AI project and API key.

## Contributing

We welcome contributions to enhance the functionality of the Smart Marketing Assistant. To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please open an issue in the repository or contact the project maintainers.

---

Thank you for using the Smart Marketing Assistant! We hope it helps you achieve your Instagram marketing goals.
