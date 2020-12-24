from django.shortcuts import render
from django.http import JsonResponse

# manually trigger user report scrape (can probably delete later)
from .report_scraper import scrape_user_report_data
def get_user_report_data(request):
    count = scrape_user_report_data()
    return JsonResponse({'count': count})
