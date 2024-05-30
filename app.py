from transformers import BertTokenizer

text = "This allows the model to handle complex words and misspellings while keeping the length of the inputs manageable."

# Character Tokenizer
char_tokenized_text = list(text)
print(char_tokenized_text)

# # Word Tokenizer
word_tokenized_text = text.split(' ')
print(word_tokenized_text)

# Subword Tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
subword_tokenized_text = tokenizer.tokenize(text)
print('subword_tokenized_text')