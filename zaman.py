from datetime import datetime, timedelta

def tarihleri_al():
    bugun=datetime.now()
    iki_hafta_sonra=bugun+timedelta(weeks=2)
    return bugun.strftime("%Y-%m-%d"), iki_hafta_sonra.strftime("%Y-%m-%d")
