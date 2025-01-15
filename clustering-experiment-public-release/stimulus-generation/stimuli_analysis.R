library(tidyverse)
stims = read_csv("output.csv")

sum = stims %>% 
  group_by(n) %>% 
  summarise(mean_vaccuumed_z_score = mean(vacuumed_z_score), sd_vaccuumed_z_score = sd(vacuumed_z_score))

sum %>% ggplot(aes(n, mean_vaccuumed_z_score)) + geom_point()
sum %>% ggplot(aes(n, sd_vaccuumed_z_score)) + geom_point()
