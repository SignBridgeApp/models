from flask import Flask, render_template_string, request, redirect
import os
import json

app = Flask(__name__, static_folder='gifs')

with open("data.json") as f:
    data = json.load(f)

if os.path.exists("selected.json"):
    with open("selected.json") as f:
        user_selections = json.load(f)
else:
    user_selections = {}


@app.route('/')
def display_gif():
    if len(user_selections) == len(data):
        return "Done"

    tmp = data[len(user_selections)]
    ids = [file for file in tmp["ids"] if os.path.isfile("gifs/"+file+".gif")]
    print(ids)
    return render_template_string(HTML, gloss=tmp["gloss"], ids=ids, msg=f"{len(user_selections)}/{len(data)}")


@app.route('/record_selection')
def record_selection():
    gloss = request.args['gloss']
    selected_id = request.args['id']

    user_selections[gloss] = selected_id
    with open("selected.json", "w") as f:
        json.dump(user_selections, f, indent=4)

    print(user_selections)
    return redirect("/")


HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>{{ gloss }}</title>
    <script>
      function selectGif(id, gloss) {
        window.location.href = "/record_selection?gloss=" + gloss + "&id=" + id;
      }
    </script>
  </head>
  <body>
    <h2>{{ gloss }} &nbsp; {{ msg }}</h2>

    {% for id in ids %}
    <img
      src="/gifs/{{ id }}.gif"
      alt="{{ id }}"
      width="500"
      style="border: 1px solid black; cursor: pointer"
	  onclick="selectGif('{{ id }}', '{{ gloss }}')"
    />
    {% endfor %}

  </body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
