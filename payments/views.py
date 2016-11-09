import requests
import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.urls import reverse

from courses.models import Course
from sesiones.models import Session, Enrollment

from .actions import create_payment, execute_payment


@login_required
def checkout(request):
    session_id = request.GET.get('session_id', '0')
    session = get_object_or_404(Session, id=session_id)
    course = session.course
    # course = get_object_or_404(Course, course_id=request.GET.get('course_id'))

    transaction = {
        'amount': {
            'total': '%.2f' % course.monthly_price,
            'currency': 'USD',
            'details': {
                'subtotal': '%.2f' % course.monthly_price,
                'shipping': '0.00',
            }
        },
        'item_list': {
            'items': [{
                'quantity': '1',
                'name': course.name,
                'price': '%.2f' % course.monthly_price,
                'currency': 'USD',
                'description': course.description,
                'tax': '0'
            }]
        },
        'invoice_number': str(random.randint(100, 1000000)),
        'description': 'Enrollment payment',
        # 'custom': 'merchant custom data'
    }

    response = create_payment(request, transaction)
    print(response.text)
    print(response.status_code)

    if response.status_code in [200, 201]: # everything ok
        r = response.json()
        print('*************')
        print(r['id'])
        if r['state'] == 'created':
            session.enroll(student=request.user.student, payment_id=r['id'])
            links = list(filter(lambda link: link['rel'] == 'approval_url', r['links']))
            return HttpResponseRedirect(links[0]['href'])
        else:
            print('state is not \'created\'')
            print(r)
            return HttpResponseServerError('Checkout error! Please try again.')
    else:
        print('status is not 200')
        return HttpResponseServerError('Checkout error! Please try again.')


@login_required
def execute(request):
    # token = request.GET.get('token')
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    try:
        enrollment = Enrollment.objects.get(payment_id=payment_id)
    except Enrollment.DoesNotExist:
        return HttpResponseServerError('Session does not exist!')

    response = execute_payment(request, payment_id, payer_id, enrollment.id)

    if response.status_code == 200: # everything ok
        r = response.json()
        if r['state'] == 'approved':
            enrollment.status = 'active'
            enrollment.save()
            return HttpResponseRedirect(reverse('courses:detail', kwargs={'course_id': enrollment.session.course.id}))
        else:
            return HttpResponseServerError('Payment not approved!')
    else:
        return HttpResponseServerError('Error executing payment!')
    # return-url-custom?paymentId=PAY-7M8836987D341211CLARSTLY&token=EC-96U885238J8845306&PayerID=H8SMNJNFHPSHW


def cancel(request):
    pass
