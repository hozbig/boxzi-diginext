from utils import jalali


def jdate_edge_convertor(org_date):
    if org_date:
        # If date is String:
        if type(org_date) == str:
            date = org_date.split("-")  # [0]day, [1]month, [2]day
            if int(date[0]) < 1500:
                gregorian_date = jalali.Persian(
                    int(date[0]), int(date[1]), int(date[2])
                ).gregorian_datetime()
                return gregorian_date
            return org_date

        # If date is Datetime:
        if int(org_date.year) < 1500:
            gregorian_date = jalali.Persian(
                date.year, date.month, date.day
            ).gregorian_datetime()
            return gregorian_date

    return org_date
