from flask import Flask, render_template, request
from database import create_connection, get_products_by_title, get_products, get_products_categories, get_products_by_category

app = Flask(__name__)

# Route home page
@app.route('/')
def index():
    connection = create_connection()
    try:
        products = get_products(connection)
        categories = get_products_categories(connection)
    except Exception as e:
        print(f"Error: {e}")
        products = []
        categories = []
    finally:
        connection.close()
    return render_template('index.html', products=products, categories=categories)

# Route search page
@app.route('/search', methods=['GET', 'POST'])
def search():
    connection = create_connection()
    try:
        if request.method == 'POST':
            title = request.form['title']
            products = get_products_by_title(connection, title)
        else:
            products = get_products_by_title(connection, "")
        categories = get_products_categories(connection)
    except Exception as e:
        print(f"Error: {e}")
        products = []
        categories = []
    finally:
        connection.close()
    return render_template('index.html', products=products, categories=categories)

# Route category page
@app.route('/category/<category>')
def category(category):
    connection = create_connection()
    try:
        products = get_products_by_category(connection, category)
        categories = get_products_categories(connection)
    except Exception as e:
        print(f"Error: {e}")
        products = []
        categories = []
    finally:
        connection.close()
    return render_template('index.html', products=products, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
