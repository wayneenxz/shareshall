import pandas as pd
import spacy

# Load spaCy's NLP model
nlp = spacy.load("en_core_web_sm")

# Load the dataset
wikileaks_df = pd.read_excel("wikileaks_parsed.xlsx")
news_excerpts_df = pd.read_excel("news_excerpts_parsed.xlsx")

# Function to extract named entities
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Apply entity extraction
wikileaks_df["Extracted Entities"] = wikileaks_df["Text"].apply(extract_entities)
news_excerpts_df["Extracted Entities"] = news_excerpts_df["Text"].apply(extract_entities)

# Save results
wikileaks_df.to_excel("wikileaks_entities.xlsx", index=False)
news_excerpts_df.to_excel("news_entities.xlsx", index=False)
print("✅ Entity extraction complete! Results saved as 'wikileaks_entities.xlsx' and 'news_entities.xlsx'.")
