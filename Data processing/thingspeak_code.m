clear all
close all
clc
HR=[76.0,
    74.0,
    74.0,
    76.0,
    74.0,
    75.0,
    73.0,
    72.0,
    75.0,
    74.0,
    74.0,
    75.0,
    67.0,
    65.0,
    64.0,
    61.0,
    67.0,
    60.0,
    61.0,
    61.0,
    61.0,
    69.0,
    70.0,
    73.0,
    73.0,
    74.0,
    75.0,
    75.0,
    74.0,
    74.0,
    74.0,
    74.0,
    75.0,
    72.0,
    73.0,
    72.0,
    64.0,
    68.0,
    67.0,
    68.0,
    66.0,
    63.0,
    61.0,
    62.0,
    63.0,
    72.0,
    74.0,
    76.0,
    74.0,
    75.0,
    75.0,
    74.0,
    75.0,
    73.0,
    75.0,
    75.0,
    72.0,
    72.0,
    73.0,
    72.0,
    64.0,
    68.0,
    67.0,
    64.0,
    65.0,
    62.0,
    64.0,
    60.0,
    63.0,
    75.0,
    74.0,
    72.0];

Temp=[
 36.64517936216756,
    36.42013939491984,
    36.827671696318745,
    37.08351419274047,
    37.32615287327342,
    37.34335362725011,
    37.12349465892651,
    37.4741094029819,
    37.21751757239251,
    37.361506801819154,
    37.21472234001526,
    37.36880429978299,
    37.43448132929658,
    37.45950399480584,
    37.195583942761274,
    37.303452763592084,
    37.297524860340395,
    36.90145710166203,
    36.44618153453252,
    36.333956067647115,
    36.53744996243563,
    36.50710482613424,
    36.3571892682103,
    36.2755490667502,
    36.27636658679548,
    36.74209636111999,
    36.854897159782304,
    36.96854122171806,
    36.95788342030413,
    37.09862050360426,
    37.0142265741663,
    37.31291593911299,
    37.35975840471846,
    37.449590583487414,
    37.27543969956493,
    37.22443300148096,
    37.34378900766621,
    37.43562520596157,
    37.08954641253515,
    37.35639294739414,
    37.0514732479413,
    36.94037279954141,
    36.80310537785269,
    36.40363213528436,
    36.27467019146848,
    36.301364559055045,
    36.488743772370455,
    36.4338917489294,
    36.396763741438285,
    36.61463445920175,
    37.00912882132045,
    36.92626618057648,
    36.96605876332328,
    37.29921968102481,
    37.274455221215554,
    37.24191270686752,
    37.483074871393605,
    37.37975737027541,
    37.28029162156317,
    37.41545161825496,
    37.26992731423122,
    37.26009031807058,
    37.01981036060221,
    37.29854205074782,
    36.83570334886009,
    36.77477319607842,
    36.90521500718981,
    36.5616282578264,
    36.24431862706924,
    36.3209261805752,
    36.1855515613592,
    36.08103270294077   
];

Weight=[
    62.181280283434205,
    62.132218606082866,
    62.18485320612798,
    62.22251947349646,
    62.387366123299124,
    62.367603958406455,
    62.25178219664796,
    62.368039267350284,
    62.29306401017143,
    62.5255792639746,
    62.33167511347155,
    62.57592060893789,
    62.51205066337074,
    62.528922353415545,
    62.248478450961244,
    62.391796746805866,
    62.240017364621664,
    62.25926730312477,
    62.33238459873841,
    62.28165901975261,
    62.33617182750455,
    62.39090210486882,
    62.1768655108383,
    62.28303054734244,
    62.032139848515136,
    62.28702863772945,
    62.00381043484271,
    62.21418644037776,
    62.14620565093997,
    62.270354447286955,
    62.360826467094,
    62.27460868526201,
    62.400116469859164,
    62.250889042794455,
    62.37888942410503,
    62.52356172253896,
    62.665946182187795,
    62.55079535696542,
    62.33021514276279,
    62.35950522899462,
    62.37127472944119,
    62.347045661889354,
    62.25171791779143,
    62.44127976197297,
    62.359627495830125,
    62.21638909554248,
    62.20856469304002,
    62.181435302603745,
    62.20097116639806,
    62.098052245933836,
    62.15838789644345,
    62.1641793708367,
    62.31241546907197,
    62.42552614878522,
    62.42783216873328,
    62.256236003363306,
    62.196174286496245,
    62.49453813128815,
    62.432036659757465,
    62.44188641797743,
    62.41672903027593,
    62.46912808103955,
    62.24717719339175,
    62.266336493495686,
    62.35236542798301,
    62.43612527918987,
    62.34597639718404,
    62.311796292345925,
    62.236389573206424,
    62.36158844140792,
    62.23287767437245,
    62.27651912656763
];

% Channel ID to read data from 
readChannelID = 1356837; 
% Field IDs 
temperatureFieldID = 1;
heartRateFieldID = 2;
weightFieldID = 3;

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

catalog_url = 'http://482bab82faa6.ngrok.io/trained_models/';
write_url = [catalog_url 'update'];
response = webwrite(write_url,s);

%% Model building function LLS (Linear Least Squares)
function w=build_model(x, y)
    w=(x'*x)\x'*y;
end
