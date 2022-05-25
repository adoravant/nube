from django.shortcuts import render

# Create your views here.
def home_view(request):
	template_name="main/index.html"
	context= { "sect" : "home" }
	return render(request, template_name, context)


def about():
	property_list = Propiedad.objects.filter(price__lte=25000)[0:16]
	template_name="main/about.html"
	context= { "sect" : "about", "property_list" : property_list }
	return render(request, template_name, context=context )


def contact(request):
	template_name="main/contact.html"
	sect = "contact"
	return render(request, template_name, context={ "sect": "contact" })


def property_agent(request):
	template_name="main/property_agent.html"
	context= { "sect" : "property_agent" }
	return render(request, template_name, context )


def property_list(request):
	template_name="main/property-list.html"
	context= { "sect" : "property_list" }
	return render(request, template_name, context)

def property_type(request):
	template_name="main/property-type.html"
	context= { "sect" : "property_type" }
	return render(request, template_name, context)



def testimonial(request):
	template_name="main/testimonial.html"
	context= { "sect" : "testimonial" }
	return render(request, template_name, context)
