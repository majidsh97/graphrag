import nltk
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd

from .myutils import completion


def get_entity_seed(texts:list[str]):

    # Download the necessary resources from NLTK
    nltk.download('stopwords')
    nltk.download('punkt')

    # Example list of texts (you can replace this with your own list of texts)
    # Tokenize, clean, and count words in all texts
    stop_words = set(stopwords.words('english'))

    # Initialize an empty Counter to accumulate word counts
    total_word_counts = Counter()

    # Loop over each text in the list
    for text in texts:
        # Tokenize the text into words
        words = nltk.word_tokenize(text.lower())  # Convert to lower case for uniformity

        # Filter out stopwords and non-alphabetic words
        filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

        # Update the total word counts
        total_word_counts.update(filtered_words)

    # Filter words that appear at least twice
    entity_seed = {word: count for word, count in total_word_counts.items() if count >= 2}

    
    return entity_seed


def clean_entity_seed(entity_seed):
    #2. Filter out those that do not seem relevant to others. 
    #    2. Keep only one of duplicates or very similar entities like solder and soldering or hole and holes.

    prompt=\
    """You are given a list of candidate entities with their frequencies.

    Filter out those that are too general like conjuctions, auxiliary verbs or not a meaningful term i.e. not suitable for being an entity.
    
    Your output format should be the same as candidate entities.
    
    Candidate entities:
    {entity_seed}
    Filtered entities:
    """.format(entity_seed=entity_seed)
    print(prompt)
    return completion(prompt,"",True,temperature=0.7)



def get_matched_entity(text,entity_seed):
    words = set(nltk.word_tokenize(text.lower()) )
    print("words",words)
    entity_keys = set(entity_seed['entity'].str.lower())  
    print("entity_keys",entity_keys)
    matches = words.intersection(entity_keys)    
    print('matches',matches)
    return matches

def pipeline(texts):
    entity_seed = get_entity_seed(texts)
<<<<<<< HEAD
    entity_seed = clean_entity_seed(entity_seed)
=======
    #entity_seed = clean_entity_seed(entity_seed)
>>>>>>> 002a077 (entity seed)
    entity_seed = pd.DataFrame(entity_seed.items(), columns=["entity", "count"])
    entity_seed.to_parquet("entity_seed.parquet")
    
    return entity_seed

    
    
if __name__ == "__main__":
    texts = ["This is an example sentence", "Another example sentence"]
    entity_seed = pipeline(texts)
    matched = get_matched_entity(texts[0],entity_seed)
    print(matched)
    
    


    """
    from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep
    from graphrag.index.workflows.load import load_workflows
    from graphrag.index import run_pipeline, run_pipeline_with_config
    from graphrag.index.config import PipelineWorkflowReference

    workflows: list[PipelineWorkflowReference] = [
        PipelineWorkflowReference(
            steps=[
                {
                    # built-in verb
                    "verb": "derive",  # https://github.com/microsoft/datashaper/blob/main/python/datashaper/datashaper/verbs/derive.py
                    "args": {
                        "column1": "col1",  # from above
                        "column2": "col2",  # from above
                        "to": "col_multiplied",  # new column name
                        "operator": "*",  # multiply the two columns
                    },
                    # Since we're trying to act on the default input, we don't need explicitly to specify an input
                }
            ]
        ),
    ]

    workflows = load_workflows(workflow_config)
    print(workflows)"""
    
    