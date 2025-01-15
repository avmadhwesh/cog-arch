library(lme4)
library(tidyverse)
library(car)
library(MuMIn)
library(jsonlite)

# Reliability analysis

reliability_df = read_json("data/clustering-pairs.json", simplifyVector = TRUE) %>%
  mutate(number_of_clusters_diff = number_of_clusters_stim_1 - number_of_clusters_stim_2) %>% 
mutate(online = !experiment_version == 1)

# Sanity checks for online condition
mod1 = lmer(fowlkes_mallows_index ~ 1 + number_of_points * group + online + (1|participant_id) + (1|base_uuid), data=reliability_df)
mod2 = lmer(fowlkes_mallows_index ~ 1 + number_of_points * group + (1|participant_id) + (1|base_uuid), data=reliability_df)

# Online is not necessary
model.sel(mod1, mod2)

mod = lmer(duration_stim_2 ~ 1 +flipped + (1|participant_id) + (1|base_uuid), data=reliability_df)
summary(mod)
mod %>% Anova(type=3)

# Flipped is not necessary
lmer(fowlkes_mallows_index ~ 1 + flipped + (1|participant_id) + (1|base_uuid), data = reliability_df) %>% summary()

model = lmer(fowlkes_mallows_index ~ 1 + number_of_points * group + (1|participant_id) + (1|base_uuid), data = reliability_df, control = lmerControl(optCtrl=list(maxfun=1e7, optimizer="bobyqa")))

model %>% summary()

Anova(model, type = 3)

model = lmer(abs(number_of_clusters_diff) ~ 1 + number_of_points * group + (1|participant_id) + (1|base_uuid), data = reliability_df)

model  %>%
  Anova(type = 3)

model %>% summary()

cdf = read_csv("data/clustering-cross-participants.csv")

tmp = cdf %>% group_by(participant_id_1, cluster_structure, number_of_points, base_uuid) %>% summarize(fowlkes_mallows_index = mean(fowlkes_mallows_index))

model = lmer(fowlkes_mallows_index ~ 1 + number_of_points * cluster_structure + (1|participant_id_1) + (1|base_uuid), data = tmp)

model %>% summary()

model %>% Anova(type = 3)

df = read_csv("build/clusters_data.csv")

tmp = df %>% group_by(participant_id, base_uuid, number_of_points, cluster_structure, trial_number) %>% summarize(n_clusters = n())

model = lmer(n_clusters ~ 1 + number_of_points * cluster_structure + (1|participant_id) + (1|base_uuid), data = tmp)

model %>% summary()

model %>% Anova(type = 3)

analyze_attribute = function (variable_name, data) {
  
  if (variable_name == "area" | variable_name == "linearity" | variable_name == "density") {
    data = data %>% filter(numerosity >= 3)
  }
  
  model1formula = paste0(variable_name, " ~ 1 + number_of_points + cluster_structure +
                 (1 | participant_id) + (1 | base_uuid)")
  
  model2formula = paste0(variable_name, " ~ 1 + number_of_points * cluster_structure +
                 (1 | participant_id) + (1 | base_uuid)")
  
  # model1 = lmer(model1formula, 
  #               data=data, control=lmerControl(optCtrl=list(maxfun=1e7, optimizer="bobyqa")))
  # model2 = lmer(model2formula, 
  #               data=data, control=lmerControl(optCtrl=list(maxfun=1e7, optimizer="bobyqa")))
  # models = list(model1, model2)
  # selection = model.sel(models)
  # best_model = models[[(selection %>% row.names)[1] %>% as.numeric()]]
  best_model = lmer(model2formula,data=data, control=lmerControl(optCtrl=list(maxfun=1e7, optimizer="bobyqa")))
  print(Anova(best_model, type = 3))
  print(best_model %>% summary())
}

analyze_attribute("convex_hull_point_percentage", df)




