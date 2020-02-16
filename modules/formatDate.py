import calendar, dateutil.parser # For converting xsd:datetime to something sensible

def formatDate(date, specificity):
    dateOfPost = date
    date_string = ""
    mydate = dateutil.parser.parse(dateOfPost)
    month_no = mydate.month
    monthstring = calendar.month_name[month_no]
    year = str(mydate.year)
    date_string = monthstring  + " " + year
    return date_string
