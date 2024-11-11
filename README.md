# Generative Adventure Game

Introducing "The Adventure Game", a concept for the November 2024 "AWS Game Builder Challenge".  It's a text based, open ended, RPG (role playing game).  The game use generative models from Amazon Bedrock using the Converse API to build an AI agent that uses a graph data structure to maintain game state.

![Adventure Game](img/adventure-game.jpg)


For a more detailed overview of the project, including how to customize and update the game,please see this blog post: [My Generative Adventure Game](https://community.aws/content/2ogvbYrb6RzMIvNX3ZvQIYSBa9j/my-generative-adventure-game)

### Note on Cost:

> Running this project will incur costs that are NOT covered by AWS Free Tier (and may not be covered by AWS credits).  This project makes use of generative models through Amazon Bedrock, and depending on which model is used, the size of prompts and the number of turns, the cost will vary.  This project is not intended to be a cost effective way to run a game.  Please review the [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) page for more details.

### Note on Game Play (and Kids):

> This game uses generative AI, and as such the game state may not be consistent or predictable.  Caution should be used when playing this game, especially with sensitive topics or allowing children to play. It is not recommended to enter private information or allow children to play without adult supervision.

### Requirements

Before you move forward, be sure to have:
- A current Python development environment.
- An AWS Account configured for local development.
- Access to models in Amazon Bedrock.

### Running the project
For running the project, first you need to install the npm libraries by running:

```bash
git clone [repository-url]
cd [repository-name]
```

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.