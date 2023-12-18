# Lazy Student
## Retrieval Augmented Generation Pipeline for Interactive Learning
![alt text](assets/lazy_student.png)
### This repository will allow you to submit a machine learning whitepaper and engage in conversations to discuss the intricacies of the paper with an LLM. 

## Installation
### 1) Clone the repository
```
git clone git@github.com:rjgreen97/lazy_student.git
```
### 2) Install the requirements
```
pip3 install -r requirements.txt
```
### 3) Create an .env file
```
touch .env
```
### 4) Add your OpenAI API key to the .env file
#### Make sure to follow the format:
```
OPENAI_API_KEY=<your key here>
```

### 5) Move the desired whitepaper to the *knowledge_store* directory
- The whitepaper should be in PDF format
- For best results, there should only ever be one whitepaper in the *knowledge_store* directory
- It does not matter what the file is named

### 6) Allow the `begin_conversation.sh` script to be executed
```
chmod +x bin/begin_conversation.sh
```

### 7) Run the `begin_conversation.sh` script
```
bin/begin_conversation.sh
```

### *Optional* 8) Adjust the *base_prompt* located in `rag_pipeline/rag_config.py` 
- Depending on what you are looking to discuss, you may want to adjust the *base_prompt* to better suit your needs
