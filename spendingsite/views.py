from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from .models import Transaction

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
daysMonths = [31, 28, 31, 30, 31,30, 31, 31, 30, 31, 30, 31]
categories = ['Rent', 'Utilities', 'Food', 'Health', 'Recreation', 'Miscellaneous', 'Transportation']

date = datetime.today()

def index(request):

    year = int(date.strftime('%Y'))
    month = months[int(date.strftime('%m')) - 1]
    daysPrevMonth = daysMonths[int(date.strftime('%m')) - 2]
    days = daysMonths[int(date.strftime('%m')) - 1]
    daysNextMonth = daysMonths[int(date.strftime('%m'))]
    day = int(date.strftime('%d'))

    monthStartDate = datetime(year, int(date.strftime('%m')) - 1, daysPrevMonth)
    monthEndDate = datetime(year, int(date.strftime('%m')), days)

    query = Transaction.objects.raw("""
        SELECT id, SUM(price) as monthTotal FROM spendingsite_transaction
        WHERE date BETWEEN %s and %s
        GROUP BY id
    """, [monthStartDate, monthEndDate])

    queryYear = Transaction.objects.raw("""
            SELECT id, SUM(price) as monthTotal FROM spendingsite_transaction
            WHERE date BETWEEN %s and %s
            GROUP BY id
        """, [datetime(year, 1, 1), datetime(year, 12, 31)])

    monthlyCategoryTotals = categoryTotal(categories, monthStartDate, monthEndDate)

    yearlyCategoryTotals = categoryTotal(categories, datetime(year, 1, 1), datetime(year, 12, 31))

    # print(monthlyCategoryTotals)
    # print(yearlyCategoryTotals)

    monthlyTotal = 0

    yearlyTotal = 0

    for result in query:
        monthlyTotal += result.price

    for result in queryYear:
        yearlyTotal += result.price

    context = {

        'year' : year,
        'month' : month,
        'day' : day,
        'monthlyTotal' : monthlyTotal,
        'yearlyTotal' : yearlyTotal,
        'monthlyCategoryTotals' : monthlyCategoryTotals,
        'yearlyCategoryTotals' : yearlyCategoryTotals

    }

    return HttpResponse(render(request, "spendingsite/index.html", context))

def add(request):

    if request.method == "POST":

        for i in range(12):

            if months[i] == request.POST['month']:

                monthNum = i + 1

        formatDate = f"{request.POST['year']}-{monthNum}-{request.POST['day']}"

        year = int(request.POST['year'])

        month = monthNum

        day = int(request.POST['day'])

        description = request.POST['description']

        price = float(request.POST['price'])

        category = request.POST['category']

        if addTransaction(formatDate, description, price, category, year, month, day) == 0:
            print("SUCCESS")

        else:

            print("FAIL")

        return index(request)

    else :

        year = int(date.strftime('%Y'))
        month = months[int(date.strftime('%m')) - 1]
        day = int(date.strftime('%d'))

        context = {

            'years' : range(2024,2028),
            'months' : months,
            'days' : range(1,32),
            'categories' : categories,
            'curYear' : year,
            'curMonth' : month,
            'curDay' : day

        }

        return HttpResponse(render(request, "spendingsite/add.html", context))

def list(request):

    listOfTransactions = {}

    transactions = Transaction.objects.all()

    for i in range(0,11):

        month = []

        for transaction in transactions:

            if transaction.year == 2024 and transaction.month == i + 1:

                month.append(transaction)

        listOfTransactions[months[i]] = month



    context = {

        'transactions' : listOfTransactions,
        'year' : int(date.strftime('%Y'))


    }

    return HttpResponse(render(request, "spendingsite/list.html", context))

def addTransaction(date, description, price, category, year, month, day):

    try:
        Transaction.objects.create(date=date, description=description, price=price, category=category, year=year, month=month, day=day)
        return 0
    except:
        return 1

def categoryTotal(categories, start, end):

    # print(categories)

    categoryTotals = {}

    for category in categories:

        # print(category)

        query = Transaction.objects.raw("""
                SELECT id, SUM(price) as monthTotal FROM spendingsite_transaction
                WHERE date BETWEEN %s and %s
                AND category = %s
                GROUP BY id
            """, [start, end, category])

        sum = 0

        for results in query:
            sum += results.price

        categoryTotals[category] = sum

    return categoryTotals







