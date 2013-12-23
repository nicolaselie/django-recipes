rm db.sqlite3
#rm media/*

if [ -f initial_data.json ]
then
    python2 manage.py syncdb --noinput

else
    python2 manage.py syncdb
fi

#python2 manage.py shell < test/fill_db.py
