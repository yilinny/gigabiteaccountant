import gspread
from gspread.models import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from datetime import date

scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scopes)
client = gspread.authorize(creds)


def store_data(data, sheet_name):
    sheet = client.open(sheet_name).sheet1
    sheet.append_row(data)

def store_variable(variable, contact,column,sheet_name):
    sheet = client.open(sheet_name).sheet1
    cell = sheet.find(str(contact))
    row = cell.row
    sheet.update_cell(row, column, variable)

def store_expenses(var, column, comments):
    sheet= client.open('finance').worksheet('Personal Expenses')
    a = date.today().strftime("%d/%m/%y")
    data= [a, '', '', '', comments]
    data[column] = var
    sheet.append_row(data)

def store_invoice(var, company):
    sheet= client.open('Food supplier + packaging').worksheet(company)
    sheet.append_row(var)

def store_delivery(var):
    sheet= client.open('finance').worksheet('delivery cost')
    sheet.append_row(var)

