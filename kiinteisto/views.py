# views.py

from django.shortcuts import render, HttpResponse
import requests
import json
import csv

from django.contrib import messages


def lookup(request):

    result_line = []
    fin_address = []
    

    if request.method == 'POST':
        tunnus = request.POST.get('tunnus')
        first_three_digits = tunnus.split("-")
        first_three_digits = first_three_digits[0]

        with open('staticfiles/kiinteistot/osoitteet.txt', encoding="latin-1") as f:
            for num, line in enumerate(f):
                if num < 2650808 and int(first_three_digits) >= 686:
                    continue
                elif num < 1750000 and int(first_three_digits) >= 425:
                    continue
                elif num < 729790 and int(first_three_digits) >= 178:
                    continue
                else: 
                    result_line = search_for_address(tunnus, line)
                    if result_line:
                        break;
        searchData = {}

        if result_line:
            fin_add, street_num, post_num, north_coord, east_coord, city = printing_address_info(result_line)
            searchData['address'] = fin_add
            searchData['street'] = street_num
            searchData['postnumber'] = post_num
            searchData['northcoord'] = north_coord
            searchData['eastcoord'] = east_coord
            searchData['city'] = city
            print (north_coord)
            print (east_coord)
            fin_address.append(searchData)
        else:
            fin_address.append("EI HAKUTULOSTA")

    #return render(request, 'kiinteisto/main.html')
    return render(request, 'kiinteisto/main.html', {'show': fin_address})

def search_for_address(tunnus, line):

    lopullinen_tunnus = []
    sliced_line = line.split(";")
    tunnus_sliced = tunnus.split("-")
    if len(tunnus_sliced[0]) == 2:
        lopullinen_tunnus.append("0")
        lopullinen_tunnus.append(tunnus_sliced[0])
    elif len(tunnus_sliced[0]) == 1:
        lopullinen_tunnus.append("00")
        lopullinen_tunnus.append(tunnus_sliced[0])
    else: 
        lopullinen_tunnus.append(tunnus_sliced[0])

    if len(tunnus_sliced[1]) == 2:
        lopullinen_tunnus.append("0")
        lopullinen_tunnus.append(tunnus_sliced[1])
    elif len(tunnus_sliced[1]) == 1:
        lopullinen_tunnus.append("00")
        lopullinen_tunnus.append(tunnus_sliced[1])
    else: 
        lopullinen_tunnus.append(tunnus_sliced[1])

    if len(tunnus_sliced[2]) == 3:
        lopullinen_tunnus.append("0")
        lopullinen_tunnus.append(tunnus_sliced[2])
    elif len(tunnus_sliced[2]) == 2:
        lopullinen_tunnus.append("00")
        lopullinen_tunnus.append(tunnus_sliced[2])
    elif len(tunnus_sliced[2]) == 1:
        lopullinen_tunnus.append("000")
        lopullinen_tunnus.append(tunnus_sliced[2])
    else: 
        lopullinen_tunnus.append(tunnus_sliced[2])

    if len(tunnus_sliced[3]) == 3:
        lopullinen_tunnus.append("0")
        lopullinen_tunnus.append(tunnus_sliced[3])
    elif len(tunnus_sliced[3]) == 2:
        lopullinen_tunnus.append("00")
        lopullinen_tunnus.append(tunnus_sliced[3])
    elif len(tunnus_sliced[3]) == 1:
        lopullinen_tunnus.append("000")
        lopullinen_tunnus.append(tunnus_sliced[3]) 
    else:
        lopullinen_tunnus.append(tunnus_sliced[3]) 

    str_lopullinen_tunnus = ''.join(lopullinen_tunnus)
    
    if str_lopullinen_tunnus == sliced_line[14]:
        return sliced_line

def printing_address_info(result_line):

    address_name_fin = result_line[7]
    address_name_swe = result_line[8]
    street_number = result_line[9]
    post_number = result_line[10]
    north_coord = result_line[4]
    east_coord = result_line[5]
    city = result_line[1]
    city_rows = analyse_city_file(city)
    city_name = city_rows[1]

    finnish_address = address_name_fin + " " + street_number + " " + post_number 
    swedish_address = address_name_swe + street_number + post_number 

    #return finnish_address, swedish_address
    return address_name_fin, street_number, post_number, north_coord, east_coord, city_name

def stats(request):
    x_row = []
    tunnus_with_zeroes = ""
    city_number = ""
    city_rows = []
    lines = []
    real_estate_in_town = 0;

    if request.method == 'POST':
        tunnus = request.POST.get('tunnus')
        first_three_digits = tunnus.split("-")
        first_three_digits = first_three_digits[0]
        tunnus_with_zeroes = add_zeroes_to_id(tunnus)

        with open('staticfiles/kiinteistot/osoitteet.txt', encoding="latin-1") as f:
            lines = f.readlines()
            c = csv.reader(lines, delimiter=';')
            
            try:
                x = findexcept(c, 14, tunnus_with_zeroes)
                print(x)
                x_row = x
                real_estate_in_town = find_amount_of_towns(c, 1, x_row[1])

            except ValueError as ve:
                print('Error: {}'.format(ve))


        if x_row[1]:
            city_number = x_row[1]
            city_rows = analyse_city_file(city_number)
            city_name = city_rows[1]    
            printables = []
            data_to_print = {}
            data_to_print['city_name'] = city_rows[0]
            data_to_print['swe_name'] = city_rows[1]
            data_to_print['state'] = city_rows[3]
            data_to_print['amount_of_r_state'] = real_estate_in_town
            printables.append(data_to_print)
    


    if city_rows:
        return render(request, 'kiinteisto/stats.html', {'show': printables})
    else:
        return render(request, 'kiinteisto/stats.html')

def find(reader, col, val):
    for row in reader:
        if row[col] == val:
            return row
    raise ValueError('Value {} not found in row {}'.format(val, col))


def findexcept(reader, col, val):
    r = find(reader, col, val)
    r.pop(col)
    return r

def find_amount_of_towns(reader, col, val):
    amount = 0
    for row in reader:
        if row[col] == val:
            amount += 1
    return amount

def add_zeroes_to_id(tunnus):
    
    lopullinen_tunnus = []
    tunnus_sliced = tunnus.split("-")

    if len(tunnus_sliced[0]) == 2:
        lopullinen_tunnus.append("0")
        lopullinen_tunnus.append(tunnus_sliced[0])
    elif len(tunnus_sliced[0]) == 1:
        lopullinen_tunnus.append("00")
        lopullinen_tunnus.append(tunnus_sliced[0])
    else: 
        lopullinen_tunnus.append(tunnus_sliced[0])

    if len(tunnus_sliced[1]) == 2:
        lopullinen_tunnus.append("0")
        lopullinen_tunnus.append(tunnus_sliced[1])
    elif len(tunnus_sliced[1]) == 1:
        lopullinen_tunnus.append("00")
        lopullinen_tunnus.append(tunnus_sliced[1])
    else: 
        lopullinen_tunnus.append(tunnus_sliced[1])

    if len(tunnus_sliced[2]) == 3:
        lopullinen_tunnus.append("0")
        lopullinen_tunnus.append(tunnus_sliced[2])
    elif len(tunnus_sliced[2]) == 2:
        lopullinen_tunnus.append("00")
        lopullinen_tunnus.append(tunnus_sliced[2])
    elif len(tunnus_sliced[2]) == 1:
        lopullinen_tunnus.append("000")
        lopullinen_tunnus.append(tunnus_sliced[2])
    else: 
        lopullinen_tunnus.append(tunnus_sliced[2])

    if len(tunnus_sliced[3]) == 3:
        lopullinen_tunnus.append("0")
        lopullinen_tunnus.append(tunnus_sliced[3])
    elif len(tunnus_sliced[3]) == 2:
        lopullinen_tunnus.append("00")
        lopullinen_tunnus.append(tunnus_sliced[3])
    elif len(tunnus_sliced[3]) == 1:
        lopullinen_tunnus.append("000")
        lopullinen_tunnus.append(tunnus_sliced[3]) 
    else:
        lopullinen_tunnus.append(tunnus_sliced[3]) 

    str_lopullinen_tunnus = ''.join(lopullinen_tunnus)
    
    return str_lopullinen_tunnus

def analyse_city_file(city_number):
    row_list_x = []
    with open('staticfiles/kiinteistot/kunnat.csv') as f:
        lines = (line.strip() for line in f)
        c = csv.reader(lines, delimiter=';')

        try:
            x = findexcept(c, 0, city_number)
            print(x , "we are at analyse_city_file")
            row_list_x = x
            
        except ValueError as ve:
            print('Error: {}'.format(ve))

    return row_list_x
     