from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Pet
import mysql.connector
from django.conf import settings
from django.shortcuts import redirect

mydb = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )

# Create your views here.
@login_required
def pet_page(request):
    if request.method == 'POST':
        name = request.POST.get('name2')
        breed = request.POST.get('breed2')
        species = request.POST.get('species2')
        age = request.POST.get('age2')

        cursor = mydb.cursor()
        cursor.execute("INSERT INTO pets (name, breed, species, age) VALUES (%s, %s, %s,%s)", (name, breed, species, age))
        mydb.commit()

        return redirect('pet_page')
    
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    return render(request, 'pet_page.html', {'pets': pets})

@login_required
def sort_pet(request):
    name = request.GET.get('name')
    breed = request.GET.get('breed')
    species = request.GET.get('species')
    age = request.GET.get('age')
    adopted_needs_home = request.GET.get('adopted_needs_home')
    adopted_adopted = request.GET.get('adopted_adopted')
    
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM pets WHERE 1=1"  # Starting with a basic query
    
    # Adding filters based on provided criteria
    if name:
        query += f" AND name LIKE '%{name}%'"
    if breed:
        query += f" AND breed LIKE '%{breed}%'"
    if species:
        query += f" AND species LIKE '%{species}%'"
    if age:
        query += f" AND age = {age}"
    if adopted_needs_home:
        query += f" AND adoptered = 0"
    if adopted_adopted:
        query += f" AND adoptered = 1"
    
    cursor.execute(query)
    pets = cursor.fetchall()

    return render(request, 'pet_page.html', {'pets': pets})

@login_required
def delete_pet(request, pet_id):
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM pets WHERE pet_id = %s", (pet_id,))
    mydb.commit()

    return redirect('pet_page')


@login_required
def edit_pet(request, pet_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        breed = request.POST.get('breed')
        species = request.POST.get('species')
        age = request.POST.get('age')

        cursor = mydb.cursor()
        cursor.execute("UPDATE pets SET name=%s, breed=%s, species=%s, age=%s WHERE pet_id=%s", (name, breed, species, age, pet_id))
        mydb.commit()

        return redirect('pet_page')
    
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets WHERE pet_id = %s", (pet_id,))
    pet = cursor.fetchone()

    return render(request, 'edit_pet.html', {'pet': pet})

