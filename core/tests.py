from django.test import TestCase

# Create your tests here.

global count
count = 0

def increment():
    global count
    count += 1
    return count

increment()