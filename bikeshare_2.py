import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    city = ''
    cities = CITY_DATA.keys()
    while len(city) == 0:
        city = input('Please choose a city (Chicago, New York City, Washington)').lower()
        if city not in cities:
            city = ''
            print('Uh oh! That\'s not a valid city. Try again.')

    # Check for direct raw data request.
    month = ''
    day = ''
    raw_skip = input('Would you like to see the raw data directly? Enter yes or no.').lower()
    while raw_skip not in ('yes', 'no'):            
        raw_skip = input('Sorry, that wasn\'t a valid input. Enter yes or no.').lower()
    if raw_skip == 'no':
        # Get user input for month (all, january, february, ... , december)
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        while len(month) == 0:
            month = input('Please choose a month or all').lower()
            if month not in months:
                month = ''
                print('Uh oh! That\'s not a valid month. Please type it out fully.')

        # Get user input for day of week (all, monday, tuesday, ... sunday)
        days = ['all', 'sunday', 'monday', 'tuesday',
                'wednesday', 'thursday', 'friday',
                'saturday, sunday']
        while len(day) == 0:
            day = input('Please choose a day of the week, or all.').lower()
            if day not in days:
                day = ''
                print('Uh oh! That\'s not a valid day of the week. Please type it out fully.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june'
                  'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Display the most common month
    df['month'] = df['Start Time'].dt.month
    pop_month = df['month'].mode()[0]
    print('Most popular month:', pop_month)
    
    # Display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    pop_dow = df['day_of_week'].mode()[0]
    print('Most popular day of the week:', pop_dow)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]
    print('Most popular start hour:', pop_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print('Most popular start station:',pop_start)

    # Display most commonly used end station
    pop_end = df['End Station'].mode()[0]
    print('Most popular end station:',pop_end)

    # Display most frequent combination of start station and end station trip
    df['End to End'] = df['Start Station'] + ' to ' + df['End Station']
    pop_e2e = df['End to End'].mode()[0]
    print('Most popular trip:',pop_e2e)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total Travel Time:',total_time)

    # Display mean travel time
    avg_time = df['Trip Duration'].mean()
    print('Average Travel Time:',avg_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        genders = df['Gender'].value_counts()
    except:
        print('No gender data available')
    else:
        print(genders)

    # Display earliest, most recent, and most common year of birth
    try:
        early_yob = df['Birth Year'].min()
    except:
        print('No birth year data available')
    else:
        print('Earliest birth year:',early_yob)
        recent_yob = df['Birth Year'].max()
        print('Most recent birth year:',recent_yob)
        common_yob = df['Birth Year'].mode()[0]
        print('Most common birth year:',common_yob)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(city, proceed):
    """Displays raw data until user asks to stop."""

    raw_df = pd.read_csv(CITY_DATA[city])

    # Depending on previous input or output, this question may not be necessary.
    if len(proceed) == 0:
        proceed = input('Would you like to see the raw data? Enter yes or no.').lower()
        while proceed not in ('yes', 'no'):            
                proceed = input('Sorry, that wasn\'t a valid input. Enter yes or no.').lower()

    index = 0
    max_col = raw_df.size / len(raw_df.columns)
    while proceed == 'yes' and index < max_col:
        print(raw_df[index:index + 5])
        index += 5
        proceed = input('Would you like to see more raw data? Enter yes or no').lower()
        while proceed not in ('yes', 'no'):            
            proceed = input('Sorry, that wasn\'t a valid input. Enter yes or no.').lower()
    if index >= max_col:
        print('All data has been presented.')

def main():
    while True:
        city, month, day = get_filters()
        goto_raw = ''
        if len(month) > 0:
            df = load_data(city, month, day)
            if df.size > 0:
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
            else:
                print("No data available given your search criteria.")
                print('-'*40)
                goto_raw = 'no'
        else:
            goto_raw = 'yes'

        raw_data(city, goto_raw)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart not in ('yes', 'no'):            
            restart = input('Sorry, that wasn\'t a valid input. Enter yes or no.').lower()

        if restart == 'no':
            break


if __name__ == "__main__":
    main()
