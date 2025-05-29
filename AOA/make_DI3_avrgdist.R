install.packages("CAST", repos = "https://cloud.r-project.org/")
#utils::install.packages("miceadds")
library(CAST)
library(vroom)
library(parallel)
library(bigmemory)
library(RANN) 
library(doParallel)
library(foreach)
library(miceadds)
glob_start_time <- Sys.time()

sample_percentages <- c(1:10 %o% 10^(-7:-4))
source("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_scripts/train_DI_avrgdist.R")
variables <- c('city', 'LC_CORINE', 'IMPERV', 'HEIGHT', 'COAST', 'ELEV', 'POP', 'RH', 'SP', 'PRECIP','T_2M', 'wind_speed', 'TCC',  'CAPE', 'BLH', 'SSR','SOLAR_ELEV', 'DECL')
cluster3_data <- miceadds::load.Rdata2(filename = "../AOA_data/CLUSTER3_TRAIN_VAL.RData")
cluster3_data <- cluster3_data[variables]
cluster3_val_folds <- read.csv("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/folds_CLUSTER3.csv", header = TRUE)
cluster3_val_folds <- as.matrix(cluster3_val_folds)

# Identify rows with NA in cluster1_data
na_rows <- apply(cluster3_data, 1, function(row) any(is.na(row)))

# Remove rows with NA from both datasets
cluster3_data <- cluster3_data[!na_rows, ]
cluster3_val_folds<- cluster3_val_folds[!na_rows, ]
cluster3_val_folds <- as.vector(cluster3_val_folds)

cluster3_weights <- read.csv("../AOA_data/importances_CL3.csv")
cluster3_weights_t <- data.frame(t(cluster3_weights$Importance))

# Set the column names as the feature names
colnames(cluster3_weights_t) <- cluster3_weights$Feature
rownames(cluster3_weights_t) <- NULL


variables <- c('LC_CORINE', 'IMPERV', 'HEIGHT', 'COAST', 'ELEV', 'POP', 'RH', 'SP', 'PRECIP','T_2M', 'wind_speed', 'TCC',  'CAPE', 'BLH', 'SSR','SOLAR_ELEV', 'DECL')
cat("start calculating train_DI \n")
for (i in 1:length(sample_percentages)){
  start_time <- Sys.time()
  train_DI1 <- train_DI(train = cluster3_data, variables = variables, weight = cluster3_weights_t, CVtest = cluster3_val_folds, sample_percentage = sample_percentages[i])
  end_time <- Sys.time()
  total_time <- as.numeric(difftime(end_time, start_time, units = "secs")) 
  # Append results to the CSV files
  write.table(train_DI1$trainDist_avrgmean, 
              file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_avrgmean_multiple.csv", 
              row.names = FALSE, col.names = !file.exists("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_avrgmean_multiple.csv"), 
              append = TRUE, sep = ",")

  write.table(total_time, 
              file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_time_multiple.csv", 
              row.names = FALSE, col.names = !file.exists("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_time_multiple.csv"), 
              append = TRUE, sep = ",")
  write.table(sample_percentages[i], 
              file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_percentages_multiple.csv", 
              row.names = FALSE, col.names = !file.exists("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_percentages_multiple.csv"), 
              append = TRUE, sep = ",")
}

glob_end_time <- Sys.time()
glob_total_time <- as.numeric(difftime(glob_end_time, glob_start_time, units = "secs")) 
#write.csv(scale_df, file = paste0("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_scaleparam_",sample_percentage,".csv"), row.names = FALSE)
write.csv(glob_total_time, file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_global_time_multiple.csv")
#write.csv(train_DI$catvars, file = paste0("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_catvars_",sample_percentage,".csv"), row.names = FALSE)

