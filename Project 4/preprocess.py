import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
import os
import string
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def preprocessing():
    directory = os.listdir('static/')
    print("dirs >>>>>>>>>>>>>>> ", directory)
    for files in directory:
        print(files)
        file = open("static/"+files, encoding="utf8")
        write_path = 'preprocessed/{}'.format(files)
        for line in file:
            line = line.lower()
            line = line.translate(str.maketrans('', '', string.punctuation))
            line = line.replace("’","")
            line = " ".join(line.split())
            swords = set(stopwords.words("english"))
            tokens = word_tokenize(line)
            filtered = [word for word in tokens if word not in swords]
            lemmatized = [lemmatizer.lemmatize(word,pos = 'v') for word in filtered]
            line = " ".join(lemmatized)
            line = line.replace("’","")
            write_file = open(write_path, 'a', encoding="utf8")
            write_file.write(line+ "\n")
            write_file.close()
    file.close()        

preprocessing()