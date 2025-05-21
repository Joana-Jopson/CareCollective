from django.contrib import admin
from django.urls import path
from . import views


urlpatterns=[
    path('', views.index, name='index'),
    #path('login/', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_register/', views.user_register, name='user_register'),
    path('donor_register/', views.donor_register, name='donor_register'),
    path('change_password/', views.change_password, name='change_password'),
    path('search/', views.search, name='search'),
    path('notifications/', views.notifications, name='notifications'),
    #----------------------------USER-------------------------------------
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('donor/<int:donor_id>/', views.donor_details_page, name='donor_details_page'),
    path('user_items_based_category/<int:category_id>/', views.user_items_based_category, name='user_items_based_category'),
    path('add_request/<int:item_id>/', views.add_request, name='add_request'),
    path('my-requests/', views.user_request_view, name='user_request_view'),
    path('user_request_update/<int:request_id>/', views.user_request_update, name='user_request_update'),
    path('delete-request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('user_view_status/', views.user_view_status, name='user_view_status'),
    path('delete-status/<int:request_id>/', views.delete_order_request, name='delete_order_request'),
    path('item/<int:item_id>/', views.item_complete_details, name='item_complete_details'),
    path('my_chat_list/', views.user_chat_list, name='user_chat_list'),
    path('chat/<int:donor_id>/', views.user_donor_chat, name='user_donor_chat'),
    path('comment_list/', views.user_leave_comment, name='user_leave_comment'),
    path('comments/<int:donor_id>/', views.leave_comment, name='leave_comment'),
    path('item_search/<int:item_id>/', views.user_items_search, name='user_items_search'),
   
    #----------------------------DONOR-------------------------------------
    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('add_item/', views.add_item, name='add_item'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('donor-items-update/<int:item_id>/', views.donor_items_update, name='donor_items_update'),
    path('donor_items_based_category/<int:category_id>/', views.donor_items_based_category, name='donor_items_based_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('list_donated_items/', views.list_donated_items, name='list_donated_items'),
    path('manage-requests/', views.donor_manage_requests, name='donor_manage_requests'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('my-category-requests/', views.donor_view_category_request, name='donor_view_category_request'),
    path('delete-category/<int:category_id>/', views.delete_category_request, name='delete_category_request'),
     path('user_map/', views.user_map_view, name='user_map'),
    path('my_chats_list/', views.donor_chat_list, name='donor_chat_list'),
    path('my-chats/<int:user_id>/', views.donor_user_chat, name='donor_user_chat'),
    path('my-comments/', views.donor_comments_view, name='donor_comments_view'),

    
    #----------------------------ADMIN-------------------------------------
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_category_requests/', views.manage_category_requests, name='manage_category_requests'),
    path('approve_category/<int:category_id>/', views.approve_category, name='approve_category'),
    path('reject_category/<int:category_id>/', views.reject_category, name='reject_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('manage_users/', views.admin_manage_users, name='admin_manage_users'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('manage_donors/', views.admin_manage_donors, name='admin_manage_donors'),
    path('block_donor/<int:user_id>/', views.block_donor, name='block_donor'),
    path('unblock_donor/<int:user_id>/', views.unblock_donor, name='unblock_donor'),
    path('admin_items/', views.admin_manage_items, name='admin_manage_items'),
    path('admin_items_block/<int:item_id>/', views.block_item, name='block_item'),
    path('admin_items_unblock/<int:item_id>/', views.unblock_item, name='unblock_item'),
    path('admin_order_status_view/', views.admin_order_status_view, name='admin_order_status_view'),
    path('comments_list/', views.admin_comment_list, name='admin_comment_list'),
    path('block_comment/<int:comment_id>/<int:donor_id>/', views.block_comment, name='block_comment'),
    path('unblock_comment/<int:comment_id>/<int:donor_id>/', views.unblock_comment, name='unblock_comment'),
    
    
    
    
    ]

