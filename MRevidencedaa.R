
# DATA ANALYSIS FROM SQLITEDATABASE ---------------------------------------
# Author: Winfred Gatua ---------------------------------------------------
# Date:05/12/2022 ---------------------------------------------------------
#set working directory

setwd("~/OneDrive - University of Bristol/Winfred_PhDApps/Streamlit_MRevidenceentryapp/")

install.packages('RSQLite')

library(RSQLite)
library(dplyr)
library(ggplot2)

con <- dbConnect(SQLite(),'Mr_EvidenceDB')
#list tables
dbListTables(con) #list down the tables
result <- tbl(con, 'results')
results <- data.frame(result)

#odds ratio (ID1)

results %>% 
  filter(effectsizetype_id=="ID1") %>% 
  ggplot(aes(y=results_id,x=effectsize,xmin=lowerinterval,xmax=upperinterval)) +
  geom_point() +
  geom_errorbarh(height=.1) +
  labs(title='Effect Size by Study', x='Effect Size', y = 'Results_ID') +
  geom_vline(xintercept=0, color='black', linetype='dashed', alpha=.5) +
  theme_classic()

#mean difference(ID2)
results %>% 
  filter(effectsizetype_id=="ID2") %>% 
  ggplot(aes(y=results_id,x=effectsize,xmin=lowerinterval,xmax=upperinterval)) +
  geom_point() +
  geom_errorbarh(height=.1) +
  labs(title='Effect Size by Study', x='Effect Size', y = 'Results_ID') +
  geom_vline(xintercept=0, color='black', linetype='dashed', alpha=.5) +
  theme_classic()


# Beta (ID4) --------------------------------------------------------------------
results %>% 
  filter(effectsizetype_id=="ID4") %>% 
  ggplot(aes(y=results_id,x=effectsize,xmin=lowerinterval,xmax=upperinterval)) +
  geom_point() +
  geom_errorbarh(height=.1) +
  labs(title='Effect Size by Study', x='Effect Size', y = 'Results_ID') +
  geom_vline(xintercept=0, color='black', linetype='dashed', alpha=.5) +
  theme_classic()





