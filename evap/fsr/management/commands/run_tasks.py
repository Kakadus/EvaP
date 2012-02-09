import datetime

from django.core.management.base import BaseCommand

from evap.evaluation.models import Course
from evap.fsr.models import EmailTemplate

# days before end date to send reminder
REMIND_X_DAYS_AHEAD_OF_END_DATE = 2

class Command(BaseCommand):
    args = '<kind of jobs>'
    help = 'Runs updates/tasks based on time events'
    
    def update_courses(self):
        """ Updates courses state, when evaluation time begins/ends."""
        today = datetime.date.today()
        
        for course in Course.objects.all():
            try:
                if course.state == "approved" and course.vote_start_date <= today:
                    course.evaluation_begin()
                    course.save()
                elif course.state == "inEvaluation" and course.vote_end_date < today:
                    course.evaluation_end()
                    if course.is_fully_checked():
                        course.review_finished()
                    course.save()
            except:
                pass
    
    def check_reminders(self):
        check_date = datetime.date.today() + datetime.timedelta(days=REMIND_X_DAYS_AHEAD_OF_END_DATE)
        found_courses = []
        
        for course in Course.objects.all():
            if course.state == "inEvaluation" and course.vote_end_date == check_date:
                found_courses.append(course)
        
        EmailTemplate.get_reminder_template().send_courses(found_courses, False, True)
    
    def handle(self, *args, **options):
        if len(args) > 0 and args[0] == 'daily':
            self.check_reminders()
        else:
            self.update_courses()
        
