from app import create_app,db

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# Optional: hook db to flask shell
@app.shell_context_processor
def make_shell_context():
    return {"db": db}