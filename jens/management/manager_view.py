# from backend.admin import MyAdminSite
# from django.conf.urls import url
# from django.template.response import TemplateResponse
# from jens.models.category import Category
#
#
# def manager_view(request):
#     context = dict(
#             # Include common variables for rendering the admin template.
#             MyAdminSite.each_context(request),
#             # Anything else you want in the context...
#             # 'from_me':'from me',
#     )
#     context['from_me'] = 'this is it'
#     context['selectable_categories'] = list()
#     context['selectable_categories'].append({'selected': None,
#                                              'options':  Category.objects.filter(level=0)
#                                              })
#     context['leaves'] = None
#
#     print(context['selectable_categories'])
#
#     if request.method == 'POST':
#         counter = 0
#         while True:
#             print('-' * 50)
#             selected_category = None
#             try:
#                 selected_category = request.POST.get(f'category_selector_{counter}')
#                 print(counter, selected_category)
#             except:
#                 break
#             context['selectable_categories'][counter]['selected'] = selected_category
#             if selected_category:
#                 selected_category_obj = Category.objects.get(name=selected_category)
#                 children = selected_category_obj.get_children()
#                 print(children)
#                 if not children:
#                     selected_product = None
#                     try:
#                         selected_product = request.POST.get(f'leaves_selector')
#                         print(selected_product)
#                     except:
#                         pass
#                     if selected_product:
#                         context['leaves'] = {'selected': selected_product,
#                                              'options':  selected_category_obj.products.all()
#                                              }
#                         break
#                     context['leaves'] = {'selected': None,
#                                          'options':  selected_category_obj.products.all()
#                                          }
#                     print('reached to the products')  # insert what you want to do here
#                     break
#                 print('all passed')
#                 context['selectable_categories'].append({'selected': None,
#                                                          'options':  children
#                                                          })
#             else:
#                 break
#             counter += 1
#     return TemplateResponse(request, "admin/test_template.html", context)
