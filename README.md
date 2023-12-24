# Lazy Student
## Retrieval Augmented Generation Pipeline for Interactive Learning
<img src="assets/lazy_student.png" alt="drawing" width="400"/>

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
### 3) Create an .env file and add your OpenAI API key
```
touch .env
```
### be sure to follow the format:
```
OPENAI_API_KEY=<your key here>
```


### 4) Run the `run.sh` script
```
bin/run.sh
```

### *Optional* Adjust the *base_prompt* located in `src/rag_config.py` 
- Depending on what you are looking to discuss, you may want to adjust the *base_prompt* to better suit your needs
