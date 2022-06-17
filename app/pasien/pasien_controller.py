from flask import *
from app.pasien_history import pasien_history_controller
from app.pasien.pasien_model import pasien
from app.auth.auth_model import auth
from app.trans import trans_model
from app.auth import auth_controller
from app import db, pd, BytesIO
import datetime
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

# This file is work for setting the function

# The function below work for showing the active data on the database.
def viewPasien():
    rows = pasien.query.filter(pasien.flag=="Y").all()
    return render_template("pasien/pasien.html", datas=rows, username=current_user)
    db.session.close()

# The function below work for adding data to the database.
# This function use form to get value form the website.
def addPasien():
    username = request.form.get("username")
    password = request.form.get("password")
    nama_pasien = request.form.get("namaPasien")
    alamat_pasien = request.form.get("alamatPasien")
    date = datetime.datetime.now()
    created_date = date
    updated_date = date
    newUser = auth(username=username, status_auth='pasien', password=generate_password_hash(password, method='sha256'), flag="Y", created_date=date, updated_date=date)
    db.session.add(newUser)
    db.session.commit()
    id = auth_controller.findAuth(username)
    saveAdd = pasien(id_auth=id, username=username, password=password, nama_pasien=nama_pasien, alamat_pasien=alamat_pasien, flag="Y", status_diperiksa="N", created_date=created_date, updated_date=updated_date)
    db.session.add(saveAdd)
    db.session.commit()
    flash("Data Successfully Added.")
    return redirect(url_for('pasien_bp.viewPasien'))
    db.session.close()

# The function belom work for update / edit data on the database.
# This function use form to get value form the website.
def editPasien(idPasien):
    nama_pasien = request.form.get("namaPasien")
    alamat_pasien = request.form.get("alamatPasien")
    date = datetime.datetime.now()
    updated_date = date
    data = checkDataPasien(idPasien)
    username = current_user.username
    if "Ada" == data:
        flash("Data Tidak dapat diupdate. Data Pasien sedang dalam Transaksi.")
    else:
        saveEdit = pasien.query.filter(pasien.no_pasien == idPasien).first()
        pasien_history_controller.addPasienHistory(username, idPasien, saveEdit.nama_pasien, saveEdit.alamat_pasien, updated_date)
        saveEdit.nama_pasien = nama_pasien
        saveEdit.username = username
        saveEdit.alamat_pasien = alamat_pasien
        saveEdit.updated_date = updated_date
        saveEdit.flag = "Y"
        db.session.commit()
        flash("Data Successfully Updated.")
    return redirect(url_for('pasien_bp.viewPasien'))
    db.session.close()

# The function below work for change flag and didnt deleting data from the database, just change flag from "Y" to "N"
# This function using data id from the website.
def deletePasien(idPasien):
    data = checkDataPasien(idPasien)
    if "Ada" == data:
        flash("Data Tidak dapat dihapus. Data Pasien sedang dalam Transaksi.")
    else:
        saveEdit = pasien.query.filter(pasien.no_pasien==idPasien).first()
        saveEdit.flag = "N"
        saveEdit.updated_date = datetime.datetime.now()
        db.session.commit()
    return redirect(url_for('pasien_bp.viewPasien'))
    db.session.close()

# The function below work for searching data from the website and showing active data from database.
# This function using form to get value from the website.
def searchPasien():
    idPasien = request.form.get("idPasien")
    namaPasien = request.form.ger("namaPasien")
    if idPasien == "":
        idPasien = "%"
    else:
        idPasien = idPasien
    if namaPasien == "":
        namaPasien = "%"
    else:
        namaPasien = "%" + namaPasien + "%"
    searchPasien = pasien.query.filter(pasien.id_pasien.like(idPasien), pasien.nama_pasien.like(namaPasien), pasien.flag=="Y").all()
    return render_template("pasien.html", datas=rows, username=current_user)

# The function below work for checking data from the database that has specified id.
# When data showing value Y, the status changed into Ada therefore status changed into Tidak when data showing N value.
def checkDataPasien(uid):
    rows = pasien.query.filter(pasien.no_pasien==uid).first()
    if rows.status_diperiksa == "Y":
        status = "Ada"
    elif rows.status_diperiksa == "N":
        status = "Tidak"
    return status

# The function below work for import data from xlsx file and added data to the database.
# This function use xlsx file with predefined templates.
def importFilePasien():
    if request.method == 'POST':
        f = request.files['file']
        data_xls = pd.read_excel(f)
        created_date = datetime.datetime.now()
        updated_date = datetime.datetime.now()
        for i in range(len(data_xls)):
            nama_pasien = data_xls.loc[i][1]
            alamat_pasien = data_xls.loc[i][2]
            username = data_xls.loc[i][3]
            password = data_xls.loc[i][4]
            newUser = auth(username=username, status_auth='pasien', password=generate_password_hash(password, method='sha256'), flag="Y", created_date=created_date, updated_date=updated_date)
            db.session.add(newUser)
            db.session.commit()
            id = auth_controller.findAuth(username)
            saveAdd = pasien(id_auth=id, username=username, password=password, nama_pasien=nama_pasien, alamat_pasien=alamat_pasien, status_diperiksa="N", flag="Y", created_date=created_date, updated_date=updated_date)
            db.session.add(saveAdd)
            db.session.commit()
        return redirect(url_for('pasien_bp.viewPasien'))
    return render_template("pasien/pasien.html", username=current_user)

# The function below work for export template for adding data to the database.
# This function export xlsx file.
def downloadTemplatePasien():
    df_1 = pd.DataFrame(columns=['Nama Pasien', 'Alamat Pasien', 'Username', 'Password'])
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_1.to_excel(writer, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    format = workbook.add_format()
    format.set_bg_color('#eeeeee')
    worksheet.set_column(0,2)
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename="Template_Pasien.xlsx", as_attachment=True)
    con.close()

def searchPasien():
    no_pasien = request.form.get("noPasien")
    nama_pasien = request.form.get("namaPasien")
    if no_pasien == "":
        no_pasien = "%"
    else:
        no_pasien = no_pasien
    if nama_pasien == "":
        nama_pasien = "%"
    else:
        nama_pasien = "%" + nama_pasien + "%"
    rows = pasien.query.filter(pasien.no_pasien.like(no_pasien), pasien.nama_pasien.like(nama_pasien), pasien.flag=="Y").all()
    return render_template("pasien/pasien.html", datas = rows, username=current_user)
    db.session.close()