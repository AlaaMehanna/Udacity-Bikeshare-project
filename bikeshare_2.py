import time
import pandas as pd
import numpy as np

CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'w': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities=['ch','ny','w']
    city= input('Please specify which city you want to show data about \n type (ch) for chicago\n type (ny) for New york city\n type (w) for washington\n ').lower()
    while city not in cities :
        print('That is incorrect input, please check your spelling and try again')    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city= input('Please specify which city you want to show data about \n type (ch) for chicago\n type (ny) for New york city\n type (w) for washington\n ').lower()
    # get user input for month (all, january, february, ... , june)
    months=['january','february','march','april','may','june','all']
    month=input('please specify which month you want the data to be filtered by: \n january\n february\n march\n april\n may\n june\n all\n').lower()
    while month not in months:
        print('That is incorrect input, please check your spelling and try again')
        month=input('please specify which month you want the data to be filtered by: \n january\n february\n march\n april\n may\n june\n all\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days=['saturday','sunday','monday','tuesday','wednesday','thursday','friday','all']
    day=input('please specify which day you want the data to be filtered by: \n saturday\n sunday\n monday\n tuesday\n wednesday\n thursday\n friday\n all\n').lower()
    while day not in days:
        print('That is incorrect input, please check your spelling and try again')
        day=input('please specify which day you want the data to be filtered by: \n saturday\n sunday\n monday\n tuesday\n wednesday\n thursday\n friday\n all\n').lower()


    print('-'*40)
    return city, month, day

def load_data(city, month, day):
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month=df['month'].mode()[0]
    print('The most common month is: ', common_month)

    # display the most common day of week
    common_day=df['day_of_week'].mode()[0]
    print('The most common day is: ',common_day)

    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    common_hour=df['hour'].mode()[0]
    print('The most common Hour is: ',common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start=df['Start Station'].mode()[0]
    print('The most used Start Staion is: ',common_start)
    # display most commonly used end station
    common_end=df['End Station'].mode()[0]
    print('The most used End Station is: ',common_end)
    # display most frequent combination of start station and end station trip
    df['trip route']=df['Start Station']+"  'AND'  "+df['End Station']
    common_route=df['trip route'].mode()[0]
    print('The most used combination is: ',common_route)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time=df['Trip Duration'].sum()
    print("Total Travel Time in 'mins' is: ",travel_time/60)
    # display mean travel time
    avg_time=df['Trip Duration'].mean()
    print("Average travel time in 'mins' is: ",avg_time/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print(user_types)
    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts().to_frame()
        print(gender_counts)
    # Display earliest, most recent, and most common year of birth

        earliest=df['Birth Year'].min()
        most_recent=df['Birth Year'].max()
        most_common=df['Birth Year'].mode()[0]
        print('The earliest year of birth is : ',int(earliest))
        print('The most recent year of birth is : ',int(most_recent))
        print('The most common year of birth is : ',int(most_common))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        print('This data is not available for Washington')

def display_raw_data(city):
    print('\nRaw data is available to check... \n')
    display_raw = input('To View the availbale raw data in chuncks of 5 rows type: Yes or No if you don\'t want \n').lower()
    while display_raw not in ('yes', 'no'):
        print('That\'s invalid input, please check your spelling and try again')
        display_raw = input('To View the availbale raw data in chuncks of 5 rows type: Yes or No if you don\'t want \n').lower()
   # The second while loop is on the same level and doesn't belong to the first.
    while display_raw == 'yes':
        try:
            for chunk in pd.read_csv(CITY_DATA[city], index_col = 0 ,chunksize=5):
                print(chunk)
                display_raw = input('To View another sample of raw data in chuncks of 5 rows type: Yes\n').lower()
                if display_raw != 'yes':
                    print('Thank You!')
                    break
            break

        except KeyboardInterrupt:
            print('Thank you!')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        x=display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
