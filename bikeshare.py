import time
import pandas as pd
import numpy as np
import datetime
import calendar

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
    cities = ['chicago','new york city','washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # want the entry to be case 'insensitive' so using .lower() method
    city = str(input("\nWould you like to look at Chicago, New York City, or Washington?\n")).lower()
    
    while city not in cities:
        city = input("\nPlease enter a valid city. Options include Chicago, New York City, Washington:\n").lower()
        break

    # get user input for month (all, january, february, ... , june)
    month = str(input("\nWhich month are you interested in? Choose between January and June inclusive.\nType 'all' if you do not want to filter by month:\n")).lower()
    
    while month not in months:
        month = input("\nPlease enter a valid month. Options include January, February, March, April, May, June, or all:\n")
        break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input("\nWhich day of of the week are you interested in?\nType 'all' if you do not want to filter by day:\n")).lower()
    
    while day not in days:
        day = input("\nPlease enter a valid day. Options include Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all:\n")

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
    # adding .str.lower() to convert the new day column to lower case to match user's input
    df['day'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        print(month)

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day]

    return df

def time_statistics(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n*** Calculating The Most Frequent Times of Travel ***\n')
    start_time = time.time()

    # converting 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extracting month from 'Start Time' column
    df['month'] = df['Start Time'].dt.month
    # finding most commong month
    most_common_month_int = df['month'].value_counts().idxmax()
    most_common_month_name = calendar.month_name[most_common_month_int]

    # extracting day from 'Start Time' column
    df['day'] = df['Start Time'].dt.day_name().str.lower()
    # displaying the most common day of week
    most_common_day = df['day'].value_counts().idxmax().title()

    # extracting hour from 'Start Time' column
    df['hour'] = df['Start Time'].dt.hour
    # displaying the most common start hour
    most_common_hour = df['hour'].value_counts().idxmax()

    print("Most popular month: {}\n".format(most_common_month_name))
    print("Most popular day: {}\n".format(most_common_day))
    print("Most popular start hour: {}\n".format(most_common_hour))

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return most_common_month_int, most_common_day, most_common_hour

def station_statistics(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n*** Calculating The Most Popular Stations and Trip ***\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()


    # display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()

    print("Most commonly used start station: {}\n".format(most_common_start_station))
    print("Most commonly used end station: {}\n".format(most_common_end_station))
    print("Most frequent combination of start station and end station trip:\n{}\n".format(most_common_combination))

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return most_common_start_station, most_common_end_station, most_common_combination

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n*** Calculating Trip Duration ***\n')
    start_time = time.time()

    # display total travel time in seconds
    total_travel = df['Trip Duration'].sum()
    total_pre_conversion = int(total_travel)
    total_conversion = datetime.timedelta(seconds=total_pre_conversion)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    mean_pre_conversion = int(mean_travel)
    mean_conversion = datetime.timedelta(seconds=mean_pre_conversion)
    # mean_travel_time_mins = str(datetime.timedelta(seconds=mean_travel_time_secs))

    print("Total travel time (hh:mm:ss): {}\n".format(total_conversion))
    print("Mean travel time (hh:mm:ss): {}\n".format(mean_conversion))

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return total_travel, mean_travel

def user_stats(df):
    """Displays statistics on bikeshare users."""

    # There doesn't seem to be a gender column in the washington csv file 
    # As a result, this part of the code results in an error when 'washington' is selected by the user
    
    # for col in df.columns: 
    #     print(col) 

    print('\n*** Calculating User Stats ***\n')

    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count of user types:\n{}\n".format(user_types))

    # Display counts of gender
    # As per comment, use a conditional statement to filter out the city of Washington
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts() 
        print("Count of gender types:\n{}\n".format(gender_types))
    else:
        print("No gender data available for your chosen city")

    # Display earliest, most recent, and most common year of birth 
    # As per comment, use a conditional statement to filter out the city of Washington   
    if 'Birth Year' in df.columns:
        earliset_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].value_counts().idxmax()
        print("Earliest, most recent, and most common year of birth:\n{}, {}, {}\n".format(earliset_birth_year, recent_birth_year, most_common_birth_year))
    else:
        print("No birth year data available for your chosen city")
    

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)

# As per comment, use a while loop, keep a counter of the number of rows printed and you can print the next five rows accordingly.
def raw_data(df):
    counter = 10
    while True:
        more_rows = input('\nWould you like to see (more) raw data behind these statistics? Type \'yes\' or \'no\':\n')
        if more_rows == 'yes':
            print(df.iloc[:counter])
            counter += 10
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        restart = input('\nYou have selected these options:\nCity: {}\nMonth: {}\nDay: {}\n\nWould you like to continue with this selection? Type \'yes\' or \'no\':\n'.format(city.title(), month.title(), day.title())).lower()
        if restart.lower() != 'yes':
            get_filters()

        time_statistics(df)
        station_statistics(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
