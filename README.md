# EmailService
Email service with periodic updates

You will need
 - Redis server (confguration for redis server can be done in settings.py of the project
 - celery (install through requirements)
 - email account with **access to less secure apps turned on**
 
 **Configure email parameters in the mailer/views.py where these variables are declared.**
 
 1) Create a virtual environment and activate it
 2) install requirements using 'pip install -r requirements.txt'
 3) start the redis server (I used executeable file to turn on the server).
 4) start celery beat using 'celery -A emailService beat -l info'
      It should look like this:
      
      
              (venv) C:\Users\AC52420\Desktop\django\emailService>celery -A emailService beat -l info
              celery beat v3.1.18 (Cipater) is starting.
              __    -    ... __   -        _
              Configuration ->
                  . broker -> redis://localhost:6379//
                  . loader -> celery.loaders.app.AppLoader
                  . scheduler -> celery.beat.PersistentScheduler
                  . db -> celerybeat-schedule
                  . logfile -> [stderr]@%INFO
                  . maxinterval -> now (0s)
              [2020-03-26 16:56:25,336: INFO/MainProcess] beat: Starting...

 5) start celery worker using 'celery -A emailService worker -l info'
      It should looke like this:
      
          (venv) C:\Users\AC52420\Desktop\django\emailService>celery -A emailService worker -l info

             -------------- celery@IND-5CG9381L54 v3.1.18 (Cipater)
            ---- **** -----
            --- * ***  * -- Windows-10-10.0.18362-SP0
            -- * - **** ---
            - ** ---------- [config]
            - ** ---------- .> app:         emailService:0x2998e5b5828
            - ** ---------- .> transport:   redis://localhost:6379//
            - ** ---------- .> results:     redis://localhost:6379
            - *** --- * --- .> concurrency: 8 (prefork)
            -- ******* ----
            --- ***** ----- [queues]
             -------------- .> celery           exchange=celery(direct) key=celery


            [tasks]
              . emailService.celery.debug_task
              . email_report
              
6) start the django server using' 'python manage.py runserver <ip:port>
