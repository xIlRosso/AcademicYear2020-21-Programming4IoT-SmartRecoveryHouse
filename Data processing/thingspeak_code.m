clear all
close all
clc
HR=[74
    73 
    75 
    76 
    74 
    73
    75
    75
    74
    75
    74
    74
    61
    68
    61
    67
    63
    66
    64
    66
    67
    73
    76
    72
    75
    74
    76
    75
    73
    75
    73 
    73 
    75 
    74 
    74 
    75
    61 
    64
    67
    65
    66 
    67
    60
    60
    60
    73 
    71 
    71
    76 
    76 
    75 
    74
    73 
    73
    72
    74
    73
    74
    73
    75 
    66
    65 
    67 
    68
    61
    64
    60 
    64 
    66
    69
    75
    74];

Temp=[36.67229847
    36.74233949
    36.93479792 
    36.83616897
    37.27852256
    37.11282007
    37.40323107 
    37.46321118 
    37.44844983 
    37.22701999 
    37.24394931 
    37.39121639
    37.38439771
    37.33833157 
    37.13269878 
    37.00036234 
    37.12999505 
    36.94330312
    36.58917721
    36.68404048
    36.48656652 
    36.23863959
    36.16260629 
    36.11126123
    36.48337372 
    36.50774523 
    36.61417313 
    36.91276786 
    37.17980773 
    37.22182842
    37.4195522  
    37.49837599
    37.30321776
    37.46083418 
    37.25112321
    37.21706488
    37.2513302 
    37.2316004 
    37.47400989 
    37.21359392
    37.21503498
    36.9148732
    36.6105656  
    36.49195643
    36.47443237 
    36.23897747
    36.04954456 
    36.15350644
    36.53295377
    36.43545209
    36.77502285 
    36.89427741 
    37.41235785 
    37.4973591
    37.08745994 
    37.23234475 
    37.242089  
    37.2996986 
    37.35435376
    37.37713773
    37.22158645
    37.40743863
    37.44012953
    37.14661274 
    36.92369896 
    36.70470585
    36.80252662 
    36.50244001 
    36.17014947 
    36.25003122 
    36.30991273
    36.48491888];

Weight=[60.69527982
    60.68610054 
    60.65215258
    60.64039919
    60.78429703
    60.95059542
    60.84569508
    60.73221039
    68.36994253
    62.37344718
    63.69149092
    65.27915288
    65.42393389
    61.25064335 
    60.66641689 
    60.76030897 
    60.83393744 
    60.87683725
    60.78269383
    60.91569924 
    60.87710796 
    60.79736407 
    60.8421319  
    60.71892971
    60.68869363
    60.7239962 
    60.60424022 
    60.76288249 
    60.67206406
    60.88469314
    60.86107823 
    60.68334566 
    69.38882389 
    61.41796348 
    67.40338332 
    69.0938187
    64.82354186 
    62.19334765
    60.83122581 
    60.76360894 
    60.74354173 
    60.81618599
    60.89301161
    60.86270848
    60.76476516
    60.90259654
    60.69481439
    60.70785883
    60.58159116 
    60.74866277 
    60.6843459  
    60.73125012 
    60.74628653 
    60.88498961
    60.94051075 
    60.82115292 
    64.11429735 
    63.55889611 
    65.07047508 
    61.29725749
    64.45018116 
    67.08891466
    60.84524309
    60.86200879 
    60.72727629 
    60.78417796
    60.93534678 
    60.93997243 
    60.90577472 
    60.82928354 
    60.72700406 
    60.78747237];

% Channel ID to read data from 
readChannelID = 1356837; 
% Field IDs 
temperatureFieldID = 1;
heartRateFieldID = 2;
weightFieldID = 3;
addressFieldID = 4;

% Channel Read API Key 
% If your channel is private, then enter the read API Key between the '' below: 
readAPIKey = '36L6M6Y8FN7KGHY9'; 

% Get temperature data for the last 60 minutes from the MathWorks weather 
% station channel. Learn more about the THINGSPEAKREAD function by going to 
% the Documentation tab on the right side pane of this page. 

measuredTemperature = thingSpeakRead(readChannelID,'Fields',temperatureFieldID,'NumMinutes',999999,'ReadKey',readAPIKey); 
measuredTemperature(isnan(measuredTemperature(:,1)),:) = []; % remove all NaN values

measuredHeartRate = thingSpeakRead(readChannelID,'Fields',heartRateFieldID,'NumMinutes',999999,'ReadKey',readAPIKey); 
measuredHeartRate(isnan(measuredHeartRate(:,1)),:) = []; % remove all NaN values

measuredWeight = thingSpeakRead(readChannelID,'Fields',weightFieldID,'NumMinutes',999999,'ReadKey',readAPIKey); 
measuredWeight(isnan(measuredWeight(:,1)),:) = []; % remove all NaN values

catalog_address = thingSpeakRead(readChannelID,'Fields',addressFieldID,'NumMinutes',999999,'ReadKey',readAPIKey,'OutputFormat','table'); 


samples=72;
% HR=HR';
% Temp=Temp';
% Weight=Weight';
t=linspace(1,samples, samples);

%Upsample t
t_up=linspace(1,samples*60, samples*60-60);

%Upsample HR

HR_up=[];
for i=2:samples
    HR_up=[HR_up linspace(HR(i-1), HR(i),60)];
end

%Upsample Temp

Temp_up=[];
for i=2:samples
    Temp_up=[Temp_up linspace(Temp(i-1), Temp(i),60)];
end

%Upsample Weight

Weight_up=[];
for i=2:samples
    Weight_up=[Weight_up linspace(Weight(i-1), Weight(i),60)];
end

%Build input matrix
X=[HR_up;Temp_up;Weight_up;t_up]';

%Divide set into training and test sets
N=length(X(:,1));
N_train=floor(0.7*N);
N_test=N-N_train;

%% Model for HR
%Regressand HR, regressors Temp, Oxyg, Weight, t
%X(:,1) HR -> X(:,2) Temp -> X(:,3)  Weight -> X(:,4) t

%Extract regressand
y=X(:,1);

%Extract regressors
X_regr=X(:,2:4);

%Extract test and train set

y_train=y(1:N_train);
x_train=X_regr(1:N_train, :);

y_test=y(N_train+1:end);
x_test=X_regr(N_train+1:end,:);

%Train the model

w_hat=build_model(x_train, y_train);

%Test the model

y_hat=x_test*w_hat;

%Check performance

diff=abs(y_test-y_hat);

MSE=mean(abs(y_test-y_hat).^2)


%The model built is accurate enough
%Now build the model for future predictions
w_HR=build_model(X_regr, y);

%% Model for Temp
y=X(:,2);

X_regr=X;
X_regr(:,2)=[];

w_Temp=build_model(X_regr, y);

%% Model for Weight

y=X(:,3);
X_regr=X;
X_regr(:,3)=[];

w_weight=build_model(X_regr, y);


%% Write models on a json

s.HR_regression=w_HR;
s.Temp_regression=w_Temp;
s.weight_regression=w_weight;
stri=jsonencode(s);

fid=fopen('Regression_Trained.json','w');
fprintf(fid, stri);
fclose(fid);

%% Post the json file to the catalog
catalog_address=catalog_address.Address;

catalog_address=cell2mat(catalog_address);

addr = strcat(catalog_address, '/trained_models');

catalog_url = addr;
write_url = [catalog_url 'update'];
response = webwrite(write_url,s);

%% compute regressed values
% measuredTemperature, measuredHeartRate, measuredWeight [0, 1, 2]




measuredValues= [measuredHeartRate(end), measuredTemperature(end), measuredWeight(end)]; 

HR_bar = regress(s.HR_regression, measuredValues, 2)

Temp_bar = regress(s.Temp_regression, measuredValues, 1)

Weight_bar = regress(s.weight_regression, measuredValues, 3)

out_data.Temp=Temp_bar;
out_data.HeartR=HR_bar;
out_data.Weight=Weight_bar;

addr=strcat(catalog_address, '/regression_result');

write_url = [addr 'update'];
response = webwrite(write_url, out_data);


%% Model building function LLS (Linear Least Squares)
function w=build_model(x, y)
    w=(x'*x)\x'*y;
end


%% regressed value computation with simple multiplication

function bar = regress(w, x, no_extr)
    w(no_extr)=[];
    x(no_extr)=[];
    bar=x*w;
end