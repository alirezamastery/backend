from django.contrib import admin
from django.conf.urls import url
from django.template.response import TemplateResponse
from jens.models.category import Category


# from jens.management.manager_view import manager_view

class MyAdminSite(admin.AdminSite):

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        new_app = {
            "name":      "Product Manager",
            "app_label": "product_manager_app",
            # "app_url": "/admin/test_view",
            # 'has_module_perms': True,
            "models":    [
                {
                    "name":        "select product",
                    "object_name": "select_product",
                    # 'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                    "admin_url":   "/admin/test_view",
                    # "add_url":     "/admin/test_view/add/",
                    "view_only":   True,
                }
            ],
        }

        # for k,v in app_list[1]['models'][0].items():
        #     print(f'{k:<20} | {v}')

        app_list.insert(1, new_app)  # adding this after the first app in side bar

        return app_list

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'test_view/',  # root is 'admin/'
                self.admin_view(self.my_view), name="preview"),
        ]
        return urls + custom_urls

    def my_view(self, request):
        context = dict(
                # Include common variables for rendering the admin template.
                self.each_context(request),
                # Anything else you want in the context...
                # 'from_me':'from me',
        )
        context['from_me'] = 'this is it'
        context['levels'] = list()
        context['levels'].append({'selected':    None,
                                  'selected_pk': None,
                                  'options':     Category.objects.filter(level=0)
                                  })
        context['leaf_node'] = None
        # note that each time a request is sent, we are building the context from zero
        if request.method == 'POST':
            counter = 0
            while True:  # start going down the category hierarchy
                category_pk = None
                try:
                    category_pk = request.POST.get(f'category_selector_{counter}')
                except:
                    break
                if category_pk:
                    # if the user has selected a category for this level in the category hierarchy,
                    # get the children of the selected category which will become the options for the next level
                    category_obj = Category.objects.get(pk=category_pk)
                    context['levels'][counter]['selected'] = category_obj.name
                    context['levels'][counter]['selected_pk'] = category_obj.pk
                    # in this section we check if the data in request.POST for this level, is a child of
                    # the previous category.so if the user changes a selection, all the next 'select' tags
                    # in the front end will be removed
                    if counter > 0:
                        parent_pk = context['levels'][counter - 1]['selected_pk']
                        parent_obj = Category.objects.get(pk=parent_pk)
                        parent_options_pk = [str(option.pk) for option in parent_obj.get_children()]
                        if category_pk not in parent_options_pk:
                            break
                    children = category_obj.get_children()
                    # if the selected category has no children, it means we have reached a leaf node and
                    # should start looking for the products related to this node
                    if not children:
                        # TODO find a way to get product obj, now we only have a name which is not enough
                        selected_product = None
                        try:
                            selected_product = request.POST.get(f'product_selector')
                        except:
                            pass
                        if selected_product:
                            context['leaf_node'] = {'selected': selected_product,
                                                    'options':  category_obj.products.all()
                                                    }
                            # --- do your thing here ---
                            break
                        context['leaf_node'] = {'selected': None,
                                                'options':  category_obj.products.all()
                                                }
                        break
                    # if the selected category has children, continue going down the category hierarchy
                    context['levels'].append({'selected': None,
                                              'options':  children
                                              })
                else:
                    break
                counter += 1

        return TemplateResponse(request, "admin/test_template.html", context)
