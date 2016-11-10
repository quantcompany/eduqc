rivets.formatters.decorate = function(value, format){
  return format.replace('{0}', value)
} // course detail url

rivets.formatters.checkoutURL = function(coupon, courseId){
  var url = '/payments/checkout?course_id=' + courseId;

  if (coupon) {
      url += '&coupon=' + coupon;
  }

  return url;
}
