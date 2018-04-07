import time
import pandas as pd
import numpy as np
import csv
import pprint
import datetime
import calendar
from scipy.stats.mstats import mode
from scipy import stats
import itertools

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

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print('Hello! Let\'s explore some US bikeshare data!')
        city = input('\nWould you like to see data for Chicago, New York city, or Washington?\n')
        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print('\n That input is not valid. Please try again. \n')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you like to view data for?\n'
                    'Please choose January, February, March, April, May, June or All if you would like to view all months!\n')
        if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('\n That input is not valid. Please try again. \n')
            continue
        else:
            break



    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day would you like to view data for?\n'
                    'Please choose Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or ALL if you would like to view all months!\n')
        if day.lower() not in ('monday', 'tuesday', 'wednesay', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print('\n That input is not valid. Please try again. \n')
            continue
        else:
            break

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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

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
    common_month = df['month'].mode()[0]
    print('The most common month:', common_month)
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day:', common_day)
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start = df['Start Station'].mode()[0]
    print('The most commonly used start station:', start)

    # display most commonly used end station
    end = df['End Station'].mode()[0]
    print('The most commonly used end station:', end)

    # display most frequent combination of start station and end station trip
    combo_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    print('The most frequent combination of Start and End stations:', combo_station.head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print('Total travel time, in seconds:', total)
    # display mean travel time
    mean = df['Trip Duration'].mean()
    print('Mean travel time, in seconds:', mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Type of users,:\n', user_types)
    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('Gender count:\n', gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].sort_values(ascending=True)
        recent = df['Birth Year'].sort_values(ascending=False)
        common = df['Birth Year'].mode()[0]
        print('Earliest year:', earliest.head(1))
        print('Most recent year:', recent.head(1))
        print('Most common year of birth:', common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
