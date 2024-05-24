from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask import current_app

portal = Blueprint("portal", __name__)


@portal.route("/")
def home():
    return render_template("home.html")

@portal.route("/dashboard")
def dash():
    return render_template("dashboard.html")

@portal.route("/logs")
def logs_menu():
    OP = current_app.OnionPortal
    logs = ["Master"]
    for o in OP.onions.values():
        logs.append(o.name)
    return render_template("logs_menu.html", logs=logs)

@portal.route("logs/show/<name>")
def show_logs(name):
    print(name)
    if name == "Master":
        onion = current_app.OnionPortal
        logs = onion.showLogs()
    else:
        onion = current_app.OnionPortal.onions.get(name)
        logs = onion.torLogs
    log_name = onion.name
    
    return render_template("show_logs.html", log_name=log_name, logs=logs)

@portal.route("/portals", methods=["POST", "GET"])
def portals():
    OP = current_app.OnionPortal
    onions = OP.showOnions()
    if request.method == "POST":
        if request.form.get("Start"):
            OP.startPortals()
        elif request.form.get("Stop"):
            OP.stopPortals()
        return redirect(url_for('portal.portals_confirm'))
    return render_template("portals.html", onions=onions)

@portal.route("/portals/confirm")
def portals_confirm():
    return redirect(url_for('portal.portals'))

@portal.route("/portals/show/<name>", methods=["POST", "GET"])
def show_portal(name):
    onion = current_app.OnionPortal.onions.get(name)
    info = onion.info
    if request.method == "POST":
        if request.form.get("Start"):
            onion.START()
        elif request.form.get("Stop"):
            onion.stop()
        elif request.form.get("Circuit"):
            onion.newCircuit()
        return redirect(url_for("portal.show_portal_confirm", name=name))

    return render_template("show_portal.html", info=info)

@portal.route("/portals/show/confirm/<name>")
def show_portal_confirm(name):
    return redirect(url_for("portal.show_portal", name=name))

@portal.route("/add", methods=["POST", "GET"])
def add_portal():
    OP = current_app.OnionPortal
    ports = OP.extra_ports
    if request.method == "POST":
        port_num = request.form.get("port")
        OP.addOnion(port_num)
        return redirect(url_for("portal.add_portal_confirm"))
    return render_template("add_portal.html", ports=ports)

@portal.route("/add/confirm")
def add_portal_confirm():
    return redirect(url_for("portal.add_portal"))