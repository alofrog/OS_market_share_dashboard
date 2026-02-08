import pandas as pd
import requests
import io
import datetime

def get_statcounter_data(metric, device, region, start_date, end_date):
    """
    Fetches data from StatCounter using the CSV export URL pattern.
    
    Args:
        metric (str): 'os', 'search_engine', 'browser', 'social_media', etc.
        device (str): 'desktop', 'mobile', 'tablet', 'console', 'combined' (Desktop+Mobile+Tablet+Console)
                      Note: Statcounter uses specific codes. 'ww' is region.
                      Platform codes might be part of the chart_id.
        region (str): 'ww' for Worldwide.
        start_date (datetime.date): Start date.
        end_date (datetime.date): End date.
        
    Returns:
        pd.DataFrame: The fetched data or None if failed.
    """
    # Format dates as YYYYMM
    start_str = start_date.strftime("%Y%m")
    end_str = end_date.strftime("%Y%m")
    
    # Construct Chart ID
    # Patterns: 
    # Search Engine: search_engine-ww-monthly-YYYYMM-YYYYMM
    # OS: os-ww-monthly-YYYYMM-YYYYMM
    # Mobile OS: mobile_os-ww-monthly-YYYYMM-YYYYMM (Wait, looking at the user snippet: mobile_os_combined-ww-monthly...)
    
    # Logic to map device/metric to the slug part
    # Example: 'search_engine' + 'desktop' -> 'search_engine-desktop-ww-monthly...'
    # But usually the device is part of the metric name in the ID or handled separately?
    # User's snippet: mobile_os_combined-ww-monthly-202501-202601
    # Likely: [metric]_[device]-ww-monthly-[start]-[end]
    # Let's try to be generic.
    
    slug_base = f"{metric}_{device}" if device != "combined" else f"{metric}_combined"
    
    # StatCounter sometimes uses different slugs. 
    # Search Engine: search_engine
    # OS: os
    # Browser: browser
    
    # Refined logic based on user snippet "mobile_os_combined":
    # If metric is "os" and device is "mobile", it seems to be "mobile_os".
    # If metric is "search_engine", it is "search_engine".
    
    if metric == "os":
        if device == "combined":
             slug = "os_combined"
        elif device == "mobile":
             slug = "mobile_os" # Based on snippet? But snippet said mobile_os_combined?
             # Actually snippet: mobile_os_combined-ww-monthly...
             # Maybe "mobile_os_combined" means "Mobile OS" (combined vendors)
        else:
             slug = f"{device}_os"
    elif metric == "search_engine":
        slug = "search_engine"
    else:
        slug = metric

    # The user snippet was `mobile_os_combined`.
    # Let's construct the chart ID.
    chart_id = f"{slug}-{region}-monthly-{start_str}-{end_str}"
    
    url = f"https://gs.statcounter.com/chart.php?{chart_id}&csv=1"
    
    print(f"Fetching from: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # StatCounter CSV usually starts with some metadata lines or just headers.
        # Let's try reading it.
        # Sometimes the first line is title, we might need to skip.
        # Usually it's strictly CSV.
        
        content = response.content.decode('utf-8')
        
        # Check if response is HTML error page
        if "<!DOCTYPE html>" in content[:50]:
            print("Received HTML instead of CSV. Access might be blocked or URL invalid.")
            return None
            
        df = pd.read_csv(io.StringIO(content))
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def get_mock_data():
    """Returns mock data for testing UI without internet/valid scraping."""
    dates = pd.date_range(start="2025-01-01", periods=12, freq="M").strftime("%Y-%m")
    data = {
        "Date": dates,
        "Google": [92.0 + i*0.1 for i in range(12)],
        "Bing": [3.0 - i*0.05 for i in range(12)],
        "Yahoo!": [1.5 for _ in range(12)],
        "Baidu": [1.0 for _ in range(12)],
        "DuckDuckGo": [0.5 + i*0.02 for i in range(12)],
        "Other": [2.0 for _ in range(12)]
    }
    return pd.DataFrame(data)
