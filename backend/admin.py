from django.contrib import admin
from django.conf.urls import url
from django.template.response import TemplateResponse
from jens.models.category import Category


class MyAdminSite(admin.AdminSite):

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        new_app = [
            {
                "name":      "My Custom App",
                "app_label": "my_test_app",
                # "app_url": "/admin/test_view",
                # 'has_module_perms': True,
                "models":    [
                    {
                        "name":        "tcptraceroute",
                        "object_name": "tcptraceroute",
                        # 'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                        "admin_url":   "/admin/test_view",
                        "add_url":     "/admin/test_view/add/",
                        "view_only":   True,
                    }
                ],
            }
        ]
        # for k,v in app_list[1]['models'][0].items():
        #     print(f'{k:<20} | {v}')
        print(type(app_list))
        # app_list.append(new_app)
        app_list += new_app
        # app_list.insert(0,new_app)

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
        context['selectable_categories'] = [None, ]
        context['selectable_categories'][0] = {'selected': None,
                                               'options':  Category.objects.filter(level=0)
                                               }
        context['leaves'] = None

        print(context['selectable_categories'])

        if request.method == 'POST':
            counter = 0
            while True:
                print('-' * 50)
                selected_category = None
                try:
                    selected_category = request.POST.get(f'category_selector_{counter}')
                    print(counter, selected_category)
                except:
                    break
                context['selectable_categories'][counter]['selected'] = selected_category
                if selected_category:
                    selected_category_obj = Category.objects.get(name=selected_category)
                    children = selected_category_obj.get_children()
                    print(children)
                    if not children:
                        selected_product = None
                        try:
                            selected_product = request.POST.get(f'leaves_selector')
                            print(selected_product)
                        except:
                            pass
                        if selected_product:
                            context['leaves'] = {'selected': selected_product,
                                                 'options':  selected_category_obj.products.all()
                                                 }
                            break
                        context['leaves'] = {'selected': None,
                                             'options':  selected_category_obj.products.all()
                                             }
                        print('reached to the products')  # insert what you want to do here
                        break
                    print('all passed')
                    context['selectable_categories'].append({'selected': None,
                                                             'options':  children
                                                             })
                else:
                    break
                counter += 1
        return TemplateResponse(request, "admin/test_template.html", context)
