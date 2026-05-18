from datetime import date, timedelta

def track_medicines(medicine_list):
    print("=== MEDICINE STOCK TRACKER ===\n")
    
    today = date.today()
    
    for medicine in medicine_list:
        name = medicine['name']
        tablets_per_day = medicine['tablets_per_day']
        total_tablets = medicine['total_tablets']
        is_critical = medicine['is_critical']
        
        # Calculate how many days stock will last
        days_remaining = total_tablets // tablets_per_day
        finish_date = today + timedelta(days=days_remaining)
        reorder_date = today + timedelta(days=days_remaining - 2)
        
        print(f"Medicine   : {name}")
        print(f"Stock      : {total_tablets} tablets")
        print(f"Daily dose : {tablets_per_day} tablet(s) per day")
        print(f"Lasts until: {finish_date}")
        print(f"Reorder by : {reorder_date}")
        
        if is_critical:
            print(f"⚠️  CRITICAL MEDICINE - Do not miss reorder!")
        
        if days_remaining <= 2:
            print(f"🚨 URGENT - Stock almost finished!")
        elif days_remaining <= 5:
            print(f"⚠️  WARNING - Stock running low!")
        else:
            print(f"✅ Stock is sufficient")
        
        print("-" * 40)

# Test with medicines from your prescription
medicines = [
    {
        'name': 'Cap. D-Pearl 60k',
        'tablets_per_day': 1,
        'total_tablets': 8,
        'is_critical': False
    },
    {
        'name': 'T. Cetirizine 10mg',
        'tablets_per_day': 1,
        'total_tablets': 5,
        'is_critical': False
    },
    {
        'name': 'Cap. Omeprazole 20mg',
        'tablets_per_day': 1,
        'total_tablets': 5,
        'is_critical': False
    }
]

track_medicines(medicines)