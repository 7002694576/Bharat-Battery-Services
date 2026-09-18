from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# =========================
# MONGODB
# =========================

client = MongoClient("mongodb://127.0.0.1:27017/")

db = client["Bharat_Battery_DB"]

orders_collection = db["orders"]
products_collection = db["products"]


# =========================
# IMAGE UPLOAD SETTINGS
# =========================

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================
# DEFAULT PRODUCTS
# =========================

default_products = [

    {
        "name": "TG400L",
        "category": "Car Battery",
        "capacity": "35 Ah",
        "price": "₹3,835",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "SLV DIN44R",
        "category": "Car Battery",
        "capacity": "44 Ah",
        "price": "₹5,447",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "PREMIO 55D23L",
        "category": "Car Battery",
        "capacity": "54 Ah",
        "price": "₹5,723",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "TGZ4 ADV",
        "category": "Two-Wheeler",
        "capacity": "3 Ah",
        "price": "₹1,182",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "YTZ7",
        "category": "Two-Wheeler",
        "capacity": "6 Ah",
        "price": "₹1,850",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "TG7D",
        "category": "Two-Wheeler",
        "capacity": "7 Ah",
        "price": "₹1,654",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "YTZ5",
        "category": "Two-Wheeler",
        "capacity": "4 Ah",
        "price": "₹1,395",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "TATA Green 150 Ah",
        "category": "Inverter Battery",
        "capacity": "150 Ah",
        "price": "Contact for Price",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "TATA Green 200 Ah",
        "category": "Inverter Battery",
        "capacity": "200 Ah",
        "price": "Contact for Price",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "Home Inverter Battery",
        "category": "Inverter Battery",
        "capacity": "12V Battery",
        "price": "Contact for Price",
        "warranty": "Warranty Available",
        "image": "tg400l.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "Home Inverter 800 VA",
        "category": "Inverter",
        "capacity": "800 VA",
        "price": "Contact for Price",
        "warranty": "Warranty Available",
        "image": "inv.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "Home Inverter 1100 VA",
        "category": "Inverter",
        "capacity": "1100 VA",
        "price": "Contact for Price",
        "warranty": "Warranty Available",
        "image": "inv.png",
        "active": True,
        "created_at": datetime.now()
    },

    {
        "name": "Home Inverter 1500 VA",
        "category": "Inverter",
        "capacity": "1500 VA",
        "price": "Contact for Price",
        "warranty": "Warranty Available",
        "image": "inv.png",
        "active": True,
        "created_at": datetime.now()
    }
]


# =========================
# SEED PRODUCTS
# =========================

def seed_products():

    count = products_collection.count_documents({})

    if count == 0:

        products_collection.insert_many(
            default_products
        )

        print("13 existing products added to MongoDB.")

    else:

        print(f"Products already exist: {count}")


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    products = list(
        products_collection.find(
            {
                "active": {
                    "$ne": False
                }
            }
        ).sort("_id", 1)
    )

    car_products = []
    bike_products = []
    inverter_battery_products = []
    inverter_products = []

    for product in products:

        category = product.get(
            "category",
            ""
        )

        if category == "Car Battery":

            car_products.append(product)

        elif category == "Two-Wheeler":

            bike_products.append(product)

        elif category == "Inverter Battery":

            inverter_battery_products.append(
                product
            )

        elif category in [
            "Inverter",
            "Home Inverter"
        ]:

            inverter_products.append(
                product
            )

    return render_template(
        "index.html",
        car_products=car_products,
        bike_products=bike_products,
        inverter_battery_products=inverter_battery_products,
        inverter_products=inverter_products
    )


# =========================
# TEST DATABASE
# =========================

@app.route("/test-db")
def test_db():

    try:

        client.admin.command("ping")

        return "MongoDB Connected Successfully!"

    except Exception as e:

        return f"MongoDB Connection Error: {e}"


# =========================
# PLACE ORDER
# =========================

@app.route(
    "/place-order",
    methods=["POST"]
)
def place_order():

    try:

        data = request.get_json()

        order = {

            "product": data.get(
                "product",
                ""
            ),

            "name": data.get(
                "name",
                ""
            ),

            "mobile": data.get(
                "mobile",
                ""
            ),

            "address": data.get(
                "address",
                ""
            ),

            "price": data.get(
                "price",
                ""
            ),

            "status": "Pending",

            "order_date": datetime.now()
        }

        orders_collection.insert_one(
            order
        )

        return jsonify({

            "success": True,

            "message":
                "Order saved successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
def admin():

    orders = list(
        orders_collection.find().sort(
            "order_date",
            -1
        )
    )

    products = list(
        products_collection.find().sort(
            "_id",
            -1
        )
    )

    return render_template(
        "admin.html",
        orders=orders,
        products=products
    )


# =========================
# ADD PRODUCT
# =========================

@app.route(
    "/admin/add-product",
    methods=["POST"]
)
def add_product():

    try:

        image_path = request.form.get(
            "old_image",
            ""
        ).strip()

        image_file = request.files.get(
            "image_file"
        )

        if (
            image_file
            and image_file.filename
        ):

            if allowed_file(
                image_file.filename
            ):

                filename = secure_filename(
                    image_file.filename
                )

                image_file.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )

                image_path = (
                    "uploads/" + filename
                )

        product = {

            "category": request.form.get(
                "category",
                ""
            ).strip(),

            "name": request.form.get(
                "name",
                ""
            ).strip(),

            "capacity": request.form.get(
                "capacity",
                ""
            ).strip(),

            "price": request.form.get(
                "price",
                ""
            ).strip(),

            "warranty": request.form.get(
                "warranty",
                ""
            ).strip(),

            "image": image_path,

            "active": True,

            "created_at": datetime.now()
        }

        products_collection.insert_one(
            product
        )

        return redirect("/admin")

    except Exception as e:

        return f"Product Add Error: {e}"


# =========================
# EDIT PRODUCT
# =========================

@app.route(
    "/admin/edit-product",
    methods=["POST"]
)
def edit_product():

    try:

        product_id = request.form.get(
            "product_id"
        )

        old_image = request.form.get(
            "old_image",
            ""
        ).strip()

        image_path = old_image

        image_file = request.files.get(
            "image_file"
        )

        if (
            image_file
            and image_file.filename
        ):

            if allowed_file(
                image_file.filename
            ):

                filename = secure_filename(
                    image_file.filename
                )

                image_file.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )

                image_path = (
                    "uploads/" + filename
                )

        products_collection.update_one(

            {
                "_id": ObjectId(
                    product_id
                )
            },

            {
                "$set": {

                    "category":
                        request.form.get(
                            "category",
                            ""
                        ).strip(),

                    "name":
                        request.form.get(
                            "name",
                            ""
                        ).strip(),

                    "capacity":
                        request.form.get(
                            "capacity",
                            ""
                        ).strip(),

                    "price":
                        request.form.get(
                            "price",
                            ""
                        ).strip(),

                    "warranty":
                        request.form.get(
                            "warranty",
                            ""
                        ).strip(),

                    "image":
                        image_path,

                    "updated_at":
                        datetime.now()
                }
            }
        )

        return redirect("/admin")

    except Exception as e:

        return f"Product Edit Error: {e}"


# =========================
# UPDATE ORDER STATUS
# =========================

@app.route(
    "/admin/update-order-status/<order_id>",
    methods=["POST"]
)
def update_order_status(order_id):

    try:

        status = request.form.get(
            "status",
            "Pending"
        )

        allowed_statuses = [
            "Pending",
            "Confirmed",
            "Delivered",
            "Cancelled"
        ]

        if status not in allowed_statuses:

            return "Invalid Order Status"

        orders_collection.update_one(

            {
                "_id": ObjectId(
                    order_id
                )
            },

            {
                "$set": {

                    "status": status,

                    "status_updated_at":
                        datetime.now()
                }
            }
        )

        return redirect("/admin")

    except Exception as e:

        return f"Order Status Update Error: {e}"


# =========================
# DELETE PRODUCT
# =========================

@app.route(
    "/admin/delete-product/<product_id>",
    methods=["POST"]
)
def delete_product(product_id):

    try:

        products_collection.delete_one({

            "_id": ObjectId(
                product_id
            )

        })

        return redirect("/admin")

    except Exception as e:

        return f"Product Delete Error: {e}"


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    seed_products()

    app.run(
        debug=True
    )

