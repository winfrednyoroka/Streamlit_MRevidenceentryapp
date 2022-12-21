
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





