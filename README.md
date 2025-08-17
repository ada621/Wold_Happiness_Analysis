'''
--------------------THE GOAL OF MY PROJECT--------------------

In this project I worked with 2018 and 2019 World Happiness Datasets.My goal was to analyse internal structure of each year's data and
the differences and changes between them.
I selected Happiness Score for dependent variable and  GDP per capita, social support, healthy life expectancy, freedom to make life
choices, generosity and perceptions of corruption are independent variables.

I built a modular framework for this work and I tested OLS,Robust OLS,Log OLS and WLS models to determine the best fit for my
project.
I evaluated these models with their AIC,BIC,R-squared scores and correlation with the dependent variable.
As a result,I chose OLS model for my 2018 dataset and Robust OLS model for the my 2019 dataset.(details are explained below)

I added new columns to my datasets in the main file. For the analysis part,I did correlation analysis,basic statistical analysis,
regression modelling and regression diagnostics conjecture analysis.These analyses were carried out in two separate files: 
happiness_analysis_2018.py and happiness_analysis_2019.py

the regression predictions are implemented in regression_2018.py and regression_2019.py files.
In the happiness_graph.py file, I created a analysis graphs for both years.All graph images are saved in the figures folder.


-------------------MODEL SELECTİON------------------------------

For the 2018 dataset I applied OLS model because there was no evidence of heteroskedasticity and the model was fit my data well.
Also I preferred OLS due to its interpretability and simplicity.
But in 2019 dataset exhibited significant heteroskedasticity. For this reason I evaluated OLS,Robust OLS,WLS and Log OLS models in
in a separate file to find the best fit.

The Robust OLS adapted the heteroskedasticity but didn't eliminate it.As a result the model's predictive performance may still
be affected.Because of outliers remain harmful but Robust OLS reduce their influence.It can't be fully ignore them.
Prediction ranges may still be misleading especially when generalizing results.

On the other side WLS gave the highest R-squared(0.99)and lowest AIC(53.16) and BIC(74.51) values.>>> It can cause of overfitting
possibly triggered by outliers.

Log OLS have a lowest AIC and BIC values and ıt means it achieved the best balance between model complexity and fit.

After all of these comperation,I evaluated the confidence intervals for more detailled assentment.
Based on this evaluation, I decided to choose the Robust OLS model for my 2019 dataset because of OLS isn't compatible with
heteroskedasticity and WLS model sensitive to outliers and I have outliers in some variables.
Althought, I didn't select the Log OLS model because ıt could make interpratition more difficult.
With Robust OLS my model compatible with heteroskedasticity and also ıt reduces the influence of outliers.





------CORRELATİON ANALYSİS,REGRESSİON ASSUMPTİONS,REGRESSİON MODEL ANALYSIS AND BASİC STATISTIC INTERPRETATION-----------
------------------------------------------------------------------------------------------------------------------------------------
Observation from BASİC STATİSTİC ANALYSİS----->

The Social support variable is left-skewed in both 2019(-1.135) and 2018(-1.081).Which indicates positive values are predominant.
Based on the Kurtosis values for 2019(1.229) and 2018(1.171),the distributions suggest the presence of outliers.


The GDP per Capita variable is slightly left-skewed in both 2019(-0.385) and 2018(-0.201) which is not large enough to create a 
significant imbalance.
whereas, their kurtosis values 2019(-0.770) and 2018(-0.335) suggest that the distribution is relatively flat,indicating a low presence
of outliers.

The Perception of corruption variable is right-skewed in both 2019(1.650) and 2018(1.684) and their kurtosis values are in 2019(2.417)
and in 2018(2.51) indicate a pronounced skewness and presence of numerous outliers.

The Freedom to make life choices variable is left-skewed in both 2019(-0.686) and 2018(-0.788).The kurtosis values are in 2019(-0.069)
and 2018(-0.011)suggest a generally mild skewness and a very low risk of outliers.

The Generosity variable is right-skewed in both 2019(0.746) and 2018(0.867).Its kurtosis values 2019(1.173) and 2018(1.453).
These results are ixhibit presence of some outliers and a moderate skewness,and we can say skewness magnitude isn't substantial enough.

The Happiness Score (dependent variable) skewness values are (2019:0.011, 2018:0.015) and kurtosis values are (2019:-0.608, 2018:-0.710)
suggest almost perfectly symmetrical and a very low risk of outliers.




Observation from CORRELATİON ANALYSıS----->
Some pronounced relations, both weak and strong.
weak relations--->
Between Happiness Score and Generosity correlation is (2019:0.076, 2018:0.135).This result shows us no pronuenced relation between 
them.

Between Perseptions of corruption and Happiness Score correlation (2019:0.386, 2018:0.403)(r<0.70) suggest low to moderate relation 
between them.

Significant relations---->
Happiness Score is strongly correlated with GDP per capita(2019: 0.794, 2018: 0.802, r > 0.70)this indicating a direct and positive 
relation between economic well-being and happiness.

Happiness Score is strongly and positively correlated with Social support(2019: 0.777, 2018: 0.745, r > 0.70).This indicating a 
relationship between better social relitionships and happiness.

Happiness Score is strongly correlated with Healthy lide expectancy(2019: 0.780, 2018: 0.775, r > 0.70)we can talk about a direct and 
positive relation between life standart and happiness.

More mild relations------>
Between Freedom to make life choices and Happiness score correlation (2019:0.576, 2018:0.544, r<0.70) show to us they have a moderate 
relation.

However,correlation only shows the association between variables;we can't make a causal inference.




Results of REGRESSİON MODEL ANAYSİS------->

İf we examine 2019 R-squared result(0.779) and 2018(0.789),we can say the models can explaning %77.9 of the variance.
2019 Adjusted R-squared(0.7703) and 2018(0.7807) show that the added variables are significant. Suggesting the model is explanatory
without over-using variables.

When we examine the 2019 (AIC:253.53, BIC:274.88) and 2018(AIC:248.08, BIC:269.43) results, we can see that the values are not hight.
So model is fit my dataset well.(AIC and BIC values were almost the same in across all models expect WLS, so we can conclude that these
values are not hight.)

The F-statistic values for 2019(87.62) and 2018(92.95) show that the regression is generally meaningfull.

Looking at the p-values for both 2019 and 2018(0.00..), we can said all independent variables are collectively contribute to the model.





Observation from REGRESSİON ASSUMPTİON ANALYSİS------>

----------Normality Test(Jarque Bera)------------------

The reason why this test preffered is explaned in the happiness_analysis_2019.py file.
after the normality test,I achiveted some results and I evulated them with assumption:
In normality test, ideally p-value should be more than 0.05 to confirm that the resuduals are following a normal distrubution.
In contrast,in my both 2019 and 2018 analysis the p-values were lower(0.03).This situaction could be due to several factors.
For instace,ıf the resuduals are systematically skewed,they may produce outliers.

I investigated whether the resuduals are systematically skewed or not? I observed skewness values(-0.4983) and
this result incidace that residuals distrubution are appoximately simetcial.

Although,unnecessary variables may produce extra variance in residuals but when I examined the Adjusted R-squared and manuelly 
controlled this variables I found R-squared value to be meaningfull and didn't identify any irrelevant variable in the dataset.
However, when I examined the percepitions of corruption's kurtosis and skeweness values, I found both to be considerably highter than
normal.This explains why the normallty of resuduals doesn't fit in expected range.


-----------Homoskedasticity Test(Breush-Pagan)------------------

The test conducted on the 2019 data produced a test statistic of 7.9707 and a p-value of 0.0185. Ideally, we expect the p-value to be 
highter than 0.05 to confirm that the residuals are homoskedastic but in the 2019 data, the p-value is below this threshold,
indicating that the residual variance is not constant and varies with different values. Consequently, confidence intervals may be 
misleading and could lead to incorrect inferences. This may also affect the accuracy of standard error estimates.

The results of 2018 data (test statistic:10.5516, p-value:0.103) indicate that residual variance is constant in here and doesn't
varie with different values. Therefor,the homoskedasticity assumption is satisfied.




------Durbin-Watson Test (autocorelation)-------------

The test for the 2019 data produced a test statistic of 1.6484 and p-value of 1.6483 while the 2018 data yielded test statistic of
1.6452 and p-values is 1.6452. The p-value are above the 0.05 threshold so its exhibit that the assumption of no autocorelation is
satisfied. Consequently,we can make an inference about residuals are independent and don't ffect eachother ın both years. 





-------------ANALYSIS OF VARİABLE İMPORTANCE-------------------------

When examine the variables coefficient sizes we can rank the effects from strongest to small effect:
Freedom to make a life choices: 2019(coefficient=1.4546, p-value=0.00)and 2018(coefficient=1.3687, p-value=0.00)-this suggest that 
sense of control feeling over life is a key determinant in happiness scores.

social support 2019: (coefficient=1.1242, p-value=0.00) and 2018 (coefs=1.0098, p-value=0.000)-shows social connection an relationships
between the peoples have a substancial effect to increasing the happiness scores.

healthy life expectancy: 2019(coefficient=1.0781, p-value=0.0029)and 2018(coefficient=1.8150, p-value=0.0029)-we can say hope for a 
good life have significant impact to happiness scores.

GDP per capita: 2019(coefficient=0.7754, p-value=0.0006)and 2018 (coefficient=0.0942, p-value=0.000)-this result indicate that in 2018,
economic welfare had a effect on the happiness score whereas in 2019 , this variable has stronger effect. We can infer that economic
welfare has significant effect; however,interactions among variables also impact the happiness score.

perceptions of corruption: 2019(coefficient=0.9723, p-value=0.1813)and 2018 (coefficient=0.6824, p-value=0.1996)-this suggest that
its appear substantial cause of coefficent value. Actually the effects aren't significant due to the high p-values.

generosity: 2019(coefficient=0.4898, p-value=0.4268)ve 2018(coefficient=0.5799, p-value=0.2219)-in both years,the  coefficent values
are relatively low and not statistically significant due to their p-values.

Variables of freedom to make life choice,social support and healthy life exhibit strong positive effects; GDP per capita 
has a positive effect in 2018, and a strong positive effect in 2019.





----------------İNTERPRETATİON OF CONFİDENCE İNTERVALS--------------------

When examininig the %95 confidence intervals we expect it not to include zero. It suggest that this variable is statistically 
significant.

According to the confidence intervals, these two variables(Generocity and perseptions of corruption) are not statistically significant.
For 2019, corruption([-0.4531, 2.3977])- Generosity([-0.7183, 1.6978]) and for 2018, carripution([-0.3641, 1.7289])-Generosity
([-0.3542, 1.5140]). All of these confidence intervals include zero.

Other variables confidence intervals don't inculede zero,indicating no issues regarding statistical significance.





----------------REGRESSİON COMPARİSON TO 2018 AND 2019 DATA'S--------------------------

AIC-BIC,R-squared,Adjusted R-squared,F-statistic and F-statictic p-value values are largely similar across both years, and the result
of confidence intervals are also similar too.
For both years,normalty teste indicate that the resudulas aren't normally distributed.
However,,autocorelation test show no revidence of otocoleration in both of years.

The 2018 data appears homoskedastic,whereas the 2019 data is heteroskedastic,indicating that the residual variance in 2019 isn't 
constant.Consequently I applied the OLS model for 2018 analysis while using Robust OLS for 2019 analysis.

For both years,the variables generocity and percepitons of corruption are statisctically insignificant in terms of both confidence
intervals and effect sizes.
However,the GDP per capita variable appears to have a stronger effect on the happiness score in 2019 compared to 2018.




---------------INTERPRATATION OF REGRESSION PREDICTIONS----------------------

Interpretation of regression predictions-2018:
-----------------------------------------------
The regression model of 2018 yielded an RMSE of 0.56 and an R-squared of 0.69,suggesting that the model explains the %69 of variance 
and residual range of 5.6 is relatively low. Consequently the model predicts the data reasonably well.

Predicted values range forom 3.49 to 6.97,indicating that some countries are extremly unhappy while others appear happier.

Evulating the happiness score before and after the regression,we observe that even contries with the highest initial scores experienced
a decrease in their happiness scores and which in some cases resulted in a change of their happiness label.

some examples:
United Kingdom--(happines score=7190, happiness label=high)-(new happiness score=6290,new happiness label=above average)
Costa Rica--(happiness score=7072, happiness label=high)-(new happiness score=6210, happiness label=above average)

Conversaly, some countries showed an icrease in both happiness score and happiness label.
for example:
Qatar--(happiness score=6374, happiness label=above average)-(new happiness score=6660, new happiness label=high)
Singapore--(happiness score=6343, happiness label=above average)-(new happiness score=7080,new happines label=high).


These results provide some insights:
Contries with low happiness scores (e.g., 3.49, 3.93) tent to have more lower economic well-being,freedom standard or social support
and interpersonal relationships.
In contrast,contries with the high happiness scores(e.g., 6.97, 6.71) show highter life satisfaction among their citizens.


We can expect that GDP per capita i.e. income level might be higher,However,this variable doesn't have a statistically significant 
effect on the happiness score.Consequently,contries with low and hight happiness scores may not differ sunstanly in terms of GDP per
capita.

we can expect the value of Freedom to make life choice variable to be highter also.As it has the strongest impact on happiness scores.

According to the model's results, in some countries the happiness level came out lower than expected, which can be explained by
structural inequalities or lack of social support.Predictions above 6 reflect the positive effects of strong economic indicators and
social well-being. When interpreted together with the RMSE value, it can be said that the deviations in predictions are not very large,
so the model captures the general trend fairly well.

2019 regression prediction:
-------------------------------
RMSE: 0.64 and R-squared: 0.60.It exhibit the model can explain 60% of the data, and an error of 0.64 suggests the model’s performance 
is sufficient.
There is a similar trend to 2018. Scores have generally decreased, but we don’t see exactly the same changes.
For example:
United Kingdom:in the 2018 regression,the label dropped from “high” to “above average,” but in 2019,both the original and new happiness 
label stayed at “high.”
The change in happiness labels doesn’t happen in every case,but some countries did see a change. 
For example:
Costa Rica: in 2018, the label dropped from “high” to “above average” as before. 
Qatar: just like in 2018, the label rose from “above average” to “high.”




#----------------GRAPH INTERPRETATION-----------------#

In the happiness label distribution bar chart, the “above average” label increased in 2019 compared to 2018. The “average” and “low”
labels slightly decreased in 2019, while the “very low” label showed a small increase. For the “high” label, we don’t see any change.

From this, we can say that in 2019 the labels shifted more toward the extremes. As the “average” label decreased, the “above average”
and “very low” labels increased. However, the fact that the “high” label didn’t change suggests that this shift wasn’t very strong.
There could be a few reasons for this shift--->
We previously found that GDP per capita had a stronger positive effect on the happiness score in 2018.The decrease in GDP per capita’s
effect might have influenced the label changes.
Another factor affecting the label changes could be the combination of independent variables.
for example:
The “freedom to make life choices” variable is the most influential variable.However,when we compare the United Kingdom’s 2018 and 
2019 data, we see that the freedom to make life choice variable decreased in 2019, while GDP per capita, social support, and healthy 
life expectancy scores increased. This could explain the difference in 2018 labels and why the 2019 label didn’t change.
Perhaps the increase in freedom to make a life choice balance out the decreases in the other variables.



Looking at the variable effects chart, we see that in 2019 the effects of social support, freedom to make life choices, healthy life 
expectancy, and perception of corruption increased, while the effects of GDP per capita and generosity decreased.These changes are
generally around ±0.2. However,since the effects of perception of corruption and generosity are quite weak, we can mostly talk about
their indirect influence rather than a direct one.

From these results, it can be said that freedom to make life choices has a very important and key role in happiness scores. At the same 
time, social support—reflecting interpersonal relationships—and factors with roughly the same level of influence, such as income
distribution (GDP per capita)and healthy life expectancy, are among the most influential and should be considered carefully.

Both generosity and social support relate to social relationships, but the weak effect of generosity can be explained in a few ways:
Generosity mainly refers to helping others, while social support is more about receiving help—support that people get during difficult
times or when in need.

Another important difference is that generosity is often limited to our close social circle, whereas social support can come both 
from personal networks like family and friends and from more structured sources such as institutions or organizations.Therefore, the 
scope of support and impact on individuals can differ significantly.




'''
