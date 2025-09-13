from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Page HTML avec Bootstrap
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Veille perso</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-4">
        <h1 class="mb-4">📰 Mes articles collecté</h1>
        {% if articles %}
            <div class="list-group">
                {% for a in articles %}
                    <a href="{{ a['url'] }}" target="_blank" class="list-group-item list-group-item-action">
                        <h5 class="mb-1">{{ a['title'] }}</h5>
                        <small class="text-muted">{{ a['date'] }} – {{ a['source'] }}</small>
                    </a>
                {% endfor %}
            </div>
        {% else %}
            <div class="alert alert-warning">Aucun article pour le moment.</div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_articles():
    conn = sqlite3.connect("articles.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, title TEXT, url TEXT, date TEXT, source TEXT)")
    cur.execute("SELECT title, url, date, source FROM articles ORDER BY date DESC LIMIT 50")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/")
def index():
    articles = get_articles()
    return render_template_string(TEMPLATE, articles=articles)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")
    print(f"Starting server on port {port} with debug={debug}")
    app.run(host="0.0.0.0", port=port, debug=True)
