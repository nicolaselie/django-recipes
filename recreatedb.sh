rm db.sqlite3

if [ -f initial_data.json ]
then
    python2 manage.py syncdb --noinput

else
    python2 manage.py syncdb
fi

if [ "$1"=="--fill" ]
then
    rm media/*
    python2 manage.py shell < test/fill_db.py
fi