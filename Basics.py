#!/usr/bin/env python
# coding: utf-8

# # Hacker News Analysis
# 
# This Dataquest task requires me to anaylze Hacker News posts to figure out, out of two types of posts (`Ask HN` and `Show HN`) which receives the most comments, and at what time of day posts receive the most comments overall. 
# 
# This will test some cleaning and importing, but mainly date/time manipulation from some recent packages you'll see below.
# 
# ## Import

# In[1]:


#Import.
from csv import reader

opened_file = open('hacker_news.csv')
read_file = reader(opened_file)
HN = list(read_file)

#Splitting header and body into two.
headers = HN[0]
HN = HN[1:]

print("Header:")
print(headers)
print(" ") #Maybe there's a better way of doing this
print("Body:")
print(HN[3:5])
print(" ")
print("Length of dataset:", [len(HN)])


# ## Cleaning
# 
# Header and data have been split, so now let's filter the data to find our `Ask HN` and `Show HN`, while removing everything else.

# In[2]:


#Create three empty lists
ask_posts = []
show_posts = []
other_posts = []

#Loop through to each list
for posts in HN:
    title = posts[1]
    if title.lower().startswith("ask hn"):
        ask_posts.append(posts)
    elif title.lower().startswith("show hn"):
        show_posts.append(posts)
    else:
        other_posts.append(posts)
    
print("Length of Ask HN:", len(ask_posts))
print("Length of Show HN:", len(show_posts))
print("Length of others:", len(other_posts))
print(" ")
print("Length check:", len(ask_posts)+len(show_posts)+len(other_posts), "vs.", len(HN)) #Surely a bad way of doing this


# Our total matches the above figure, and we've split the list out ensuring that we'll include both upper and lower cases if the posts were different.
# 
# ## Analysis 1: Average number of comments per post type
# Cleaning over, let's analyze `Ask HN` and `Show HN` to see which gets more comments.

# In[3]:


#Variables starting with 0:
total_ask_comments = 0
total_show_comments = 0

#Iterate over ask and convert to integer, add those to the empty variable
for post in ask_posts:
    total_ask_comments += int(post[4])

avg_ask_comments = total_ask_comments / len(ask_posts) #Make an average
avg_ask_comments = round(avg_ask_comments, 2) #Let's tidy this up

print("Average number of Ask HN comments:", avg_ask_comments)

for post in show_posts:
    total_show_comments += int(post[4])    
    
avg_show_comments = total_show_comments / len(show_posts)
avg_show_comments = round(avg_show_comments, 2)

print("Average number of Show HN comments:", avg_show_comments)
print("")

difference = avg_ask_comments - avg_show_comments
difference = round(difference, 2)
print("Ask HN posts get", difference, "more comments on average.")


# ## Analysis 2: What time gets the most comments?
# `Ask HN` posts are the overall winner. People like to be asked things, and less so like to comment on things others have done. Incredible.
# 
# But what time are people most likely to answer questions? Let's find out in a couple of steps:
# 
# First, I'll calculate the amount of `Ask HN` posts created at each hour of the day. This includes the number of comments received.
# 
# Second, I'll calculate the average number of comments ask posts receive by hour created.
# 
# We're going to work with the datetime package to make analysis of date strings somewhat better. But before that, I'll make a results list which isolate comments by the number of comments and when they were created.

# In[4]:


result_list = []

#This was done in a single line elsewhere but I've added variables
for post in ask_posts:
    num_comments = int(post[4])
    created_at = post[6]
    result_list.append([created_at, num_comments])

#Let's get the results
result_list


# Now let's use datetime (and our new friends strptime and strftime) to parse these strings into a date format, then represent only the hour.
# 
# (I've only used these ONCE before in learning, so this code was mainly copied over from an answer and then edited to make more clear for myself).

# In[5]:


import datetime as dt

counts_by_hour = {}
comments_by_hour = {}
date_format = "%m/%d/%Y %H:%M" #Clever way of simplifying

for row in result_list:
    created_at = row[0]
    number_of_comments = row[1]
    hour = dt.datetime.strptime(created_at, date_format).strftime("%H")
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = number_of_comments
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += number_of_comments
        
comments_by_hour


# We've now seen, by hour, the total number of comments created. Clearly, `15`, or 3 o'clock, is the time most posters are active. But for analysis, let's average the times anyway. (2 a.m. is also a curious outlier).
# 
# To calculate the average, we use a special technique:
# 
# 1) Create (initialize) an empty list
# 
# 2) Loop (iterate) over the keys of a dictionary and append to the initial list another list with some magic ****ing calculation. These nerds are the worst at explaining what to do sometimes.

# In[6]:


avg_by_hour = []

for hour in comments_by_hour:
    avg_by_hour.append([hour, comments_by_hour[hour] / counts_by_hour[hour]])
    
avg_by_hour


# # Cleaning the analysis
# 
# The output is unordered, We can see 15 (or 3pm) has the highest average, but it wasn't easy! Let's just spend some time sorting this out for clearer reading.

# In[7]:


swap_avg_by_hour = []

for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]]) #Fancy!

print(swap_avg_by_hour[:1])


# In[8]:


#Use the sorted() function to sort swap_avg_by_hour in descending order.
sorted_swap = sorted(swap_avg_by_hour, reverse=True)

#And this below orders our results by top 5, but we can do better!
sorted_swap[:5]


# ## The REAL top five hours for posting
# 
# Formatted and everything:

# In[18]:


for avg, hr in sorted_swap[:5]:
    print ("At {} there were {:.2f} comments per post (on average)".format(
            dt.datetime.strptime(hr, "%H").strftime("%H:%M"),avg))


# So, lots of posts at 3 p.m. and 2 a.m. I'd be interested to find out what is getting posted at 2 a.m. that gets so much traffic, but as a business, we'd ruin the 3 p.m. timeslot with 'content marketing'.
