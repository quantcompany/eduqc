import requests
import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from courses.models import Course, Enrollment
from payments.models import Coupon

from .actions import create_payment, execute_payment


@login_required
def checkout(request):
    course_id = request.GET.get('course_id', '0')
    course = get_object_or_404(Course, id=course_id)

    code = request.GET.get('coupon', None)

    try:
        coupon = Coupon.objects.get(code=code)
        discount = coupon.discount
    except Coupon.DoesNotExist:
        discount = 0

    discount_factor = 1 - discount

    transaction = {
        'amount': {
            'total': '%.2f' % (course.monthly_price * discount_factor),
            'currency': 'USD',
            'details': {
                'subtotal': '%.2f' % course.monthly_price,
                'discount': '%.2f' % (course.monthly_price * discount),
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
        'invoice_number': '{0}-{1}-{2}'.format(
            course_id,
            request.user.id,
            timezone.now().strftime('%y%m%d%H%M%S')),
        'description': 'Enrollment payment',
        # 'custom': 'merchant custom data'
    }
    from pprint import pprint
    pprint(transaction)
    response = create_payment(request, transaction)
    print(response.status_code)
    print(response.text)

    if response.status_code in [200, 201]: # everything ok
        r = response.json()
        print('*************')
        print(r['id'])
        if r['state'] == 'created':
            course.enroll(student=request.user.student, payment_id=r['id'])
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
        return HttpResponseServerError('Enrollment does not exist!')

    response = execute_payment(request, payment_id, payer_id, enrollment.id)

    if response.status_code == 200: # everything ok
        r = response.json()
        if r['state'] == 'approved':
            enrollment.status = 'active'
            enrollment.save()
            return HttpResponseRedirect(reverse('courses:detail', kwargs={'course_slug': enrollment.course.slug}))
        else:
            return HttpResponseServerError('Payment not approved!')
    else:
        print(response.status_code)
        print(response.text)
        return HttpResponseServerError('Error executing payment!')
    # return-url-custom?paymentId=PAY-7M8836987D341211CLARSTLY&token=EC-96U885238J8845306&PayerID=H8SMNJNFHPSHW


def cancel(request):
    return HttpResponseRedirect(reverse('courses:index'))
