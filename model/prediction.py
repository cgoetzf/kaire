import pandas as pd
import numpy as np
import globals as gb

class Predictor:
    def __init__(self):
        self.static = True
        
    def init_dataset(self):
        if self.static:
            url = "C:\\_Workspace\\Kaire\\python\\ds\\training_ds.csv"
            # load dataset into Pandas DataFrame
            self.df = pd.read_csv(url, names=['id','stress','locationId','activity','timestamp','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond','classification','cond'],skiprows=1)
        else:
            from mysqlDb import mysqlConn
            conn = mysqlConn()
            self.df = pd.read_sql('SELECT * FROM history', conn)
        # Separating out the features and target
        #self.features = ['stress','locationId','activity','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond']
        self.features = ['stress','locationId','activity','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond']
        self.x = self.df.loc[:, self.features].values
        self.y = self.df.loc[:,['classification']].values
 

    def init_dataset_prediction(self):
        if self.static:
            url = "C:\\_Workspace\\Kaire\\python\\ds\\prediction_ds.csv"
            # load dataset into Pandas DataFrame
            self.df = pd.read_csv(url, names=['id','stress','locationId','activity','day','hour','stressorId','env_cond','duration','shared_time','classification'],skiprows=1)
        else:
            from mysqlDb import mysqlConn
            conn = mysqlConn()
            self.df = pd.read_sql('SELECT * FROM history', conn)
        # Separating out the features and target
        #self.features = ['stress','locationId','activity','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond']
        self.features = ['locationId','activity','duration','day','hour','stressorId','shared_time','env_cond']
        self.x = self.df.loc[:, self.features].values
        self.y = self.df.loc[:,['classification']].values 

    def standardize(self):
        # Standardizing the features
        from sklearn.preprocessing import StandardScaler
        self.x = StandardScaler().fit_transform(self.x)

    def reduce_dimension(self):
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(self.x)
        self.x = pd.DataFrame(data = principalComponents
                     , columns = ['principal component 1', 'principal component 2'])

        self.finalDf = pd.concat([self.x, self.df[['classification']]], axis = 1)

        #from sklearn.model_selection import train_test_split
        #self.x_trainrd, self.x_testrd, self.y_trainrd, self.y_testrd = train_test_split(self.x, self.y, test_size=0.3, shuffle = False, stratify = None) # if size = 0.3, 70% training and 30% test
  
    def split_dataset(self,size):
        #training dataset
        from sklearn.model_selection import train_test_split
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=size, shuffle = False, stratify = None) # if size = 0.3, 70% training and 30% test
        #print("##########","Training dataset has ",self.x_train.shape," rows and evaluation dataset has ", self.x_test.shape, "##########")

    def svm_predict(self):
        #SVM
        from sklearn import svm

        classifier = svm.SVC(kernel='rbf', probability=True) # RBF Kernel
        classifier.fit(self.x_train, self.y_train)
        self.y_pred_svm = classifier.predict(self.x_test)
        self.y_prob_svm = classifier.predict_proba(self.x_test)

    def rf_predict(self):
        #RF
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(max_depth=4, random_state=0) # RBF Kernel
        y = self.y_train.reshape(-1, 1)
        np.ravel(self.y_train)
        classifier.fit(self.x_train, self.y_train.ravel())
        self.y_pred_rf = classifier.predict(self.x_test)
        self.y_prob_rf = classifier.predict_proba(self.x_test)

    def show_metrics(self, ):
        #Metrics
        from sklearn import metrics
        print("\n##############\n")
        print("Metrics for SVM")
        print("Metrics")
        print("Accuracy:",round(metrics.accuracy_score(self.y_test, self.y_pred_svm),4))
        print("Precision:",round(metrics.precision_score(self.y_test, self.y_pred_svm,zero_division=0),4))
        print("Recall:",round(metrics.recall_score(self.y_test, self.y_pred_svm),4))
        print("F1:",round(metrics.f1_score(self.y_test, self.y_pred_svm,zero_division=0),4))
        print("\n##############\n")
        print("Metrics for RF")
        print("Metrics")
        print("Accuracy:",round(metrics.accuracy_score(self.y_test, self.y_pred_rf),4))
        print("Precision:",round(metrics.precision_score(self.y_test, self.y_pred_rf,zero_division=0),4))
        print("Recall:",round(metrics.recall_score(self.y_test, self.y_pred_rf),4))
        print("F1:",round(metrics.f1_score(self.y_test, self.y_pred_rf,zero_division=0),4))
        print("\n##############\n")


    def show_graph_std(self):
        #Show plot
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize = (8,8))
        ax = fig.add_subplot(1,1,1) 
        ax.set_xlabel('PC1', fontsize = 15)
        ax.set_ylabel('PC2', fontsize = 15)
        ax.set_title('Standardized', fontsize = 20)
        targets = [0, 1]
        colors = ['r', 'g']
        for target, color in zip(targets,colors):
            indicesToKeep = self.finalDf['classification'] == target
            ax.scatter(self.finalDf.loc[indicesToKeep, 'principal component 1']
                       , self.finalDf.loc[indicesToKeep, 'principal component 2']
                       , c = color
                       , s = 50)
        ax.legend(targets)
        ax.grid()
        plt.savefig("img/scatter_sdt.png")
        #plt.show()

    def show_graph_nonstd(self):
        #Save image file
        from graph import scatter

        img = scatter('Non-Standardized', 'PC1', 'PC2')
        img.build(self.finalDf, 'principal component 1', 'principal component 2','classification')
        img.save("scatter_nonsdt")
        #img.show()

    def show_probability(self):
        #prob = pd.DataFrame(self.y_prob,columns=['probA','probability_svm'],index=[93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133])
        prob = pd.DataFrame(self.y_prob_svm,columns=['probA','probability_svm'])
        del prob["probA"]
        #prob_rf = pd.DataFrame(self.y_prob_rf,columns=['probB','probability_rf'],index=[93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133])
        prob_rf = pd.DataFrame(self.y_prob_rf,columns=['probB','probability_rf'])
        del prob_rf["probB"]
        prob['probability_svm'] = prob['probability_svm'].apply(lambda x: round(x*100,2))
        prob_rf = prob_rf.apply(lambda y: round(y*100,2))
        result = pd.concat([self.df.tail(prob.size).reset_index(drop=True),prob], axis=1)
        result = pd.concat([result,prob_rf], axis=1)
        result.to_csv(gb.DATASET_PATH+"result_ds.csv", index=False)
        print(result)

    def show_confusion_matrix(self):
        #Show plot
        import matplotlib.pyplot as plt
        from sklearn import metrics

        confusion_matrix = metrics.confusion_matrix(self.y_test, self.y_pred_svm)
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
        cm_display.plot()
        cm_display.ax_.set_title("Confusion Matrix for SVM")
        plt.savefig("img/confusion_matrix_svm.png")
        plt.show()
        
        confusion_matrix = metrics.confusion_matrix(self.y_test, self.y_pred_rf)
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
        cm_display.plot()
        cm_display.ax_.set_title("Confusion Matrix for RF")
        plt.savefig("img/confusion_matrix_rf.png")
        plt.show()
        
    def line_graph (self):
        import matplotlib.pyplot as plt
        import numpy as np
        
        url = "C:\\_Workspace\\Kaire\\python\\ds\\linegraph.csv"
        # load dataset into Pandas DataFrame
        self.df = pd.read_csv(url, names=['id','stress','locationId','activity','timestamp','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond','classification','cond'],skiprows=1)
        #self.features = ['timestamp', 'HR', 'HRV']
        self.features = ['duration','hrv_mean','hrv_sd','shared_time']
        self.y = self.df.loc[:, self.features].values
        self.x = self.df.loc[:, ['timestamp']].values
        #self.yhr = self.df.loc[:,['HR']].values
        #self.yhrv = self.df.loc[:,['HRV']].values
        #x = [1,2,3,4,5]
        #y = [3,3,3,3,3]
          
        # plot lines
        plt.plot(self.x, self.y, label = ['duration','hrv','sdnn','shared_time'])
        #plt.plot(self.x, self.y['HRV'], label = "HRV")
        plt.legend()
        plt.savefig("img/line_nonstd.png")
        plt.show()
        from sklearn.preprocessing import StandardScaler
        self.y = StandardScaler().fit_transform(self.y)
        plt.plot(self.x, self.y, label = ['duration','hrv','sdnn','shared_time'])
        plt.legend()
        plt.savefig("img/line_std.png")
        plt.show()
        
    def line_graph_feat (self):
        import matplotlib.pyplot as plt
        import numpy as np
        url = "C:\\_Workspace\\Kaire\\python\\ds\\line_ds.csv"
        # load dataset into Pandas DataFrame
        self.df = pd.read_csv(url, names=['id','stress','timestamp','hr','rmssd','sdrr','rr'],skiprows=1)
        self.features = ['stress','hr','rmssd','sdrr','rr']
        self.y = self.df.loc[:, self.features].values
        self.x = self.df.loc[:, ['timestamp']].values
        plt.plot(self.x, self.y, label = ['stress','hr','rmssd','sdrr','rr'])
        plt.legend()
        plt.show()
        from sklearn.preprocessing import StandardScaler
        self.y = StandardScaler().fit_transform(self.y)
        plt.plot(self.x, self.y, label = ['stress','hr','rmssd','sdrr','rr'])
        plt.legend()
        plt.show()
       