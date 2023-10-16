from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__, template_folder='templates')
author = pickle.load(open('author.pkl', 'rb'))
sim_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
popular = pickle.load(open('popular.pkl', 'rb'))
books = pickle.load(open('pt.pkl', 'rb'))
data = pickle.load(open('data.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html',
                           book_name=list(popular['Book-Title'].values),
                           book_auth=list(popular['Book-Author'].values),
                           book_rat=list(popular['avg_rating'].values),
                           book_img=list(popular['Image-URL-M'].values),
                           book_numrat=list(popular['num_rating'].values))


@app.route('/rec_book')
def recommend_book_ui():
    return render_template('recommend.html')


@app.route('/Books', methods=['POST'])
def book():
    name = request.form.get('book_name')
    d = []
    if name != '':
        index = np.where(books.index == name)[0][0]
        similar = sorted(list(enumerate(sim_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        for i in similar:
            item = []
            temp_df = data[data['Book-Title'] == books.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            d.append(item)
    return render_template('recommend.html', data=d)


@app.route('/rec_auth')
def recommend_author_ui():
    return render_template('author.html')


@app.route('/Author', methods=['POST'])
def au_book():
    auth = request.form.get('book_auth')
    a = []
    if auth != '' and (auth in author['Book-Author'].values):
        for i in range(5):
            a.append([author[author['Book-Author'] == auth]['Book-Title'].values[i],
                      auth,
                      author[author['Book-Author'] == auth]['Image'].values[i],
                      author[author['Book-Author'] == auth]['avg_rating'].values[i]])
    return render_template('author.html', data=a)


if __name__ == '__main__':
    app.run(debug=True)
