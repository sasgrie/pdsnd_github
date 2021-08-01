import time

import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#initalising lists for days and months that are being used in the functions incl. all
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    # get user input for city, month & day using while loops to deal with incorrect input
    
    city = input('Choose for which city you want data displayed: Chicago, New York City, Washington:\n').lower()
    while city not in CITY_DATA.keys():
        city = input('Invalid input - please try again \nChoose for which city you want data displayed - Chicago, New York City, Washington:\n').lower()  
   
    month = input('Choose a month for which you want data displayed. Type: January, February, March... or all (for no filter):\n').lower()
    while month not in MONTHS:
        month = input('Invalid input - please try again \nChoose for which motnh you want data displayed Type: January, February, March... or all:\n').lower()
    
    
    day = input('Choose a day for which you want data displayed. Type: Monday, Tuesday, Wednesday... or all (for no filter):\n').lower()
    while day not in DAYS:
        day = input('Invalid input - please try again \nChoose a day for which you want data displayed. Type: Monday, Tuesday, Wednesday... or all (for no filter):\n').lower()
    
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns for these
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # create a concat of start and end station columns for route in the station stat function
    df['combi_start_end'] = df['Start Station'] + ' -- ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['weekday'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month using mode function
    common_month = df['month'].mode()[0]
    #use index of the months list to get corresponding month name (-1 to account for index starting at 0)
    common_month = MONTHS[common_month - 1] 
    print('Most common month: {}'.format(common_month.title()))
    
    # display the most common day of week using mode function
    common_weekday = df['weekday'].mode()[0]
    print('Most common day of the week: {}'.format(common_weekday))
    
    # display the most common start hour using mode function
    common_hour = df['hour'].mode()[0]
    print('Most common start hour: {}'.format(common_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station using mode function
    common_start = df['Start Station'].mode()[0]
    print('Most popular start station: {}'.format(common_start))
    
    # display most commonly used end station using mode function
    common_end = df['End Station'].mode()[0]
    print('Most popular end station: {}'.format(common_end))
    
    # display most frequent combination of start station and end station trip using mode function
    common_route = df['combi_start_end'].mode()[0]
    print('Most popular distance: {}'.format(common_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in min and hour
    total_time_min = round(df['Trip Duration'].sum() / 60, 2)
    total_time_hr = round(total_time_min / 60, 2)
    print('Total travel time: {} minutes \nor \nTotal travel time: {} hours'.format(total_time_min, total_time_hr))

    # display mean travel time in min
    mean_time = round(df['Trip Duration'].mean() / 60, 2)
    print('Mean travel time: {} minutes'.format(mean_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types in a dataframe for better reading exp
    count_user = df['User Type'].value_counts().to_frame('count')
    print('Count of users by type: \n {}'.format(count_user))
    print('\n' * 2)
    
    # Display counts of gender in a dataframe for better reading exp 
    if 'Gender' in df.columns:
        count_gender = df['Gender'].value_counts().to_frame('count')
        print('Count of users by gender: \n {}'.format(count_gender))
        print('\n' * 2)
    # Display earliest (min), most recent(max), and most common (mode) year of birth
    if 'Birth Year' in df.columns:
        print('Earliest birth year: {}'.format(int(df['Birth Year'].min())))  
        print('Most recent birth year: {}'.format(int(df['Birth Year'].max())))
        print('Most common birth year: {}'.format(int(df['Birth Year'].mode()[0])))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays (repeatedly) 5 rows of starting dataframe following user's input"""
    i = 0
    display_data = input("Would you like to see the first 5 lines of raw data? Type 'yes' or 'no': ").lower() 
    
    # loop and if-clause to check for invalid input and to display additional rows if requested by user
    while True:
        if display_data == 'no':
            break
        elif display_data == 'yes' :
            print(df[i:i+5])
            display_data = input("\nWould you like to see next rows of raw data? Type 'yes' or 'no': ").lower()
            i += 5
        else:
            print("\nInvalid input. Please try again:")
            display_data = input("\nWould you like to see first 5 rows of raw data? Type 'yes' or 'no': ").lower()
            continue

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
