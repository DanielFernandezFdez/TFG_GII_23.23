from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def index():
    #return "¡Hola, mundo!"
    cursos=['php','python','java','javascript']
    data={
        'title':'Index',
        'message':'¡Saludos!',
        'cursos':cursos,
        'number':len(cursos)
    }
    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)