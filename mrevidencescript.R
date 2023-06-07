
setwd("~/OneDrive - University of Bristol/Winfred_PhDApps/Streamlit_MRevidenceentryapp/")




## Load the libraries. 
library(metafor)
library(tidyverse)
library(ggplot2)
library(plotly)
library(patchwork)
library(gridExtra)
library(Rclean)


## Read in the data. 

dat1 <- read.csv("BMI_Hypertension_SBP_DBP_MRevidencecsv.txt",header = TRUE,sep = "\t") #read in the data
#make a unique id without resultsid to takeup the y-axis
dat1$ID <- paste(dat1$author,dat1$pmid.y,dat1$year, sep = "_")


## Define helper functions. 

scale_or <- function(data, estimate, lowerbound, upperbound,
    sd) {
    data_modified <- data %>%
        mutate(OR_LI = round(exp((((log(estimate)/log(10)) -
            (1.96 * (((log(upperbound) - log(lowerbound))/(2 *
                1.96))/sqrt(3)))) * sd) * log(10)),
            digits = 2)) %>%
        mutate(OR_UI = round(exp((((log(estimate)/log(10)) +
            (1.96 * (((log(upperbound) - log(lowerbound))/(2 *
                1.96))/sqrt(3)))) * sd) * log(10)),
            2)) %>%
        mutate(oddsratio = round(exp(((log(estimate)/log(10)) *
            sd) * log(10)), 2))
    return(data_modified)
}

duplicate_subset <- function(data, estimate, lowerbound,
                             upperbound, sd) {
  data_duplicatedcolumns <- data %>%
    mutate(OR_LI = lowerbound) %>%
    mutate(OR_UI = upperbound) %>%
    mutate(oddsratio = estimate)
  return(data_duplicatedcolumns)
}

# Wes Spiller 2022 - calculate the confidence
# intervals given point estimates and pvalue only
CI_calc_lower <- function(est, p) {
  z = -0.862 + sqrt(0.743 - 2.404 * log(p))
  se = est/z
  lower_interval = est - (1.96 * se)
  return(lower_interval)
}

CI_calc_upper <- function(est, p) {
  z = -0.862 + sqrt(0.743 - 2.404 * log(p))
  se = est/z
  upper_interval = est + (1.96 * se)
  return(upper_interval)
}


# head(dat1) Hypertension, odds ratio
P1 <- dat1 %>%
  arrange(ID) %>%
  filter(effectsizetype_id == "ID1" & OUTCOMEID ==
           "O1" & exposurenotes == "Adult" & outcomenotes !=
           "Gestational hypertension" & outcomenotes !=
           "Incident hypertension" & population == "EUR" &
           AnalysisType == "Main" & EXPOSURE == "BMI")

# Subset1 consist of entries that need scaling
subset1 <- P1 %>%
  filter(sd != 0)
# subset1 Subset2 consist of entries that need
# not scaling
subset2 <- P1 %>%
  filter(sd == 0)
# subset2 Scaling
subset1 <- scale_or(data = subset1, estimate = subset1$effectsize,
                    lowerbound = subset1$lowerinterval, upperbound = subset1$upperinterval,
                    sd = subset1$sd)
subset2 <- duplicate_subset(data = subset2, estimate = subset2$effectsize,
                            lowerbound = subset2$lowerinterval, upperbound = subset2$upperinterval,
                            sd = subset2$sd)
# Combine the two subsets
Total <- rbind(subset1, subset2)
# Total

# Systolic blood pressure, Beta estimates
P2 <- dat1 %>%
  arrange(ID) %>%
  filter(effectsizetype_id == "ID4" & OUTCOMEID ==
           "O2" & AnalysisType == "Main" & exposurenotes ==
           "Adult" & EXPOSURE == "BMI")

# Calculate lower and upper intervals given a
# point estimate and a pvalue
Wes_2022 <- P2 %>%
  filter(pmid.y == 35947639) %>%
  mutate(lowerinterval = CI_calc_lower(effectsize,
                                       pvalue)) %>%
  mutate(upperinterval = CI_calc_upper(effectsize,
                                       pvalue))

P2_less_Wes_2022 <- P2 %>%
  filter(pmid.y != 35947639)

# row bind the two dataframes
P2 <- rbind(Wes_2022, P2_less_Wes_2022)
# subset the data P2 scale the Beta effect
# estimates in place
P2[P2$sd != 0, ]$effectsize = P2[P2$sd != 0, ]$effectsize *
  P2[P2$sd != 0, ]$sd
P2[P2$sd != 0, ]$lowerinterval = P2[P2$sd != 0, ]$lowerinterval *
  P2[P2$sd != 0, ]$sd
P2[P2$sd != 0, ]$upperinterval = P2[P2$sd != 0, ]$upperinterval *
  P2[P2$sd != 0, ]$sd

# Diastolic blood pressure,Beta estimates
P3 <- dat1 %>%
  arrange(ID) %>%
  filter(effectsizetype_id == "ID4" & OUTCOMEID ==
           "O3" & AnalysisType == "Main" & exposurenotes ==
           "Adult" & EXPOSURE == "BMI")

P3[P3$sd != 0, ]$effectsize = P3[P3$sd != 0, ]$effectsize *
  P3[P3$sd != 0, ]$sd
P3[P3$sd != 0, ]$lowerinterval = P3[P3$sd != 0, ]$lowerinterval *
  P3[P3$sd != 0, ]$sd
P3[P3$sd != 0, ]$upperinterval = P3[P3$sd != 0, ]$upperinterval *
  P3[P3$sd != 0, ]$sd

# Hypertension; risk difference
P4 <- dat1 %>%
  arrange(ID) %>%
  filter(effectsizetype_id == "ID5" & OUTCOMEID ==
           "O1" & AnalysisType == "Main" & exposurenotes ==
           "Adult" & EXPOSURE == "BMI")
# Results expressed as increase in unit BMI
# percentage point. Thus: multiply by sd and
# divide by 100
P4[P4$sd != 0, ]$effectsize = P4[P4$sd != 0, ]$effectsize *
  P4[P4$sd != 0, ]$sd/100
P4[P4$sd != 0, ]$lowerinterval = P4[P4$sd != 0, ]$lowerinterval *
  P4[P4$sd != 0, ]$sd/100
P4[P4$sd != 0, ]$upperinterval = P4[P4$sd != 0, ]$upperinterval *
  P4[P4$sd != 0, ]$sd/100

# Diastolic blood pressure, risk difference
P5 <- dat1 %>%
  arrange(ID) %>%
  filter(effectsizetype_id == "ID5" & OUTCOMEID ==
           "O3" & AnalysisType == "Main" & exposurenotes ==
           "Adult" & EXPOSURE == "BMI")

# 1SD increase in BMI increases 0.145 SD of DBP.
# Thus:
P5[P5$sd != 0, ]$effectsize = P5[P5$sd != 0, ]$effectsize *
  P5[P5$sd != 0, ]$sd
P5[P5$sd != 0, ]$lowerinterval = P5[P5$sd != 0, ]$lowerinterval *
  P5[P5$sd != 0, ]$sd
P5[P5$sd != 0, ]$upperinterval = P5[P5$sd != 0, ]$upperinterval *
  P5[P5$sd != 0, ]$sd





# Results  

forest_plot <- function(dat1,x,y,xmin,xmax,
                        title = " ",xlab =" ", ylab = " ",colour,xintercept){
  plot <- dat1 %>% 
    ggplot(.)+
    geom_segment(aes(x = {{x}}, y={{y}},yend={{y}},xend={{x}}))+
    geom_point(aes(x = {{x}}, y={{y}},color = colour))+
    geom_errorbarh(aes(xmin={{xmin}},xmax={{xmax}},y={{y}},height = .2))+
    labs(title=title, x=xlab, y =ylab ) +
    geom_vline(xintercept=xintercept, color=colour, linetype='dashed', alpha=.5)+
    theme_classic()
  return(plot)
}


## Odds ratio Hypertension
plot1 <- forest_plot(Total, x = oddsratio, y = reorder(ID,
                                                       -year), xmin = OR_LI, xmax = OR_UI, title = "Forest plot based on odds ratio",
                     xlab = "Odds ratio (95% CI) per SD increase in BMI",
                     ylab = "Author_PMID_Year", colour = "red", xintercept = 1)
plot1 <- ggplotly(plot1)
plot1

plot2 <- forest_plot(P2, x = effectsize, y = reorder(ID,
                                                     -year), xmin = lowerinterval, xmax = upperinterval,
                     title = "Forest plot based on beta estimates",
                     xlab = "Systolic blood pressure change in mmHg per one SD increase in BMI (Kg/m2)",
                     ylab = "Author_PMID_Year", colour = "red", xintercept = 0)

plot2 <- ggplotly(plot2)
plot2

### Diastolic blood pressure

plot3 <- forest_plot(P3, x = effectsize, y = reorder(ID,
                                                     -year), xmin = lowerinterval, xmax = upperinterval,
                     title = "Forest plot based on beta estimates",
                     xlab = "Diastolic blood pressure change in mmHg per one SD increase in BMI (Kg/m^2)",
                     ylab = "Author_PMID_Year", colour = "red", xintercept = 0)

plot3 <- ggplotly(plot3)
plot3

## Risk difference Hypertension


plot4 <- forest_plot(P4, x = effectsize, y = reorder(ID,
                                                     -year), xmin = lowerinterval, xmax = upperinterval,
                     title = "Forest plot based on risk difference",
                     xlab = "Risk difference (95% CI) per SD increase in BMI",
                     ylab = "Author_PMID_Year", colour = "red", xintercept = 0)

plot4 <- ggplotly(plot4)
plot4


### Diastolic blood pressure
plot5 <- forest_plot(P5, x = effectsize, y = reorder(ID,
                                                     -year), xmin = lowerinterval, xmax = upperinterval,
                     title = "Forest plot based on risk difference",
                     xlab = "Diastolic blood pressure change in mmHg per one SD unit of BMI",
                     ylab = "Author_PMID_Year", colour = "red", xintercept = 0)
plot5 <- ggplotly(plot5)
plot5


## Metaanalysis
MR_metaanalysis <- function(dat, method, measure) {
  dat$logor <- log(dat$oddsratio)
  dat$SE <- (log(dat$OR_UI) - log(dat$OR_LI))/(2 *
                                                 qnorm(0.025))
  mr_meta <- rma(yi = dat$logor, sei = dat$SE, method = method,
                 measure = measure)
  return(mr_meta)
}




### Metaanalysis of studies that investigated
### genetic predisposition to higher BMI on the
### risk of hypertension


p1 <- MR_metaanalysis(Total, method = "REML", measure = "OR")

summary(p1)
confint(p1)

# forestplot ORs
forest_plot <- function(meta_res, dat, refline, xlab = " ") {
  forest(meta_res, header = "Author_PMID_Year", pch = 16,
         cex = 0.75, xlab = xlab, transf = exp, refline = refline,
         slab = dat$ID, xlim = c(-16, 10), at = seq(-2,
                                                    3, by = 1), ilab = cbind(dat$samplesize,
                                                                             dat$NO_ofIVs), ilab.xpos = c(-5, -1), order = "obs")
  text(c(-5, -1), 10, c("Sample size", "No of IVs"),
       cex = 0.75, font = 2)
  text(-16, -1, pos = 4, cex = 0.75, bquote(paste("RE Model (Q = ",
                                                  .(formatC(meta_res$QE, digits = 2, format = "f")),
                                                  ", df = ", .(meta_res$k - meta_res$p), ", p = ",
                                                  .(formatC(meta_res$QEp, digits = 2, format = "f")),
                                                  "; ", I^2, " = ", .(formatC(meta_res$I2, digits = 1,
                                                                              format = "f")), "%)")))
}


forest_plot(meta_res = p1, dat = Total, refline = 1,
            xlab = "Odds Ratio")


P2$SE <- (P2$upperinterval - P2$lowerinterval)/(2 *
                                                  qnorm((1 - 0.95)/2))  #calculate standard error of beta
res <- rma(yi = P2$effectsize, sei = P2$SE, method = "REML",
           measure = "GEN")
summary(res)
confint(res)

# systolic blood pressure in mmHg
forest(res, xlim = c(-16, 12), ilab = cbind(P2$samplesize,
                                            P2$NO_ofIVs), ilab.xpos = c(-5, -1), slab = P2$ID,
       cex = 0.75, header = "Authors_PMID_Year", xlab = "Beta coefficients",
       order = "obs")  #,dat = P2,refline = 0, xlab = 'Beta coefficient' )
text(c(-5, -1), 10, c("Sample size", "No of IVs"))
text(-16, -1, pos = 4, cex = 0.75, bquote(paste("RE Model (Q = ",
                                                .(formatC(res$QE, digits = 2, format = "f")), ", df = ",
                                                .(res$k - res$p), ", p = ", .(formatC(res$QEp,
                                                                                      digits = 2, format = "f")), "; ", I^2, " = ",
                                                .(formatC(res$I2, digits = 1, format = "f")), "%)")))

### Metaanalysis of studies that investigated
### genetic predisposition to higher BMI on DBP

P3$SE <- (P3$upperinterval - P3$lowerinterval)/(2 *
                                                  qnorm((1 - 0.95)/2))  #calculate standard error of beta
res <- rma(yi = P3$effectsize, sei = P3$SE, method = "REML",
           measure = "GEN")
summary(res)
confint(res)



# Diastolic blood pressure in mmHg

forest(res, xlim = c(-16, 9), ilab = cbind(P3$samplesize,
                                           P3$NO_ofIVs), ilab.xpos = c(-5, -1), cex = 0.75,
       header = "Authors_PMID_Year", mlab = "", xlab = "Beta coefficients",
       slab = P3$ID, order = "obs")  #,dat = P2,refline = 0, xlab = 'Beta coefficient' )
text(c(-5, -1), 9, c("Sample size", "No of IVs"))
text(-16, -1, pos = 4, cex = 0.75, bquote(paste("RE Model (Q = ",
                                                .(formatC(res$QE, digits = 2, format = "f")), ", df = ",
                                                .(res$k - res$p), ", p = ", .(formatC(res$QEp,
                                                                                      digits = 2, format = "f")), "; ", I^2, " = ",
                                                .(formatC(res$I2, digits = 1, format = "f")), "%)")))


