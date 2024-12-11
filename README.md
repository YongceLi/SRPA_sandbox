# SRPA: Self-Reflective Preference Adaptation
## Abstract
With the rapid advancement of Large Language Models (LLMs) and their wide-ranging applications, there’s a growing interest in improving the efficiency and quality of interactions between humans and LLMs. Researchers are exploring ways to leverage LLMs' capabilities to better understand and adapt to user preferences, ultimately enhancing personalization and user experience during interactions. Traditional approaches, such as reinforcement learning, require fine-tuning each model to learn individual user preferences. However, achieving personalized experiences for each user through model fine-tuning is highly resource-intensive and requires collecting a preference dataset for each user. This raises the question: Can LLMs effectively learn a user's implicit preferences by reflecting on past conversations without training the model? In this paper, we propose Self-Reflective Preference Adaptation (SRPA), a training-free personalization framework that builds an external preference database from each user’s conversation history, guided by the LLM's self-reflection ability. This framework is lightweight, easy to integrate into any LLM-based chatbot, and designed to adapt to user preferences within just a few conversations. SRPA significantly improves conversational efficiency, reducing the average number of conversation turns required to achieve satisfactory outputs by up to 20% across user groups and consistently outperforming DPO or larger baseline models in alignment with user preferences.

## Setup
To initialize your environment and install necessary packages, use the following commands:

```bash
conda create -n <your_env_name> python=3.10
conda activate <your_env_name>
```
Set up your OpenAI API Key in your environment before running any OpenAI related models. 

## Evaluation
To run the evaluation on SRPA using role-players, generate questions for your roleplayers and create teh dataset.
The example dataset is in `synthetic_task_dataset.jsonl`. 
```bash
python runner.py 
    --data_path {your_dataset_path.jsonl
    --extract_threshold {preference_extraction_threshold}
    --update_threshold {preference_update_threshold}
    --no_preference {True for evaluating without SRPA}
```

## Interface
To use the interface for SRPA, run:
```bash
python app.py
```
If you want to share the interface to others, in last line:
```bash
demo.launch(share=True) # False for only run locally
```