
# DATA ANALYSIS FROM SQLITEDATABASE ---------------------------------------
# Author: Winfred Gatua ---------------------------------------------------
# Date:05/12/2022 ---------------------------------------------------------
#set working directory

setwd("~/OneDrive - University of Bristol/Winfred_PhDApps/Streamlit_MRevidenceentryapp/")

#install.packages('RSQLite')

library(RSQLite)
library(dplyr)
library(ggplot2)
library(plotly)
library(gridExtra)
library(tidyverse)
library(forestploter)
library(grid)

con <- dbConnect(SQLite(),'Mr_EvidenceDB')
#list tables
dbListTables(con) #list down the tables
result <- tbl(con, 'results')
results <- data.frame(result)

#obtain some entries from results table
results <- dbGetQuery(con, 'SELECT * FROM results')
results
#odds ratio (ID1)

p1 <- results %>% 
  group_by(pmid) %>% 
  #filter(effectsizetype_id=="ID1") %>% 
  ggplot(aes(y=fct_rev(as.character(pmid)),x=effectsize,xmin=lowerinterval,xmax=upperinterval)) +
  geom_point(aes(color=methodid)) +
  geom_errorbarh(height=.1) +
  labs(title='Effect Size by study', x='Odds Ratio', y = 'Study_PMID') +
  geom_vline(xintercept=1, color='black', linetype='dashed', alpha=.5) +
  facet_wrap(vars(pmid))+
  theme_classic()
ggplotly(p1)

#mean difference(ID2)
P2 <- results %>% 
  filter(effectsizetype_id=="ID2") %>% 
  ggplot(aes(y=results_id,x=effectsize,xmin=lowerinterval,xmax=upperinterval)) +
  geom_point(aes(color=methodid)) +
  geom_errorbarh(height=.1) +
  labs(title='Effect Size by results', x='Mean difference', y = 'Results_ID') +
  geom_vline(xintercept=1, color='black', linetype='dashed', alpha=.5) +
  theme_classic()

ggplotly(P2)


# Beta (ID4) --------------------------------------------------------------------
P3 <- results %>% 
  filter(effectsizetype_id=="ID4") %>% 
  ggplot(aes(y=results_id,x=effectsize,xmin=lowerinterval,xmax=upperinterval)) +
  geom_point(aes(color=methodid)) +
  geom_errorbarh(height=.1) +
  labs(title='Effect Size by results', x='Betas', y = 'Results_ID') +
  geom_vline(xintercept=0, color='black', linetype='dashed', alpha=.5) +
  theme_classic()

ggplotly(P3)



# Make forest plot using forestploter -------------------------------------
dt <- dbGetQuery(con, 'SELECT * FROM results')
dt
#Create an empty and or blank column
dt$` ` <- paste(rep(" ", 20),collapse=" ")

#create the confidence interval column

dt$`MD (95% CI)` <- sprintf("%.2f (%.2f - %.2f)",dt$effectsize,dt$lowerinterval,dt$upperinterval)
head(dt)

dt <- dt %>% 
  filter(effectsizetype_id=="ID2") 

#define the theme

tm <- forest_theme(ci_pch = 20,
                   ci_col = "blue",
                   ci_fill = "red",
                   ci_alpha = 1,
                   ci_Theight = 0.3,
                   refline_col = "red",
                   legend_value = c("O6","O7"),)
  
p <- forest(dt[,c(2,13:14)],
          est = dt$effectsize,
          lower = dt$lowerinterval,
          upper = dt$upperinterval,
          sizes = 0.8,
          ci_column = 2,
         ref_line = 0,
         xlim = c(-1,17),
         footnote = "These are \nthe study PMIDs",
         xlab = "Mean Difference",
         title = "Forest plot showing the mean differences of BMI\n and DBP and SBP",
         theme = tm)
plot(p)

#get the metrics of the plot and save it
p_wh <- get_wh(plot = p, unit = "in")
png('Figures/Meandifferenceplot.png', res = 300, width = p_wh[1], height = p_wh[2], units = "in")
p
dev.off()


# Make a forest plot with Odds ratio only ---------------------------------
dt_or <- dbGetQuery(con, 'SELECT * FROM results')
dt_or
#Create an empty and or blank column
dt_or$` ` <- paste(rep(" ", 20),collapse=" ")

#create the confidence interval column

dt_or$`OR (95% CI)` <- sprintf("%.2f (%.2f - %.2f)",dt_or$effectsize,dt_or$lowerinterval,dt_or$upperinterval)
head(dt)

dt_or <- dt_or %>% 
  filter(effectsizetype_id=="ID1") 

#define the theme

tm <- forest_theme(ci_pch = 20,
                   ci_col = "blue",
                   ci_fill = "red",
                   ci_alpha = 1,
                   ci_Theight = 0.3)

p <- forest(dt_or[,c(2,13:14)],
            est = dt_or$effectsize,
            lower = dt_or$lowerinterval,
            upper = dt_or$upperinterval,
            sizes = 0.8,
            ci_column = 2,
            ref_line = 1,
            arrow_lab = c("Decreased risk", "Increased risk"),
            xlim = c(-1,7),
            footnote = "These are \nthe study PMIDs",
            xlab = "Odds Ratio",
            theme = tm)
plot(p)

#get the metrics of the plot and save it
p_wh <- get_wh(plot = p, unit = "in")
png('Figures/oddsratio_plot.png', res = 300, width = p_wh[1], height = p_wh[2], units = "in")
p
dev.off()

# Make a forest plot with Beta estimates ----------------------------------

dt_beta <- dbGetQuery(con, 'SELECT * FROM results')
dt_beta
#Create an empty and or blank column
dt_beta$` ` <- paste(rep(" ", 20),collapse=" ")

#create the confidence interval column

dt_beta$`BETA (95% CI)` <- sprintf("%.2f (%.2f - %.2f)",dt_beta$effectsize,dt_beta$lowerinterval,dt_beta$upperinterval)
head(dt_beta)

dt_beta <- dt_beta %>% 
  filter(effectsizetype_id=="ID4") 

#define the theme

tm <- forest_theme(ci_pch = 20,
                   ci_col = "blue",
                   ci_fill = "red",
                   ci_alpha = 1,
                   ci_Theight = 0.3)

p <- forest(dt_beta[,c(2,13:14)],
            est = dt_beta$effectsize,
            lower = dt_beta$lowerinterval,
            upper = dt_beta$upperinterval,
            sizes = 0.8,
            ci_column = 2,
            ref_line = 0,
            xlim = c(-1,20),
            footnote = "These are \nthe study PMIDs",
            xlab = "Beta estimates",
            theme = tm)
plot(p)

#get the metrics of the plot and save it
p_wh <- get_wh(plot = p, unit = "in")
png('Figures/betaplot.png', res = 300, width = p_wh[1], height = p_wh[2], units = "in")
p
dev.off()
# Make a forest plot for Hazard ratios ------------------------------------

dt_hr <- dbGetQuery(con, 'SELECT * FROM results')
dt_hr
#Create an empty and or blank column
dt_hr$` ` <- paste(rep(" ", 20),collapse=" ")

#create the confidence interval column

dt_hr$`HR (95% CI)` <- sprintf("%.2f (%.2f - %.2f)",dt_hr$effectsize,dt_hr$lowerinterval,dt_hr$upperinterval)
head(dt_hr)

dt_hr <- dt_hr %>% 
  filter(effectsizetype_id=="ID3") 

#define the theme

tm <- forest_theme(ci_pch = 20,
                   ci_col = "blue",
                   ci_fill = "red",
                   ci_alpha = 1,
                   ci_Theight = 0.3)

p <- forest(dt_hr[,c(2,13:14)],
            est = dt_hr$effectsize,
            lower = dt_hr$lowerinterval,
            upper = dt_hr$upperinterval,
            sizes = 0.8,
            ci_column = 2,
            ref_line = 0,
            xlim = c(-1,17),
            footnote = "These are \nthe study PMIDs",
            theme = tm)
plot(p)

#get the metrics of the plot and save it
p_wh <- get_wh(plot = p, unit = "in")
png('Figures/hazardratioplot.png', res = 300, width = p_wh[1], height = p_wh[2], units = "in")
p
dev.off()

# Make forest plot for riskdifference -------------------------------------

dt_rd <- dbGetQuery(con, 'SELECT * FROM results')
dt_rd
#Create an empty and or blank column
dt_rd$` ` <- paste(rep(" ", 20),collapse=" ")

#create the confidence interval column

dt_rd$`RD (95% CI)` <- sprintf("%.2f (%.2f - %.2f)",dt_rd$effectsize,dt_rd$lowerinterval,dt_rd$upperinterval)
head(dt_rd)

dt_rd <- dt_rd %>% 
  filter(effectsizetype_id=="ID5") 

#define the theme

tm <- forest_theme(ci_pch = 20,
                   ci_col = "blue",
                   ci_fill = "red",
                   ci_alpha = 1,
                   ci_Theight = 0.3)

p <- forest(dt_rd[,c(2,13:14)],
            est = dt_rd$effectsize,
            lower = dt_rd$lowerinterval,
            upper = dt_rd$upperinterval,
            sizes = 0.8,
            ci_column = 2,
            ref_line = 0,
            xlim = c(-1,2),
            footnote = "These are \nthe study PMIDs",
            xlab = "Risk Difference",
            theme = tm)
plot(p)

#get the metrics of the plot and save it
p_wh <- get_wh(plot = p, unit = "in")
png('Figures/riskdifferenceplot.png', res = 300, width = p_wh[1], height = p_wh[2], units = "in")
p
dev.off()
