from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadatabind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def listMenuItems(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)

    return render_template('menu.html', restaurant = restaurant, items = menuItems)

@app.route('/restaurants/<int:restaurant_id>/addNewMenuItem', methods = ['GET', 'POST'])
def addNewMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('listMenuItems', restaurant_id = restaurant_id))
    else:
        return render_template('addNewMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/editMenuItem', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    itemToEdit = session.query(MenuItem).filter_by(id = item_id).one()

    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['price']:
            itemToEdit.price = request.form['price']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        session.add(itemToEdit)
        session.commit()
        flash("Item edited!")
        return redirect(url_for('listMenuItems', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, item_id = item_id, item = itemToEdit)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/removeMenuItem', methods = ['Get','POST'])
def deleteMenuItem(restaurant_id, item_id):
    itemToDelete = session.query(MenuItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item deleted!")
        return redirect(url_for('listMenuItems', restaurant_id = restaurant_id))
    else:
        return render_template('deleteItem.html', restaurant_id = restaurant_id, item_id = item_id, item = itemToDelete)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    
    return jsonify(MenuItems = [item.serialize for item in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, item_id):
    menuItem = session.query(MenuItem).filter_by(id = item_id).one()
    return jsonify(menuItem.serialize)

if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
