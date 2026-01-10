import csv
import random
from datetime import datetime, timedelta

def generate_flight_data(filename, num_records=1000):
    header = [
        'date', 'flight_sorties', 'is_holiday', 'user_type', 'enterprise_name',
        'admin_region', 'aircraft_model', 'day_of_week', 'cross_region', 'time_slot',
        'flight_duration', 'flight_distance', 'altitude_interval', 'aircraft_category',
        'entity_id'
    ]

    user_types = ['Individual', 'Enterprise', 'Unknown']
    enterprises = ['DJI', 'EHang', 'XAG', 'Aerofugia', 'AutoFlight'] + [f'Ent_{i}' for i in range(1, 100)]
    regions = ['Nanshan', 'Futian', 'Luohu', 'Baoan', 'Longgang']
    models = ['Mavic 3', 'Matrice 300', 'Agras T40', 'EH216', 'V1500']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    time_slots = [f'{h:02d}:00-{h+1:02d}:00' for h in range(6, 22)]
    altitude_intervals = ['0-100m', '100-300m', '300-600m', '>600m']
    categories = ['Consumer', 'Industrial', 'Logistics', 'Passenger']

    start_date = datetime(2023, 1, 1)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for _ in range(num_records):
            date_offset = random.randint(0, 364)
            date = start_date + timedelta(days=date_offset)
            is_holiday = date.weekday() >= 5 # Simplified

            row = [
                date.strftime('%Y-%m-%d'),
                random.randint(1, 5),
                'Yes' if is_holiday else 'No',
                random.choice(user_types),
                random.choice(enterprises),
                random.choice(regions),
                random.choice(models),
                days[date.weekday()],
                f"{random.choice(regions)}-{random.choice(regions)}",
                random.choice(time_slots),
                random.randint(5, 60),
                random.uniform(0.5, 20.0),
                random.choice(altitude_intervals),
                random.choice(categories),
                f'Entity_{random.randint(1, 200)}'
            ]
            writer.writerow(row)

if __name__ == '__main__':
    generate_flight_data('evidence_project/sources/low_altitude_economy/flight_data.csv', 5000)
