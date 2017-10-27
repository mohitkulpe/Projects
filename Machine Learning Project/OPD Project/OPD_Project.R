
#  Loading Data

library(ISLR)
library(MASS)

mydata <- read.csv('OPD_2C.csv')

head(mydata)
dim(mydata)

# 1. Checking for Missing Values 'NA'

sum(is.na(mydata))


# 2. Correlations between variables

cor(mydata[1:6])


# 3. Visualize Highly Correlated variables    

library(ggplot2)
library(gridExtra)

x <- qplot(x=mydata$pelvic_incidence, y=mydata$sacral_slope, color=mydata$class, shape=mydata$class, geom='point', main = 'pelvic_incidence vs sacral_slope', ylab = 'sacral_slope', xlab = 'pelvic_incidence')+scale_shape(solid=FALSE)
x


# 4. Checking Outliers


# Checking Outliers in pelvic_incidence

urange1 = mean(mydata$pelvic_incidence)+3*sd(mydata$pelvic_incidence)

lrange1 = mean(mydata$pelvic_incidence)-3*sd(mydata$pelvic_incidence)

o1 = which(mydata$pelvic_incidence < lrange1 | mydata$pelvic_incidence > urange1)


# Checking Outliers in pelvic_tilt.numeric 
urange2 = mean(mydata$pelvic_tilt.numeric)+3*sd(mydata$pelvic_tilt.numeric)

lrange2 = mean(mydata$pelvic_tilt.numeric)-3*sd(mydata$pelvic_tilt.numeric)

o2 = which(mydata$pelvic_tilt.numeric < lrange2 | mydata$pelvic_tilt.numeric > urange2)

outlier <- append(o1,o2)


# Checking Outliers in pelvic_radius 
urange3 = mean(mydata$pelvic_radius)+3*sd(mydata$pelvic_radius)

lrange3 = mean(mydata$pelvic_radius)-3*sd(mydata$pelvic_radius)

o3 = which(mydata$pelvic_radius < lrange3 | mydata$pelvic_radius > urange3)

outlier <- append(outlier,o3)


# Checking Outliers in lumbar_lordosis_angle 
urange4 = mean(mydata$lumbar_lordosis_angle)+3*sd(mydata$lumbar_lordosis_angle)

lrange4 = mean(mydata$lumbar_lordosis_angle)-3*sd(mydata$lumbar_lordosis_angle)

o4 = which(mydata$lumbar_lordosis_angle < lrange4 | mydata$lumbar_lordosis_angle > urange4)

outlier <- append(outlier,o4)


# Checking Outliers in sacral_slope 
urange5 = mean(mydata$sacral_slope)+3*sd(mydata$sacral_slope)

lrange5 = mean(mydata$sacral_slope)-3*sd(mydata$sacral_slope)

o5 = which(mydata$sacral_slope < lrange5 | mydata$sacral_slope > urange5)

outlier <- append(outlier,o5)


# Checking Outliers in degree_spondylolisthesis 
urange6 = mean(mydata$degree_spondylolisthesis)+3*sd(mydata$degree_spondylolisthesis)

lrange6 = mean(mydata$degree_spondylolisthesis)-3*sd(mydata$degree_spondylolisthesis)

o6 = which(mydata$degree_spondylolisthesis < lrange6 | mydata$degree_spondylolisthesis > urange6)

outlier <- append(outlier,o6)



# Outlier present in data with respect to row numbers

uni <- sort(unique(outlier))
uni


# 5. Handling Outliers

### 1.Delete Entire Row 

newdata <- mydata[-uni,]
dim(newdata)


###2. Replace by Median  


mydata1 <- read.csv('OPD_2C.csv')

#replace by Median 1
mydata1$pelvic_incidence[which(mydata1$pelvic_incidence < lrange1 | mydata1$pelvic_incidence > urange1)] <- median(mydata1$pelvic_incidence)

#replace by Median 2
mydata1$pelvic_tilt.numeric[which(mydata1$pelvic_tilt.numeric < lrange2 | mydata1$pelvic_tilt.numeric > urange2)] <- median(mydata1$pelvic_tilt.numeric)

#replace by Median 3
mydata1$pelvic_radius[which(mydata1$pelvic_radius < lrange3 | mydata1$pelvic_radius > urange3)] <- median(mydata1$pelvic_radius)

#replace by Median 4
mydata1$lumbar_lordosis_angle[which(mydata1$lumbar_lordosis_angle < lrange4 | mydata1$lumbar_lordosis_angle > urange4)] <- median(mydata1$lumbar_lordosis_angle)

#replace by Median 5
mydata1$sacral_slope[which(mydata1$sacral_slope < lrange5 | mydata1$sacral_slope > urange5)] <- median(mydata1$sacral_slope)

#replace by Median 6
mydata1$degree_spondylolisthesis[which(mydata1$degree_spondylolisthesis < lrange6 | mydata1$degree_spondylolisthesis > urange6)] <- median(mydata1$degree_spondylolisthesis)



# 6. Summarizing datasets   

summary(mydata)
summary(newdata)
summary(mydata1)


# 7. Model Fitting  


# Fit logistic regression with all features & dataset with outliers
glm.fit_mydata <- glm(class ~ . ,data=mydata ,family=binomial)
summary(glm.fit_mydata)

# Fit logistic regression with all features & dataset without outliers (Row deletion method)
glm.fit_newdata <- glm(class ~ . ,data=newdata ,family=binomial)
summary(glm.fit_newdata)

# Fit logistic regression with all features & dataset without outliers (Median replace method)
glm.fit_mydata1 <- glm(class ~ . ,data=mydata1 ,family=binomial)
summary(glm.fit_mydata1)



# 8. Overall fraction of correct predictions   

### Overall fraction of correct predictions with all features & dataset with outliers.   


probability_mydata <- predict(glm.fit_mydata, type = "response")

pred_mydata <- rep("Abnormal", length(probability_mydata))
pred_mydata[probability_mydata > 0.5] <- "Normal"

#Confusion Matrix
table(pred_mydata, mydata$class)
mean(pred_mydata == mydata$class )


### Overall fraction of correct predictions all features & dataset without outliers (Row deletion method)  

probability_newdata <- predict(glm.fit_newdata, type = "response")

pred_newdata <- rep("Abnormal", length(probability_newdata))
pred_newdata[probability_newdata > 0.5] <- "Normal"

#Confusion Matrix
table(pred_newdata, newdata$class)

mean(pred_newdata == newdata$class)
    
  
  
### Overall fraction of correct predictions with all features & dataset without outliers (Median replace method)   
  
 probability_mydata1 <- predict(glm.fit_mydata1, type = "response")

pred_mydata1 <- rep("Abnormal", length(probability_mydata1))
pred_mydata1[probability_mydata1 > 0.5] <- "Normal"

#Confusion Matrix
table(pred_mydata1, mydata1$class)

mean(pred_mydata1 == mydata1$class)



# 9. Trying to increase fraction of correct predictions:    
## Deciding Important Feature to increase fraction of correct predictions.    


summary(glm.fit_mydata1)


## Selecting Important Feature by using Backward Selection Method  

#### So we will use pelvic_radius & degree_spondylolisthesis in this model.   
  

# Subset selection 1

glm.fit_mydata1_1 <- glm(class ~ pelvic_radius+degree_spondylolisthesis ,data=mydata1 ,family=binomial)

probability_mydata1_1 <- predict(glm.fit_mydata1_1, type = "response")

pred_mydata1_1 <- rep("Abnormal", length(probability_mydata1_1))
pred_mydata1_1[probability_mydata1_1 > 0.5] <- "Normal"
table(pred_mydata1_1, mydata1$class)

mean(pred_mydata1_1 == mydata1$class )
     
  
#### Now we will try another combination of pelvic_incidence, lumbar_lordosis, pelvic_radius & degree_spondylolisthesis because these 4 features have p-value close to zero.   
  

#Subset selection 2

glm.fit_mydata1_2 <- glm(class ~ pelvic_incidence+lumbar_lordosis_angle+pelvic_radius+degree_spondylolisthesis ,data=mydata1 ,family=binomial)

probability_mydata1_2 <- predict(glm.fit_mydata1_2, type = "response")

pred_mydata1_2 <- rep("Abnormal", length(probability_mydata1_2))
pred_mydata1_2[probability_mydata1_2 > 0.5] <- "Normal"
table(pred_mydata1_2, mydata1$class)

mean(pred_mydata1_2 == mydata1$class )


# 10. Cross Validation  

### Split data into Training (80%) & Test (20%)     


set.seed(1)
subset <- sample(nrow(mydata1), nrow(mydata1) * 0.8)
train_mydata1 = mydata1[subset, ]
test_mydata1 = mydata1[-subset, ]


### Fitting Model with Training Dataset.   

set.seed(1)
glm.train_mydata1 <- glm(class ~ ., data=train_mydata1,family = binomial)

train_mydata1.probability <- predict(glm.train_mydata1, test_mydata1, type="response")
train_mydata1_class <- ifelse(train_mydata1.probability > 0.5, 'Normal', 'Abnormal')
table(test_mydata1$class, train_mydata1_class)

mean(train_mydata1_class == test_mydata1$class)


# 11. Plotting ROC   


library(ROCR) 
library(Metrics)

pr <- prediction(train_mydata1.probability, test_mydata1$class)
perf <- performance(pr,measure = "tpr",x.measure = "fpr")
par(mfrow = c(1,1))
plot(perf, main='ROC')



# 12. Testing Model on random data  


testdata = data.frame(pelvic_incidence=40.25020, pelvic_tilt.numeric=13.921907, lumbar_lordosis_angle=25.12495, sacral_slope=26.32829, pelvic_radius=130.32787, degree_spondylolisthesis=2.230652)

glm.fit_mydata1
result <- predict(glm.fit_mydata1, testdata, type="response")

if (result>=0.0 & result < 0.50) {print('Abnormal')
  
}else {print('Normal')}


