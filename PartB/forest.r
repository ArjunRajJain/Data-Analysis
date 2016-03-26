library(ggplot2)
library(randomForest)
setwd("/Users/arjunjain/Dropbox/WealthfrontTask/PartB");

set.seed(1)in
train <- read.csv("input/train.csv", stringsAsFactors=FALSE)
test  <- read.csv("input/test.csv",  stringsAsFactors=FALSE)
#,"int_rate","installment","emp_length","home_ownership","annual_inc","loan_status","purpose","addr_state"
extractFeatures <- function(data) {
  features <- c("loan_amnt","funded_amnt","term")
  fea <- data[,features]
  for(feature in features) {
    fea[feature][!is.na(fea[feature])] <- 0
  }
  #print(fea$term[1])
  fea$term <- as.factor(fea$term)
  #fea$Age[is.na(fea$Age)] <- 
  #fea$Fare[is.na(fea$Fare)] <- median(fea$Fare, na.rm=TRUE)
  #fea$Embarked[fea$Embarked==""] = "S"
  #fea$Sex      <- as.factor(fea$Sex)
  #fea$Embarked <- as.factor(fea$Embarked)
  return(fea)
}

rf <- randomForest(extractFeatures(train), as.factor(train$good), ntree=100, importance=TRUE)

submission <- data.frame(id = test$id)
submission$good <- predict(rf, extractFeatures(test))
write.csv(submission, file = "1_random_forest_r_submission.csv", row.names=FALSE)

imp <- importance(rf, type=1)
featureImportance <- data.frame(Feature=row.names(imp), Importance=imp[,1])

p <- ggplot(featureImportance, aes(x=reorder(Feature, Importance), y=Importance)) +
  geom_bar(stat="identity", fill="#53cfff") +
  coord_flip() + 
  theme_light(base_size=20) +
  xlab("") +
  ylab("Importance") + 
  ggtitle("Random Forest Feature Importance\n") +
  theme(plot.title=element_text(size=18))

ggsave("2_feature_importance.png", p)