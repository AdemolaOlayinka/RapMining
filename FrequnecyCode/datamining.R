setwd("~/Documents")
library(ggplot2)
library(dplyr)
library(tidyr)
library(reshape2)
library(RColorBrewer)

## Rap Analysis Project Data Cleaning

# Get hit and non-hit themes
hits <- read.csv('large_corpus_themes_hits.csv')

# Get top 20 themes
themes <- colnames(hits)[-1]

## Cleaning up our own data
## Making Relative Freqeuncies of Artists Over Time

# Get data
topics <- read.csv('topic_model_counts.csv')

# Split into multiple columns
top <- topics[,c(4,5)]
sec <- topics[,c(4,6)]
third <- topics[,c(4,7)]
fourth <- topics[,c(4,8)]
fifth <- topics[,c(4,9)]

names <- c("year","topic")

colnames(top) <- names
colnames(sec) <- names
colnames(third) <- names
colnames(fourth) <- names
colnames(fifth) <- names

# Make into master dataset
counts_year <- bind_rows(top, sec)
bind_rows(counts_year, third)
bind_rows(counts_year, fourth)
bind_rows(counts_year, fifth)

# Get overall summaries
freqs_by_year <- count(group_by(counts_year,year),topic)

# Take into account 0's when topic not mentioned
for(i in seq(1981,2017,by=1)) {
  current <- subset(freqs_by_year, freqs_by_year$year == i) 
  for(x in themes) {
    mentioned <- FALSE;
    for(z in current$topic) {
      if(x == z) {
        mentioned <- TRUE;
      }
    }
    if(mentioned == FALSE) {
      row <- c(i, x, 0)
      totRows <- dim(freqs_by_year)[1]
      freqs_by_year[totRows+1,] <- row
    }
  }
}

# Make all vals check out with type
freqs_by_year$n <- as.integer(freqs_by_year$n)

# Get total counts
div <- freqs_by_year %>%
  group_by(year) %>%
  summarise(total = sum(n))

# Add total counts
freqs_by_year <- left_join(freqs_by_year, div, by = "year")

# Remove any blank data
freqs_by_year <- subset(freqs_by_year, topic != "")

# Get relative frequencies
freqs_by_year$freq <- freqs_by_year$n/freqs_by_year$total

# Change format for better graphing
freqs_by_year <- freqs_by_year[,c(1,2,5)]
freqs_by_year$year <- as.integer(freqs_by_year$year)

# Create color palette for visualization
colors <- c('#77ACD1',
            '#CEDDF1',
            '#FFB16D',
            '#FFD6AD',
            '#7FC57F',
            '#C0ECB8',
            '#E67C7C',
            '#FFC0BF',
            '#BEA3D7',
            '#DCCFE5',
            '#B99892',
            '#DBC3BE',
            '#EEACDA',
            '#FAD3E4',
            '#B1B1B1',
            '#DDDDDD',
            '#D6D779',
            '#E9E9BA',
            '#72D7E2',
            '#C4E9EF')

# Now plot over time
ggplot(aes(x=year,y=freq,group=topic,fill=topic),data=freqs_by_year) +
  geom_line() +
  xlab("Year") +
  ylab("Relative Frequency") +
  ggtitle("Relative Frequency of Topics by Selected Hip-Hop Artists, 1984-2017") + 
  theme(plot.title = element_text(hjust = 0.5),
        panel.background = element_blank()) + 
  xlim(1984,2017) + 
  geom_area(position = "stack") +
  scale_fill_manual(values = colors)

# Get summaries for each of top 5 topics
# This time for GOF, so by artist
top <- as.data.frame(count(group_by(topics, Artist), Top))
sec <- as.data.frame(count(group_by(topics, Artist), Second))
third <- as.data.frame(count(group_by(topics, Artist), Third))
fourth <- as.data.frame(count(group_by(topics, Artist), Fourth))
fifth <- as.data.frame(count(group_by(topics, Artist), Fifth))

# Names for new columns
names <- c("artist","topic","n")

colnames(top) <- names
colnames(sec) <- names
colnames(third) <- names
colnames(fourth) <- names
colnames(fifth) <- names

# Make into large dataset
counts_artist <- bind_rows(top, sec)
bind_rows(counts_artist, third)
bind_rows(counts_artist, fourth)
bind_rows(counts_artist, fifth)

# Get overall summaries
topics_final <- counts_artist %>%
  group_by(artist, topic) %>%
  summarise(n = n())

# Get list of unique artists
artists <- count(group_by(topics_final, artist))[,1]

# Take into account 0's when topic not mentioned
for(i in artists$artist) {
  current <- subset(topics_final, topics_final$artist == i) 
  for(x in themes) {
    mentioned <- FALSE;
    for(z in current$topic) {
      if(x == z) {
        mentioned <- TRUE;
      }
    }
    if(mentioned == FALSE) {
      row <- c(i, x, 0)
      totRows <- dim(topics_final)[1]
      topics_final[totRows+1,] <- row
    }
  }
}

# Make all vals check out with type
topics_final$n <- as.integer(topics_final$n)

# Now get total number of topics for each artist
total_topics <- topics_final %>%
  group_by(artist) %>%
  summarise(total = sum(n))

# Now get active years
years <- topics %>%
  group_by(Artist) %>%
  summarise(start = min(Year), end = max(Year))
colnames(years) <- c('artist','start','end')

# Add total counts
topics_final <- left_join(topics_final, total_topics, by = "artist")

# Also add artists active dates
topics_final <- left_join(topics_final, years, by = "artist")

# Remove any blank data
topics_final <- subset(topics_final, topic != "")

# Get relative frequencies
topics_final$freq <- topics_final$n/topics_final$total

# Create data frame to store GOF output
distances <- data.frame(chisq = numeric(),
                        pval = numeric(),
                        resid = numeric())

# Now we want to compare each artist
# Over the mean relative frequency of themes
# For hit and non-hit data
for (i in years$artist) {
  
  # Go through artists and start/end date
  start <- years$start[years$artist == i]
  end <- years$end[years$artist == i]
  
  # Subset larger data
  current <- subset(hits, Year %in% c(start:end))[,-1]
  nullProbs <- c(colMeans(current[sapply(current, is.numeric)]))

  # Transform artist data for GOF
  artist_data <- subset(topics_final, artist == i)
  counts <- artist_data$n
  
  # Run anova comparing frequencies here
  test <- chisq.test(counts, p=nullProbs, rescale.p = TRUE)
  data <- c(test$statistic, test$p.value, test$residuals)
  totRows <- dim(distances)[1]
  distances[totRows+1,] <- data
}

distances <- bind_cols(distances,years)
