import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """(Previous docstring remains the same)"""
    print('Hello! Let\'s explore some US bikeshare data!')
    
    cities = CITY_DATA.keys()
    while True:
        city = input("Please enter a city (chicago, new york city, washington): ").lower()
        if city in cities:
            break
        print("Invalid city. Please choose from: chicago, new york city, washington.")

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Please enter a month (all, january, february, ..., june): ").lower()
        if month in months:
            break
        print("Invalid month. Please choose from: all, january, february, march, april, may, june.")

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Please enter a day (all, monday, tuesday, ..., sunday): ").lower()
        if day in days:
            break
        print("Invalid day. Please choose from: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """(Previous docstring remains the same)"""
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month.lower()) + 1
        df = df[df['month'] == month_num]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Display statistics on the most frequent times of travel.

    Args:
        df (pandas.DataFrame): Filtered bikeshare dataset with 'Start Time' column.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f"Most Common Month: {months[most_common_month - 1]}")

    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {most_common_day}")

    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """(Previous docstring remains the same)"""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print(f"Most Commonly Used Start Station: {common_start_station}")

    common_end_station = df['End Station'].mode()[0]
    print(f"Most Commonly Used End Station: {common_end_station}")

    df['trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print(f"Most Frequent Trip: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """(Previous docstring remains the same)"""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time / 3600:.2f} hours")

    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time / 60:.2f} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """(Previous docstring remains the same)"""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("Counts of User Types:")
    print(user_types)

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:")
        print(gender_counts)
    else:
        print("\nGender data not available for this city.")

    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest Year of Birth: {earliest_birth}")
        print(f"Most Recent Year of Birth: {recent_birth}")
        print(f"Most Common Year of Birth: {common_birth}")
    else:
        print("\nBirth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays 5 lines of raw data at a time upon user request."""
    start_idx = 0
    while start_idx < len(df):
        show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no: ').lower()
        if show_data != 'yes':
            break
            
        end_idx = min(start_idx + 5, len(df))
        print('\nRaw Data (rows {} to {}):'.format(start_idx + 1, end_idx))
        print(df.iloc[start_idx:end_idx])
        print('-'*40)
        
        start_idx += 5
        if start_idx >= len(df):
            print("\nNo more data to display.")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()