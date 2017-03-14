library(tidyverse)

getwd() # this should be directory where sentences.R is placed

tales_not_less_than = 30

our_data <- read.csv("sentence-length.csv", header = TRUE)
our_data <- filter(our_data, our_data$number.of.tales >= tales_not_less_than) # choose with many tales

# View(our_data)

#http://chrisalbon.com/r-stats/cleveland-plot.html
our_plot <- ggplot(data = our_data,
                   aes(x = mean.words.in.sentence,
                       y = reorder(country, mean.words.in.sentence))) +
            geom_point(color = "#8F47B8", size = 3) + # Hexadecimal color
            theme(panel.grid.major.x = element_line(size = 1),
                  panel.grid.minor.x = element_line(size = 1),
                  panel.grid.major.y = element_line(color="gray", linetype="dashed")) +
            ggtitle(paste("http://www.fairy-tales.su/",
                          "\n",
                          "для народностей с не менее чем", tales_not_less_than, "сказками" )) +
            xlab("среднее количество слов в предложении") +
            ylab("народности")

our_plot

ggsave("sentence-length.png", plot = our_plot, width = 8, height = 10)

# ggsave(filename = "sentence-length.pdf", plot = our_plot, device = cairo_pdf, width = 8.27, height = 11.69)

