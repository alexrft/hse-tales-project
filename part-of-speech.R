library(tidyverse)
library(reshape2)
library(scales)

getwd() # там же должен лежать part-of-speech.csv

tales_not_less_than = 30

our_data <- read.csv(file="part-of-speech.csv", header=TRUE)

# выберем страны где много сказок и удалим ставшие лишними уровни http://stackoverflow.com/a/31428875
our_data <- subset(our_data,  number.of.tales >= tales_not_less_than) %>% droplevels()

our_data <- select(our_data, -number.of.tales) # уберём столбец с количеством сказок

# Переведём из широкого формата в длинный
datm <- melt(our_data, id = "country") %>% 
    arrange(country)

# Переименуем пару столбцов
# http://stackoverflow.com/a/16490387
names(datm)[names(datm) == "variable"] <- "parts"

datm

my_data.summary = datm %>% 
    group_by(country, parts) %>% 
    summarise(count = sum(value)) %>%
    mutate(percent = count/sum(count), pos = cumsum(percent) - 0.5*percent)

my_data.summary


# http://stackoverflow.com/a/34904604
our_plot <- ggplot(data = my_data.summary,
       aes(x = country, y = percent, fill = parts)) +
       geom_bar(stat="identity", width = .7, colour="black", lwd=0.1) +
       geom_text(aes(label=ifelse(percent >= 0.05, paste0(sprintf("%.0f", percent*100),"%"),"")),
                     position=position_stack(vjust=0.5), colour="white") +
       scale_y_continuous(labels = percent_format()) +
       scale_x_discrete(limits = rev(levels(our_data$country)))+
       coord_flip() +
       ggtitle(paste("Распределение по частям речи для народностей с не менее чем 30 сказками",
                  "\n",
                  "в терминах https://tech.yandex.ru/mystem/doc/grammemes-values-docpage/", sep="")) +
       xlab("народности") +
       ylab("") +
       scale_fill_discrete(name = "Части речи:")
    
our_plot
# our_plot + facet_wrap(~parts)

ggsave("part-of-speech.png", plot = our_plot, width = 8, height = 10)

# ggsave(filename = "parts-of-speech.pdf", plot = our_plot, device = cairo_pdf, width = 8.27, height = 3*11.69)

