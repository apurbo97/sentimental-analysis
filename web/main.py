import sys,tweepy,csv,re
from textblob import TextBlob
from flask import Flask,render_template,request


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self,keyword,tweet_no,piedata):
        # authenticating
        consumerKey = 'I7lgWktJS6hiU8mWjjg5KDymy'
        consumerSecret = 'epVxEg8yETOz5U7yk03G0I4LzkAdeVzYWeQxs18aT0bnOxLhn7'
        accessToken = '1170570663918067713-idemngEebiZE8jxxu6XMXe9W7y9Uw1'
        accessTokenSecret = 'ZvvN3DZBvBKx9dCPpDn2XyYw6hgMzL58W21PjhidDr9F4'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # term to be searched and how many tweets to search
        searchTerm = keyword
        NoOfTerms = int(tweet_no)

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0
        general_report="Neutral"


        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        

        if (polarity == 0):
            general_report = "Neutral"
        elif (polarity > 0 and polarity <= 0.3):
            general_report = "Weakly Positive"
        elif (polarity > 0.3 and polarity <= 0.6):
            general_report = "Positive"
        elif (polarity > 0.6 and polarity <= 1):
            general_report = "Strongly Positive"
        elif (polarity > -0.3 and polarity <= 0):
            general_report = "Weakly Negative"
        elif (polarity > -0.6 and polarity <= -0.3):
            general_report = "Negative"
        elif (polarity > -1 and polarity <= -0.6):
            general_report = "Strongly Negative"

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")
        piedata=[positive,wpositive,spositive,negative,wnegative,snegative,neutral,searchTerm,NoOfTerms,general_report]
        print (piedata[6])
        return piedata
       

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

   


#****************************************************************************************************************

app = Flask(__name__)


@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/About')
def about():
    return render_template('about.html')

@app.route('/Analysis',methods=['GET','POST'])
def form():
	if (request.method=='POST'):
		piedata = []
		keyword = request.form.get('keyword')
		tweet_no = request.form.get('tweet_no')
		sa = SentimentAnalysis()
		piedata = sa.DownloadData(keyword,tweet_no,piedata)
		return render_template('view.html',piedata=piedata)


app.run(debug=True)









