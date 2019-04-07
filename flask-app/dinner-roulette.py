from app import create_app, db

app = create_app()


@app.before_first_request
def create_tables():
    db.create_all()


app.run(port=5000, debug=False)
