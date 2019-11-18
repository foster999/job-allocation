import time
import random
import threading
import uuid

class JobQueue():
    def __init__(self):
        self.jobs = []
        
    def addJob(self, job):
        self.jobs.append(job)
        
    def popJob(self):
        return self.jobs.pop()
        
    def getJobs(self):
        return self.jobs
        
    def printJobs(self):
        print([(job.identifier, job.id) for job in self.getJobs()])
            
class Job():
    def __init__(self, identifier, resource, priority):
        self.identifier = identifier
        self.resource = resource
        self.priority = priority
        self.status = "new"
        self.id = str(uuid.uuid4())
	
class Printer(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.resource_loaded = 0
        self.status = "idle"
        self.print_rate = random.random()*1000
        self.queue = queue
        self.load(10000)
        
    def load(self, quantity):
        self.resource_loaded += quantity
        
    def run(self):
        next_job = self.get_job(self.queue)
        self.extrude(next_job)
        
    def extrude(self, job_object):
        self.status = "busy"
        print(f"{self.name}: Printing {job_object.identifier}. Printer is {self.status}.")
        time.sleep(job_object.resource/self.print_rate)
        self.resource_loaded -= job_object.resource
        self.status = "idle"
        print(f"{self.name}: {job_object.identifier} printed. {self.resource_loaded} remaining. Printer is {self.status}")
        
    def get_job(self, queue):
        printable = [job for job in queue.getJobs() if job.resource <= self.resource_loaded]
        printable.sort(key=lambda x: x.priority)
        return printable.pop()

identifiers = ["Eiffel Tower", "London Bus", "Frog", "Wallace", "Gromit", "Rifle", "3D Printer"]
queue = JobQueue()

for j in identifiers:
    new_job = Job(j, random.random()*5000, 1)
    queue.addJob(new_job)

queue.printJobs()
printers = []
job1 = Job("Eiffel Tower", 400, 1)

for i in range(5):
    p = Printer("printer "+ str(i), queue)
    p.start()
    printers.append(p)
	