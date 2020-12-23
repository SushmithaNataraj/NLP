# Testing file
import spacy
nlp = spacy.load("en_core_web_md")


doc = nlp("My name is Sushmitha. A Salt Lake city, United States middle school in Liverpool, Nova Scotia is pumping up bodies as well as minds. IBM is a big IT company")
entities = {}
for token in doc:
    print("The token is :",token.text, ".** The parts of speech", token.pos_)
#     pass

for ent in doc.ents:
    entities[ent] = ent.label_
    

print(spacy.explain("GPE"))
# print("IN ", spacy.explain("IN"))

print(entities)

# # df = pd.DataFrame("Entities:", entities, "Labels:", labels)
# print(df)