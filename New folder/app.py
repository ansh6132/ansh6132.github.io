from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Path to the Excel file
EXCEL_FILE = 'data/tv_shows.xlsx'

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Sample TV show data
data = {
    'TV Show Name': ['Breaking Bad', 'Friends', 'Stranger Things'],
    'Genre': ['Drama', 'Comedy', 'Sci-fi'],
    'Rating': [9.5, 8.9, 8.7],
    'Viewership (Millions)': [10, 25, 18],
    'Year': [2013, 2004, 2019]
}

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a new Excel file if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

# Read data from Excel
def read_tv_shows():
    try:
        return pd.read_excel(EXCEL_FILE, engine='openpyxl')
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return pd.DataFrame()

# Save data to Excel
def save_tv_shows(df):
    try:
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
    except Exception as e:
        print(f"Error writing to Excel file: {e}")
@app.route('/')
def index():
    # Load TV show data
    tv_shows = read_tv_shows()

    # Convert to lists for passing to the graph
    show_names = tv_shows['TV Show Name'].tolist()
    ratings = tv_shows['Rating'].tolist()
    viewership = tv_shows['Viewership (Millions)'].tolist()

    return render_template('index.html', tv_shows=tv_shows.to_dict(orient='records'))

@app.route('/graph')
def graph():
    # Load TV show data
    tv_shows = read_tv_shows()

    # Convert to lists for the chart
    show_names = tv_shows['TV Show Name'].tolist()
    ratings = tv_shows['Rating'].tolist()
    viewership = tv_shows['Viewership (Millions)'].tolist()

    # Pass data to the graph template
    return render_template('graph.html', show_names=show_names, ratings=ratings, viewership=viewership)

@app.route('/add', methods=['POST'])
def add_show():
    # Get data from the form
    name = request.form['name']
    genre = request.form['genre']
    rating = float(request.form['rating'])
    viewership = float(request.form['viewership'])
    year = int(request.form['year'])
    
    # Load the current data
    tv_shows = read_tv_shows()

    # Append new show
    new_show = pd.DataFrame({
        'TV Show Name': [name],
        'Genre': [genre],
        'Rating': [rating],
        'Viewership (Millions)': [viewership],
        'Year': [year]
    })
    tv_shows = pd.concat([tv_shows, new_show], ignore_index=True)
    
    # Save back to the Excel file
    save_tv_shows(tv_shows)
    
    # Load TV show data
    tv_shows = read_tv_shows()
    # Convert to a list of dictionaries to pass to HTML
    tv_shows_list = tv_shows.to_dict(orient='records')
    return render_template('index.html', tv_shows=tv_shows_list)


if __name__ == '__main__':
    app.run(debug=True)
