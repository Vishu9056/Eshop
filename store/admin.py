from django.contrib import admin
from .models import Product , Category, Customer , Order, Setting, Contact


from django.contrib import messages 


class CustomerAdmin(admin.ModelAdmin): 
	list_display = ('first_name', 'phone', 'email') 

	def active(self, obj): 
		return obj.is_active == 1

	active.boolean = True


	def make_active(modeladmin, request, queryset): 
		queryset.update(is_active = 1) 
		messages.success(request, "Selected Record(s) Marked as Active Successfully !!") 

	def make_inactive(modeladmin, request, queryset): 
		queryset.update(is_active = 0) 
		messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!") 

	admin.site.add_action(make_active, "Make Active") 
	admin.site.add_action(make_inactive, "Make Inactive") 


class ContactAdmin(admin.ModelAdmin):
    search_fields = ('name','email','phone')
    ordering = ['name']
    # fields = (('name','email'),('phone','desc'))
    fieldsets = (
        ("Personal Details", {
            "fields":(
                'name','email'
            ),
        }),
        ("Other Details", {
            "fields":(
                'phone','desc'
            ),
        }),
    )

# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at']


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

    def active(self, obj): 
        return obj.is_active == 1
  
    active.boolean = True
  
    def has_add_permission(self, request): 
        return False

class AdminOrder(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity', 'price',]

# Register your models here.
admin.site.register(Product,AdminProduct )
admin.site.register(Category, AdminCategory)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, AdminOrder)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Contact,ContactAdmin)