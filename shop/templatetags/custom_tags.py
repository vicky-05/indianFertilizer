from django import template

register = template.Library()

@register.filter
def multiply(value, args):
	return value * args

@register.filter
def calculate_total_price(products):
	total_price = 0
	for product in products:
		total_price += multiply(product.product.selling_price, product.qty)
	return total_price