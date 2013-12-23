rm db.sqlite3
rm media/*
python2 manage.py syncdb --noinput
python2 manage.py shell < test/fill_db.py
