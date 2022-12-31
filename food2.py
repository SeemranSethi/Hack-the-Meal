from flask import *
import os
from werkzeug.utils import secure_filename
import label_image
import requests

def load_image(image):
    text = label_image.main(image)
    return text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    print(request.method)
    if request.method == 'POST':
        print("on the top of if")
        # Get the file from post request
        f = request.files['file']
        file_path = secure_filename(f.filename)
        f.save(file_path)
        # Make prediction
        result = load_image(file_path)
        result = result.title()
        #d = {"Ice Cream":"🍨",'Fried Rice':"🍚","Pizza":"🍕","Sandwich":"🥪","Samosa":"🌭"}
        #result = result+d[result]
        print(result)

        ingredient_name = result.lower().replace(" ","%20")
        ingrdts = requests.get("https://www.themealdb.com/api/json/v1/1/filter.php?i="+ingredient_name)
        ingredient = ingrdts.json()
        meal_name = ingredient["meals"][0]["strMeal"]
        recid = ingredient["meals"][0]["idMeal"]
        recipe_url = requests.get("https://www.themealdb.com/api/json/v1/1/lookup.php?i="+recid)
        recform = recipe_url.json()
        recipe = "<h3><b class='fs-2'><i>Ingredient identified : </i></b></h3>" + result + "<br><br><h2>" + meal_name + "</h2><br><h3 style='border:white 3px solid'><b class='fs-2'><i>Ingredients</i></b> : </h3><br>"
        for i in range(1,21):
            if(recform["meals"][0]["strIngredient"+str(i)]=="" or recform["meals"][0]["strIngredient"+str(i)]=="null" or recform["meals"][0]["strIngredient"+str(i)]==" "):
                continue
            recipe = recipe + recform["meals"][0]["strIngredient"+str(i)] + " (" + recform["meals"][0]["strMeasure"+str(i)] + ")<br>"
        recipe = recipe + "<hr><h3 style='border:white 3px solid'><b class='fs-2'><i>Recipe</i></b> : </h3><br>" + recform["meals"][0]["strInstructions"]
        print(file_path)
        print(recipe)
        os.remove(file_path)
        print(recipe)
        return recipe
    return None

if __name__ == '__main__':
    app.run()