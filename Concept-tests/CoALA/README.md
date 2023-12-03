# COALA - CO-gnitive Achitecture for Language Agents

This is an implementation of a language agent following the CoALA paper is an autonomous AI system that utilizes Google's generative AI (PalM2) to understand and interact with the world. It uses JSON files to store its thoughts and memory, and periodically generates new thoughts based on its current state.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- Google's generative AI (PalM2) API key

### Installation

1. Clone the repository
2. Install the required Python packages:

3. Create a `.env` file in the root directory and add your Google API key:

### Usage

To start the AI, run the `main.py` script:

The AI will initialize its memory and thoughts from the `memory.json` and `thoughts.json` files respectively. It will then enter a loop where it waits for user input, processes it, and responds.

## Project Structure

The project is mainly composed of two Python scripts:

- `main.py`: This is the main script that runs the AI. It defines the COALA class which handles the AI's memory, thoughts, and interactions with the user.

- `consiousness_thinking.py`: This script is responsible for generating new thoughts for the AI. It runs in a separate thread and periodically generates new thoughts based on the AI's current state.

The AI's memory and thoughts are stored in two JSON files:

- `memory.json`: This file stores the AI's working and long-term memory.

- `thoughts.json`: This file stores the AI's current thoughts.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## COALA Paper

For a detailed understanding of the concepts and methodologies used in the development of COALA, please refer to our paper available on arXiv. You can access the paper at [this link](https://arxiv.org/abs/2309.02427).


## Pause Notice.
In my dvelopments in this direction i have found nee to first put a pause to this particular approach and firstly understand the ACE (Autonomous Cognitive Entities).   
this a framework for designing ethical artificial general intelligence systems based on a layered cognitive architecture, systems much like A.L.F.I.E (Artificial LifeForm Intelligent Entity), meanwhile the same paper implements a system (stacey) with interfaces like the we and discord.  

In the meantime we are going to focus on anothe paper(Conceptual Framework for Autonomous Cognitive Entities by David Shapiro). the paper focuses mainly on implementing an ACE based system. we'll be linking the source code in this readme when ready.