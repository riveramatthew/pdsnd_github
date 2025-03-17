import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_valid_input(prompt, valid_options):
    """Prompt user for input and validate against options."""
    while True:
        choice = input(prompt).lower()
        if choice in valid_options:
            return choice
        print(f"Invalid input. Choose from: {', '.join(valid_options)}.")

def get_filters():
    """(Previous docstring remains the same)"""
    print('Hello! Let\'s explore some US bikeshare data!')
    
    cities = CITY_DATA.keys()
    city_prompt = "Please enter a city (chicago, new york city, washington): "
    city = get_valid_input(city_prompt, cities)

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month_prompt = "Please enter a month (all, january, february, ..., june): "
    month = get_valid_input(month_prompt, months)

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_prompt = "Please enter a day (all, monday, tuesday, ..., sunday): "
    day = get_valid_input(day_prompt, days)

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """Loads and filters data based on user input."""
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_num]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df

def calculate_mode(series):
    """Returns the mode of a given series safely."""
    return series.mode()[0] if not series.empty else 'N/A'

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f"Most Common Month: {months[calculate_mode(df['month']) - 1]}")
    print(f"Most Common Day of Week: {calculate_mode(df['day_of_week'])}")
    df['start_hour'] = df['Start Time'].dt.hour
    print(f"Most Common Start Hour: {calculate_mode(df['start_hour'])}")
    
    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    print(f"Most Common Start Station: {calculate_mode(df['Start Station'])}")
    print(f"Most Common End Station: {calculate_mode(df['End Station'])}")
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    print(f"Most Frequent Trip: {calculate_mode(df['trip'])}")
    
    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """(Previous docstring remains the same)"""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    durations = df['Trip Duration']  # Alias for efficiency
    print(f"Total Travel Time: {durations.sum() / 3600:.2f} hours")
    print(f"Mean Travel Time: {durations.mean() / 60:.2f} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    print("Counts of User Types:")
    print(df['User Type'].value_counts())
    
    if 'Gender' in df:
        print("\nCounts of Gender:")
        print(df['Gender'].value_counts())
    else:
        print("\nGender data not available for this city.")
    
    if 'Birth Year' in df:
        print(f"\nEarliest Year of Birth: {int(df['Birth Year'].min())}")
        print(f"Most Recent Year of Birth: {int(df['Birth Year'].max())}")
        print(f"Most Common Year of Birth: {int(calculate_mode(df['Birth Year']))}")
    else:
        print("\nBirth year data not available for this city.")
    
    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print('-' * 40)

def display_raw_data(df):
    """Displays raw data upon user request."""
    start_idx = 0
    while start_idx < len(df):
        show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no: ').lower()
        if show_data != 'yes':
            break
        print(df.iloc[start_idx:start_idx + 5])
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

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
